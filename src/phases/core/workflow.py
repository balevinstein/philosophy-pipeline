from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from pathlib import Path
import json
from .base_worker import BaseWorker, WorkerInput, WorkerOutput
from .exceptions import WorkflowError


@dataclass
class WorkflowStep:
    worker: BaseWorker
    input_mapping: Dict[str, str]  # Maps workflow state to worker input
    output_mapping: Dict[str, str]  # Maps worker output to workflow state
    name: str  # Step identifier
    save_output: bool = True  # Whether to save step output


class Workflow:
    """Manages execution of multiple workers with state management and output saving"""

    def __init__(
        self,
        initial_step: WorkflowStep,
        cycle_steps: List[WorkflowStep],
        output_dir: Optional[Path] = None,
        max_cycles: int = 1,
    ):
        self.state: Dict[str, Any] = {}
        self.current_cycle = 0

        self.initial_step = initial_step
        self.cycle_steps = cycle_steps
        self.output_dir = output_dir
        self.max_cycles = max_cycles

    def _map_state(
        self, mapping: Dict[str, str], source: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Maps source state to target state using provided mapping"""
        result = {}
        for target_key, source_path in mapping.items():
            value = source
            for key in source_path.split("."):
                if key in value:
                    value = value[key]
                else:
                    raise WorkflowError(f"Missing required state key: {source_path}")
            result[target_key] = value
        return result

    def _update_state(self, mapping: Dict[str, str], output: WorkerOutput):
        """Updates workflow state with worker output"""

        for target_path, source_path in mapping.items():
            value = output.result
            for key in source_path.split("."):
                if key in value:
                    value = value[key]
                else:
                    raise WorkflowError(f"Missing required output key: {source_path}")

            # Handle nested paths in target
            target = self.state
            path_parts = target_path.split(".")
            for part in path_parts[:-1]:
                if part not in target:
                    target[part] = {}
                target = target[part]
            target[path_parts[-1]] = value

    def _save_step_output(self, step: WorkflowStep, output: WorkerOutput):
        """Saves step output to disk"""
        if not self.output_dir or not step.save_output:
            return

        step_dir = self.output_dir / f"cycle_{self.current_cycle}" / step.name
        step_dir.mkdir(parents=True, exist_ok=True)

        # Save main output
        with open(step_dir / "output.json", "w") as f:
            json.dump(
                {
                    "result": output.result,
                    "metadata": output.metadata,
                    "status": output.status,
                },
                f,
                indent=2,
            )

        # Save any markdown content
        if "content" in output.result:
            with open(step_dir / "output.md", "w") as f:
                f.write(output.result["content"])

    def execute(self, initial_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute workflow for specified number of cycles"""
        self.state = initial_state.copy()

        # Execute initial step (development)

        print(f"\nExecuting step: {self.initial_step.name}")

        # Map workflow state to worker input
        try:
            context = self._map_state(self.initial_step.input_mapping, self.state)
        except WorkflowError as e:
            print(f"Error mapping state for step {self.initial_step.name}: {str(e)}")
            raise

        # Execute worker
        input_data = WorkerInput(context=context, parameters={"": ""})

        initial_step_output = self.initial_step.worker.execute(input_data)

        # Save output
        self._save_step_output(self.initial_step, initial_step_output)
        # Update workflow state
        try:
            self._update_state(self.initial_step.output_mapping, initial_step_output)
        except WorkflowError as e:
            print(f"Error updating state for step {self.initial_step.name}: {str(e)}")
            raise

        for cycle in range(self.max_cycles):
            self.current_cycle = cycle
            print(f"\nStarting workflow cycle {cycle + 1}/{self.max_cycles}")

            for step in self.cycle_steps:
                print(f"\nExecuting step: {step.name}")

                # Map workflow state to worker input
                try:
                    context = self._map_state(step.input_mapping, self.state)
                except WorkflowError as e:
                    print(f"Error mapping state for step {step.name}: {str(e)}")
                    raise

                # Execute worker
                input_data = WorkerInput(context=context, parameters={"cycle": cycle})

                output = step.worker.execute(input_data)

                # Save output
                self._save_step_output(step, output)

                # Update workflow state
                try:
                    self._update_state(step.output_mapping, output)
                except WorkflowError as e:
                    print(f"Error updating state for step {step.name}: {str(e)}")
                    raise

        return self.state
