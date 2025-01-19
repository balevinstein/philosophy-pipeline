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
        self.stage_name = "abstract_critic"

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        return self.prompts.get_critic_prompt(
            abstract_framework=input_data.context["current_framework"],
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
                "current_framework": state.get(
                    "current_framework"
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
        """Verify output meets requirements"""
        if not output.modifications:
            return False

        content = output.modifications.get("content")
        if not content:
            return False

        # Check for required sections
        required_sections = [
            "Scratch Work",
            "Abstract Analysis",
            "Framework Components Analysis",
            "Validation Assessment",
            "Improvement Recommendations",
            "Summary Assessment",
        ]

        for section in required_sections:
            if f"# {section}" not in content:
                return False

        # Check Framework Components subsections
        if not all(
            subsection in content
            for subsection in [
                "## Main Thesis",
                "## Core Contribution",
                "## Key Moves",
                "## Development Notes",
            ]
        ):
            return False

        # Verify validation assessment completeness
        validation_items = [
            "Scope appropriate",
            "Clearly articulated",
            "Sufficiently original",
            "Feasibly developable",
        ]
        validation_section = content.split("# Validation Assessment")[1].split("#")[0]
        if not all(item in validation_section for item in validation_items):
            return False

        # Verify summary assessment is valid
        summary = content.split("# Summary Assessment")[-1].strip()
        valid_assessments = ["MAJOR REVISION", "MINOR REFINEMENT", "MINIMAL CHANGES"]
        if not any(assessment in summary for assessment in valid_assessments):
            return False

        return True

    # Critic Specific
    def extract_summary(self, summary_text: str) -> str:
        """Extract summary assessment from text"""
        for assessment in ["MAJOR REVISION", "MINOR REFINEMENT", "MINIMAL CHANGES"]:
            if assessment in summary_text:
                return assessment
        return "UNKNOWN"
