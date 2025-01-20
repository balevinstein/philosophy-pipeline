# src/stages/phase_two/stages/stage_two/workers/abstract_critic.py

import json
from typing import Dict, Any

from src.phases.phase_two.base.framework import CriticWorker
from src.phases.phase_two.base.worker import WorkerInput
from src.phases.phase_two.stages.stage_two.prompts.abstract.abstract_prompts import (
    AbstractPrompts,
)


class AbstractCritic(CriticWorker):
    """Worker for critiquing abstract and suggesting improvements"""

    def __init__(self, config: Dict):
        super().__init__(config)
        self.prompts = AbstractPrompts()
        self.stage_name = "abstract_critic"
        self._state = {"iterations": 0, "previous_critiques": []}

    def evaluate(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate provided content"""
        # This implements the abstract method from CriticWorker
        # In our case, the actual evaluation happens in run(),
        # so this is just a wrapper
        result = self.run({"current_abstract": content})
        return result.modifications

    def get_state(self) -> Dict[str, Any]:
        """Get current worker state"""
        return self._state.copy()

    def prepare_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Prepare input for critique"""
        return WorkerInput(
            outline_state=state,
            context={
                "abstract_framework": state.get(
                    "abstract_framework"
                ),  # Changed from "current_abstract"
                "lit_readings": state.get("literature", {}).get("readings"),
                "lit_synthesis": state.get("literature", {}).get("synthesis"),
                "lit_narrative": state.get("literature", {}).get("narrative"),
            },
            task_specific={"iteration": self._state["iterations"]},
        )

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        """Construct critique prompt"""
        return self.prompts.get_critic_prompt(
            abstract_framework=input_data.context["abstract_framework"],
            lit_readings=input_data.context["lit_readings"],
            lit_synthesis=input_data.context["lit_synthesis"],
            lit_narrative=input_data.context["lit_narrative"],
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
                },
                status="completed",
            )

        except Exception as e:
            return WorkerOutput(
                modifications={},
                notes={"error": f"Failed to process response: {str(e)}"},
                status="failed",
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
        except:
            return {}

    def _extract_summary(self, response: str) -> str:
        """Extract summary assessment from response"""
        try:
            summary = response.split("# Summary Assessment")[-1].strip()
            for assessment in ["MAJOR REVISION", "MINOR REFINEMENT", "MINIMAL CHANGES"]:
                if assessment in summary:
                    return assessment
            return "UNKNOWN"
        except:
            return "UNKNOWN"
