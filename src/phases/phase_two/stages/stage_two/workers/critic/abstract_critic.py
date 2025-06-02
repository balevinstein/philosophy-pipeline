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

            # Check which format we're dealing with
            is_new_format = "# Skeptical Friend Analysis" in response

            if is_new_format:
                # For new format, extract key information differently
                validation_results = {
                    "scope_appropriate": "feasible" in response.lower(),
                    "clearly_articulated": "clear" in response.lower() and "vague" not in response.lower(),
                    "sufficiently_original": True,  # New format doesn't explicitly check this
                    "feasibly_developable": "feasible" in response.lower(),
                }
                
                # Extract summary assessment
                summary = self._extract_summary(response)
                
                # Extract most damaging flaw
                most_damaging = ""
                if "MOST DAMAGING FLAW" in response:
                    most_damaging = response.split("MOST DAMAGING FLAW")[1].split("\n")[0].strip()
                
                return WorkerOutput(
                    modifications={
                        "content": response.strip(),
                        "validation_results": validation_results,
                        "most_damaging_flaw": most_damaging,
                        "iteration": self._state["iterations"],
                    },
                    notes={
                        "summary_assessment": summary,
                        "validation_status": validation_results,
                        "format": "skeptical_friend",
                    },
                    status="completed",
                )
            else:
                # Original format processing
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
                summary = self._extract_summary(response)

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
                        "format": "original",
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

        # Check for required sections (either old format OR new skeptical friend format)
        old_format_sections = [
            "Scratch Work",
            "Abstract Analysis",
            "Framework Components Analysis",
            "Validation Assessment",
            "Improvement Recommendations",
            "Summary Assessment",
        ]

        new_format_sections = [
            "Skeptical Friend Analysis",
            "Abstract Claim Isolation",
            "Pattern Detection Results",
            "Framework Alignment Issues",
            "Summary Assessment",
        ]

        # Check if we have either the old format or the new format
        has_old_format = all(f"# {section}" in content for section in old_format_sections)
        has_new_format = all(f"# {section}" in content or f"## {section}" in content for section in new_format_sections)

        if not (has_old_format or has_new_format):
            return False

        # If using old format, check Framework Components subsections
        if has_old_format and not all(
            subsection in content
            for subsection in [
                "## Main Thesis",
                "## Core Contribution",
                "## Key Moves",
                "## Development Notes",
            ]
        ):
            return False

        # Verify summary assessment is valid (works for both formats)
        summary = content.split("# Summary Assessment")[-1].strip()
        valid_assessments = ["MAJOR REVISION", "MINOR REFINEMENT", "MINIMAL CHANGES"]
        if not any(assessment in summary for assessment in valid_assessments):
            return False

        return True
