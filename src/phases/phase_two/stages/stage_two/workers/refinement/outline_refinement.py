from typing import Dict, Any, List

from src.phases.core.base_worker import WorkerInput, WorkerOutput

from src.phases.core.worker_types import RefinementWorker
from src.phases.phase_two.stages.stage_two.prompts.outline.outline_prompts import (
    OutlinePrompts,
)


class OutlineRefinementWorker(RefinementWorker):

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.prompts = OutlinePrompts()
        self.stage_name = "outline_refinement"
        self._state = {"iterations": 0, "previous_critiques": []}

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        """Construct refinement prompt"""
        return self.prompts.get_refinement_prompt(
            outline=input_data.context["current_outline"],
            critique=input_data.context["current_critique"],
            framework=input_data.context["framework"],
            lit_synthesis=input_data.context.get("lit_synthesis"),
        )

    # TODO: NOT_USED
    def _extract_decisions(self, decisions_text: str) -> Dict[str, List[str]]:
        """Extract implementation decisions"""
        decisions = {"will_implement": [], "wont_implement": []}

        current_section = None
        for line in decisions_text.split("\n"):
            if line.startswith("## Will Implement"):
                current_section = "will_implement"
            elif line.startswith("## Won't Implement"):
                current_section = "wont_implement"
            elif line.strip().startswith("-") and current_section:
                decisions[current_section].append(line.strip()[1:].strip())

        return decisions

    def process_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Prepare input for refinement"""
        if (
            "current_outline" not in state
            or "current_critique" not in state
            or "framework" not in state
        ):
            raise ValueError("Missing required state: outline, critique, and framework")

        return WorkerInput(
            context={
                "current_outline": state["current_outline"],
                "current_critique": state["current_critique"],
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

            # Get decisions from the Refinement Decisions section
            decisions = {"will_implement": [], "wont_implement": []}

            refinement_section = sections.get("Refinement Decisions", "")
            if "## Will Implement" in refinement_section:
                will_implement = refinement_section.split("## Will Implement")[1]
                will_implement = will_implement.split("## Won't Implement")[0]
                decisions["will_implement"] = [
                    line.strip()[2:].strip()
                    for line in will_implement.split("\n")
                    if line.strip().startswith("1.")
                ]

            if "## Won't Implement" in refinement_section:
                wont_implement = refinement_section.split("## Won't Implement")[1]
                decisions["wont_implement"] = [
                    line.strip()[2:].strip()
                    for line in wont_implement.split("\n")
                    if line.strip().startswith("1.")
                ]

            return WorkerOutput(
                modifications={
                    "content": response.strip(),
                    "sections": sections,
                    "outline": sections.get("Updated Outline", ""),
                    "decisions": decisions,
                    "iteration": self._state["iterations"],
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
        """Verify output meets requirements"""
        print("\nValidating outline refinement output...")

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
            "Framework Support Analysis",
            "Refinement Decisions",
            "Updated Outline",
            "Change Notes",
        ]

        missing_sections = [
            section for section in required_sections if f"# {section}" not in content
        ]
        if missing_sections:
            print(f"Failed: Missing sections: {missing_sections}")
            return False

        # Verify Refinement Decisions subsections
        try:
            refinement_section = content.split("# Refinement Decisions")[1]
            refinement_section = refinement_section.split("# Updated Outline")[0]

            if not (
                "## Will Implement" in refinement_section
                and "## Won't Implement" in refinement_section
            ):
                print("Failed: Missing required subsections")
                print("Looking for: '## Will Implement' and '## Won't Implement'")
                return False

        except Exception as e:
            print(f"Failed to validate refinement decisions: {str(e)}")
            return False

        print("Validation passed!")
        return True
