from typing import Dict, Any

from src.phases.core.base_worker import WorkerInput, WorkerOutput
from src.phases.core.worker_types import CriticWorker
from src.phases.phase_two.stages.stage_two.prompts.abstract.abstract_prompts import (
    AbstractPrompts,
)


class AbstractCriticWorker(CriticWorker):

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.prompts = AbstractPrompts()
        self._state = {"iterations": 0, "previous_critiques": []}
        self.stage_name = "abstract-critic"

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        return self.prompts.get_critic_prompt(
            abstract_framework=input_data.context["abstract_framework"],
            lit_readings=input_data.context["lit_readings"],
            lit_synthesis=input_data.context["lit_synthesis"],
            lit_narrative=input_data.context["lit_narrative"],
        )

    def _extract_framework_analysis(self, response: str) -> Dict[str, str]:
        """Extract analysis of framework components"""
        try:
            framework_section = response.split("# Framework Components Analysis")[
                1
            ].split("#")[0]
            components = {}

            for component in [
                "Main Thesis",
                "Core Contribution",
                "Key Moves",
                "Development Notes",
            ]:
                if f"## {component}" in framework_section:
                    component_content = framework_section.split(f"## {component}")[1]
                    component_content = (
                        component_content.split("##")[0]
                        if "##" in component_content
                        else component_content
                    )
                    components[component.lower().replace(" ", "_")] = (
                        component_content.strip()
                    )

            return components
        except Exception as e:
            return str(e)

    def process_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Prepare input for critique"""
        return WorkerInput(
            context={
                "abstract_framework": state.get(
                    "abstract_framework"
                ),  # Changed from "current_abstract"
                "lit_readings": state.get("literature", {}).get("readings"),
                "lit_synthesis": state.get("literature", {}).get("synthesis"),
                "lit_narrative": state.get("literature", {}).get("narrative"),
            },
            parameters={"outline_state": state, "iteration": self._state["iterations"]},
        )

    def process_output(self, response: str) -> WorkerOutput:
        """Process response into structured output"""
        try:
            # Update state
            self._state["iterations"] += 1
            self._state["previous_critiques"].append(response)

            # Extract validation assessment
            validation_section = response.split("# Validation Assessment")[1].split(
                "#"
            )[0]
            validation_results = {
                "scope_appropriate": "yes" in validation_section.lower(),
                "clearly_articulated": "yes" in validation_section.lower(),
                "sufficiently_original": "yes" in validation_section.lower(),
                "feasibly_developable": "yes" in validation_section.lower(),
            }

            # Extract summary assessment
            summary = self.extract_summary(response)

            return WorkerOutput(
                modifications={
                    "content": response.strip(),
                    "validation_results": validation_results,
                    "framework_analysis": self._extract_framework_analysis(response),
                    "iteration": self._state["iterations"],
                },
                notes={
                    "summary_assessment": summary,
                    "validation_status": validation_results,
                },
                status="completed",
            )

        except Exception as e:
            return WorkerOutput(
                modifications={},
                notes={"error": f"Failed to process response: {str(e)}"},
                status="failed",
            )

    def validate_output(self, output: WorkerOutput) -> bool:
        if output.status == "failed":
            return False

        required_fields = ["abstract", "framework"]
        return all(field in output.result for field in required_fields)

    # Critic Specific
    def extract_summary(self, summary_text: str) -> str:
        """Extract summary assessment from text"""
        for assessment in ["MAJOR REVISION", "MINOR REFINEMENT", "MINIMAL CHANGES"]:
            if assessment in summary_text:
                return assessment
        return "UNKNOWN"
