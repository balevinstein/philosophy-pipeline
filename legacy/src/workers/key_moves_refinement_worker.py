# src/stages/phase_two/stages/stage_two/workers/key_moves_refinement_worker.py

import json
from typing import Dict, Any, List

from src.phases.phase_two.stages.stage_two.prompts.key_moves.key_moves_prompts import (
    KeyMovesPrompts,
)
from ....base.framework import FrameworkWorker
from ....base.worker import WorkerInput, WorkerOutput


class KeyMovesRefinementWorker(FrameworkWorker):
    """Worker for refining key moves based on critique"""

    def __init__(self, config: Dict):
        super().__init__(config)
        self.prompts = KeyMovesPrompts()
        self.stage_name = "key_moves_refinement"
        self._state = {"iterations": 0, "refinement_history": []}

    def get_state(self) -> Dict[str, Any]:
        """Get current worker state"""
        return self._state.copy()

    def prepare_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Prepare input for refinement"""
        print("\nPreparing input for key moves refinement...")
        print("\nReceived state keys:", list(state.keys()))

        if "key_moves_analysis" not in state or "critique" not in state:
            raise ValueError("Missing required state: key_moves_analysis and critique")

        return WorkerInput(
            outline_state=state,
            context={
                "current_moves": state["key_moves_analysis"],
                "current_critique": state["critique"],
                "framework": state.get("framework", {}),
                "outline": state.get("outline", ""),
                "lit_readings": state.get("literature", {}).get("readings"),
                "lit_synthesis": state.get("literature", {}).get("synthesis"),
                "lit_narrative": state.get("literature", {}).get("narrative"),
            },
            task_specific={"iteration": self._state["iterations"]},
        )

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        """Construct refinement prompt"""
        return self.prompts.get_refinement_prompt(
            current_moves=input_data.context["current_moves"],
            critique=input_data.context["current_critique"],
            framework=input_data.context.get("framework"),
            outline=input_data.context.get("outline"),
            lit_synthesis=input_data.context.get("lit_synthesis"),
        )

    def validate_output(self, output: WorkerOutput) -> bool:
        """Verify output meets requirements"""
        print("\nValidating key moves refinement output...")

        if not output.modifications:
            print("Failed: No modifications")
            return False

        # Instead of working with raw content, let's use the processed sections
        sections = output.modifications.get("sections", {})
        print("\nProcessed sections:", list(sections.keys()))

        # Check for required main sections
        required_sections = [
            "Scratch Work",
            "Refinement Decisions",
            "Updated Move Development",
            "Change Notes",
        ]

        missing_sections = [
            section for section in required_sections if section not in sections
        ]
        if missing_sections:
            print(f"Failed: Missing sections: {missing_sections}")
            return False

        # Check Refinement Decisions structure
        refinement_section = sections.get("Refinement Decisions", {})
        print("\nRefinement section structure:", refinement_section.keys())

        if not isinstance(refinement_section, dict):
            print("Failed: Refinement Decisions not properly structured")
            return False

        if not (
            "Will Implement" in refinement_section
            and "Won't Implement" in refinement_section
        ):
            print("Failed: Missing required Will/Won't Implement subsections")
            return False

        print("Validation passed!")
        return True

    def _extract_decisions(
        self, decisions_section: Dict[str, str]
    ) -> Dict[str, List[dict]]:
        """Extract implementation decisions with rationales"""
        decisions = {"will_implement": [], "wont_implement": []}

        # Process Will Implement section
        will_implement = decisions_section.get("Will Implement", "")
        for line in will_implement.split("\n"):
            if line.strip() and line[0].isdigit():
                if "--" in line:
                    change, rationale = line.split("--", 1)
                    decisions["will_implement"].append(
                        {"change": change.strip(), "rationale": rationale.strip()}
                    )

        # Process Won't Implement section
        wont_implement = decisions_section.get("Won't Implement", "")
        for line in wont_implement.split("\n"):
            if line.strip() and line[0].isdigit():
                if "--" in line:
                    change, rationale = line.split("--", 1)
                    decisions["wont_implement"].append(
                        {"change": change.strip(), "rationale": rationale.strip()}
                    )

        return decisions

    def process_output(self, response: str) -> WorkerOutput:
        """Process response into structured output"""
        try:
            print("\nProcessing output...")
            # Split into sections
            sections = {}
            current_section = None
            current_subsection = None
            current_content = []

            for line in response.split("\n"):
                if line.startswith("# "):  # Main section
                    print(f"\nFound main section: {line}")
                    if current_section:
                        if current_subsection:
                            print(
                                f"Saving subsection {current_subsection} under {current_section}"
                            )
                            sections[current_section][current_subsection] = "\n".join(
                                current_content
                            ).strip()
                            current_subsection = None
                        else:
                            print(f"Saving section {current_section}")
                            sections[current_section] = "\n".join(
                                current_content
                            ).strip()
                    current_section = line[2:].strip()
                    current_content = []
                    if current_section == "Refinement Decisions":
                        print("Initializing Refinement Decisions as dict")
                        sections[current_section] = (
                            {}
                        )  # Initialize as dict for subsections
                elif (
                    line.startswith("## ") and current_section == "Refinement Decisions"
                ):  # Subsection
                    print(f"\nFound subsection: {line}")
                    if current_subsection:
                        print(f"Saving previous subsection {current_subsection}")
                        sections[current_section][current_subsection] = "\n".join(
                            current_content
                        ).strip()
                    current_subsection = line[3:].strip()
                    current_content = []
                else:
                    current_content.append(line)

            # Handle final section/subsection
            if current_section:
                if current_subsection:
                    print(
                        f"\nSaving final subsection {current_subsection} under {current_section}"
                    )
                    sections[current_section][current_subsection] = "\n".join(
                        current_content
                    ).strip()
                else:
                    print(f"\nSaving final section {current_section}")
                    sections[current_section] = "\n".join(current_content).strip()

            print("\nFinal sections structure:")
            print(json.dumps(sections, indent=2))

            # Extract decisions
            decisions = self._extract_decisions(
                sections.get("Refinement Decisions", {})
            )

            # Get updated moves
            updated_moves = sections.get("Updated Move Development", "")

            # Update state
            self._state["iterations"] += 1
            self._state["refinement_history"].append(
                {"sections": sections, "decisions": decisions}
            )

            return WorkerOutput(
                modifications={
                    "content": response.strip(),
                    "sections": sections,
                    "decisions": decisions,
                    "moves": updated_moves,
                    "iteration": self._state["iterations"],
                },
                notes={
                    "changes_implemented": len(decisions.get("will_implement", [])),
                    "changes_rejected": len(decisions.get("wont_implement", [])),
                    "iteration": self._state["iterations"],
                },
                status="completed",
            )

        except Exception as e:
            return WorkerOutput(
                modifications={},
                notes={"error": f"Failed to process response: {str(e)}"},
                status="failed",
            )
