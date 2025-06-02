from typing import Dict, Any

from src.phases.core.base_worker import WorkerInput, WorkerOutput
from src.phases.core.worker_types import CriticWorker
from src.phases.phase_two.stages.stage_two.prompts.key_moves.key_moves_prompts import (
    KeyMovesPrompts,
)


class KeyMovesCriticWorker(CriticWorker):

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.prompts = KeyMovesPrompts()
        self.stage_name = "key_moves_critic"
        self._state = {"iterations": 0, "previous_critiques": []}

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        return self.prompts.get_critic_prompt(
            current_moves=input_data.context["key_moves"],
            framework=input_data.context["framework"],
            outline=input_data.context["outline"],
            lit_readings=input_data.context.get("lit_readings"),
            lit_synthesis=input_data.context.get("lit_synthesis"),
            lit_narrative=input_data.context.get("lit_narrative"),
        )

    def process_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Map the input data to worker input"""
        print("\nPreparing input for key moves critique...")
        print("\nReceived state keys:", list(state.keys()))

        if "framework" not in state or "outline" not in state:
            raise ValueError("Missing required state: framework and outline")

        # Check for key moves data in different possible locations
        key_moves_data = state.get("key_moves_analysis")  # From initial worker
        if not key_moves_data:
            key_moves_data = state.get("current_moves")  # From refinement worker
        if not key_moves_data:
            raise ValueError("No key moves data found in state")

        return WorkerInput(
            context={
                "framework": state["framework"],
                "outline": state["outline"],
                "key_moves": key_moves_data,
                "lit_readings": state.get("literature", {}).get("readings"),
                "lit_synthesis": state.get("literature", {}).get("synthesis"),
                "lit_narrative": state.get("literature", {}).get("narrative"),
            },
            parameters={"outline_state": state, "iteration": self._state["iterations"]},
        )

    def process_output(self, response: str) -> WorkerOutput:
        """Process response into structured output"""
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

            # Extract key recommendations
            recommendations = []
            summary_text = sections.get("Summary Assessment", "")
            next_steps_idx = summary_text.find("Next steps:")
            if next_steps_idx != -1:
                next_steps = summary_text[next_steps_idx:].split("\n")[1:]
                recommendations = [
                    step[3:] for step in next_steps if step.startswith("1.")
                ]

            # Update state
            self._state["iterations"] += 1
            self._state["previous_critiques"].append(
                {
                    "sections": sections,
                    "summary": summary,
                    "recommendations": recommendations,
                }
            )

            return WorkerOutput(
                modifications={
                    "content": response.strip(),
                    "sections": sections,
                    "summary": summary,
                    "recommendations": recommendations,
                    "iteration": self._state["iterations"],
                },
                notes={
                    "summary_assessment": summary,
                    "key_recommendations": recommendations,
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
        print("\nValidating key moves critique output...")

        if not output.modifications:
            print("Failed: No modifications")
            return False

        content = output.modifications.get("content")
        if not content:
            print("Failed: No content")
            return False

        # We'll require some key sections but allow flexibility in others
        # Accept either "Summary Assessment" or "Summary Recommendation"
        required_sections = ["Scratch Work"]
        required_summary_sections = ["Summary Assessment", "Summary Recommendation"]

        sections = content.split("# ")
        section_titles = [s.split("\n")[0].strip() for s in sections if s]

        print("\nFound sections:", section_titles)
        print("Required sections:", required_sections)

        missing_sections = [
            section for section in required_sections if section not in section_titles
        ]
        if missing_sections:
            print(f"Failed: Missing required sections: {missing_sections}")
            return False

        # Check if we have at least one of the summary sections
        has_summary = any(section in section_titles for section in required_summary_sections)
        if not has_summary:
            print(f"Failed: Missing summary section. Need one of: {required_summary_sections}")
            return False

        # Verify we have a valid summary assessment
        summary = ""
        for section_name in required_summary_sections:
            if f"# {section_name}" in content:
                summary = content.split(f"# {section_name}")[-1].strip()
                break

        valid_assessments = ["MAJOR REVISION", "MINOR REFINEMENT", "MINIMAL CHANGES", 
                           "ACCEPT AS IS", "MAJOR REVISIONS", "MINOR REFINEMENTS", 
                           "FUNDAMENTAL REWORK"]
        if not any(assessment in summary for assessment in valid_assessments):
            print("Failed: Invalid or missing summary assessment")
            return False

        print("Validation passed!")
        return True
