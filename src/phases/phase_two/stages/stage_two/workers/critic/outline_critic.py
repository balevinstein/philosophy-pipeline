from typing import Dict, Any, List

from src.phases.core.base_worker import WorkerInput, WorkerOutput
from src.phases.core.worker_types import CriticWorker
from src.phases.phase_two.stages.stage_two.prompts.outline.outline_prompts import (
    OutlinePrompts,
)


class OutlineCriticWorker(CriticWorker):

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.prompts = OutlinePrompts()
        self.stage_name = "outline_critic"
        self._state = {"iterations": 0, "previous_critiques": []}

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        return self.prompts.get_critic_prompt(
            outline=input_data.context["current_outline"],
            framework=input_data.context["framework"],
            lit_readings=input_data.context.get("lit_readings"),
            lit_synthesis=input_data.context.get("lit_synthesis"),
            lit_narrative=input_data.context.get("lit_narrative"),
        )

    def _extract_red_flags(self, red_flags_text: str) -> List[str]:
        """Extract list of red flags from text"""
        flags = []
        for line in red_flags_text.split("\n"):
            if line.strip().startswith("-"):
                flags.append(line.strip()[1:].strip())
        return flags

    def process_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Map the input data to worker input"""

        if "current_outline" not in state or "framework" not in state:
            raise ValueError("Missing required state: outline and framework")

        return WorkerInput(
            context={
                "current_outline": state["current_outline"],
                "framework": state["framework"],
                "lit_readings": state.get("literature", {}).get("readings"),
                "lit_synthesis": state.get("literature", {}).get("synthesis"),
                "lit_narrative": state.get("literature", {}).get("narrative"),
            },
            parameters={"outline_state": state, "iteration": self._state["iterations"]},
        )

    def process_output(self, response: str) -> WorkerOutput:
        """Process response into structured output"""
        response = response.replace("```markdown", "").replace("```", "")
        try:
            # Split into sections
            sections = {}
            current_section = None
            current_content = []

            for line in response.split("\n"):
                if line.startswith("# "):
                    if current_section:
                        sections[current_section] = "\n".join(current_content).strip()
                    current_section = line[2:].strip()
                    current_content = []
                else:
                    current_content.append(line)

            if current_section:
                sections[current_section] = "\n".join(current_content).strip()

            # Extract summary assessment
            summary = self._extract_summary(sections.get("Summary Assessment", ""))

            # Extract red flags
            red_flags = self._extract_red_flags(sections.get("Red Flags", ""))

            # Update state
            self._state["iterations"] += 1
            self._state["previous_critiques"].append(
                {"sections": sections, "summary": summary, "red_flags": red_flags}
            )

            return WorkerOutput(
                modifications={
                    "content": response.strip(),
                    "sections": sections,
                    "summary": summary,
                    "red_flags": red_flags,
                    "iteration": self._state["iterations"],
                },
                notes={
                    "summary_assessment": summary,
                    "red_flags_count": len(red_flags),
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
        """Optional output validation"""
        print("\nValidating outline critique output...")

        if not output.modifications:
            print("Failed: No modifications")
            return False

        content = output.modifications.get("content")
        if not content:
            print("Failed: No content")
            return False

        # Check for required sections
        required_sections = [
            "Scratch Work",
            "Framework Alignment Analysis",
            "Structural Analysis",
            "Feasibility Assessment",
            "Literature Integration",
            "Red Flags",
            "Specific Recommendations",
            "Summary Assessment",
        ]

        missing_sections = [
            section for section in required_sections if f"# {section}" not in content
        ]
        if missing_sections:
            print(f"Failed: Missing sections: {missing_sections}")
            return False

        # Verify summary assessment is valid
        summary = content.split("# Summary Assessment")[-1].strip()
        valid_assessments = ["MAJOR REVISION", "MINOR REFINEMENT", "MINIMAL CHANGES"]
        if not any(assessment in summary for assessment in valid_assessments):
            print("Failed: Invalid or missing summary assessment")
            return False

        print("Validation passed!")
        return True
