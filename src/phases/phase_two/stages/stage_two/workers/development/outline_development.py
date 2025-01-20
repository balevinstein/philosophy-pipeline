from typing import Dict, Any

from src.phases.core.base_worker import WorkerInput, WorkerOutput

from src.phases.core.worker_types import DevelopmentWorker
from src.phases.phase_two.stages.stage_two.prompts.outline.outline_prompts import (
    OutlinePrompts,
)


class OutlineDevelopmentWorker(DevelopmentWorker):

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.prompts = OutlinePrompts()
        self.stage_name = "outline_development"
        self._state = {"iterations": 0, "previous_critiques": []}

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        return self.prompts.get_development_prompt(
            abstract=input_data.context["abstract"],
            main_thesis=input_data.context["main_thesis"],
            core_contribution=input_data.context["core_contribution"],
            key_moves=input_data.context["key_moves"],
        )

    # TODO: STATE_EXCHANGE
    def process_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Prepare input for outline development"""
        framework = state.get("framework", {})
        if not framework:
            raise ValueError("Missing framework information")

        return WorkerInput(
            context={
                "abstract": framework.get("abstract"),
                "main_thesis": framework.get("main_thesis"),
                "core_contribution": framework.get("core_contribution"),
                "key_moves": framework.get("key_moves"),
                "lit_readings": state.get("literature", {}).get("readings"),
                "lit_synthesis": state.get("literature", {}).get("synthesis"),
                "lit_narrative": state.get("literature", {}).get("narrative"),
            },
            parameters={"outline_state": state, "phase": "outline_development"},
        )

    def process_output(self, response: str) -> WorkerOutput:
        """Process response into structured output"""
        response = response.replace("```markdown", "").replace("```", "")

        try:
            # Split into sections based on markdown headers
            sections = response.split("\n# ")
            outline_content = None
            scratch_work = None
            development_notes = None

            for section in sections:
                if section.startswith("Scratch Work"):
                    scratch_work = section.strip()
                elif section.startswith("Final Outline"):
                    outline_content = section.strip()
                elif section.startswith("Development Notes"):
                    development_notes = section.strip()

            if not outline_content:
                raise ValueError("Missing outline content")

            # Update state
            self._state["iterations"] += 1
            self._state["current_outline"] = outline_content

            return WorkerOutput(
                modifications={
                    "current_outline": outline_content,
                    "development_notes": development_notes,
                    "scratch_work": scratch_work,
                },
                notes={"iteration": self._state["iterations"]},
                status="completed",
            )

        except Exception as e:
            return WorkerOutput(
                modifications={},
                notes={"error": f"Failed to process response: {str(e)}"},
                status="failed",
            )

    def validate_output(self, output: WorkerOutput) -> bool:
        """Verify output meets basic structural requirements"""
        print("\nValidating outline output...")

        if not output.modifications:
            print("Failed: No modifications")
            return False

        outline = output.modifications.get("current_outline")
        if not outline:
            print("Failed: No outline")
            return False

        # Check for required sections
        lines = outline.split("\n")
        has_intro = False
        has_conclusion = False
        section_count = 0

        print("\nChecking sections:")
        for line in lines:
            if line.startswith("## "):  # Main sections
                section_count += 1
                print(f"Found section: {line}")
                if "introduction" in line.lower():
                    has_intro = True
                elif "conclusion" in line.lower():
                    has_conclusion = True

        print(f"\nSection count: {section_count}")
        print(f"Has intro: {has_intro}")
        print(f"Has conclusion: {has_conclusion}")

        # Validate basic structure
        if not (has_intro and has_conclusion):
            print("Failed: Missing introduction or conclusion")
            return False

        # Check reasonable section count (4-7 typical)
        if not 3 <= section_count <= 8:
            print(f"Failed: Section count {section_count} outside valid range (3-8)")
            return False

        print("Validation passed!")
        return True
