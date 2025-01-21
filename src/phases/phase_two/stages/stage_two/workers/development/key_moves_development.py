from typing import Dict, Any

from src.phases.core.base_worker import WorkerInput, WorkerOutput
from src.phases.core.worker_types import DevelopmentWorker
from src.phases.phase_two.stages.stage_two.prompts.key_moves.key_moves_prompts import (
    KeyMovesPrompts,
)


class KeyMovesDevelopmentWorker(DevelopmentWorker):

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.prompts = KeyMovesPrompts()
        self.stage_name = "key_moves_development"
        self._state = {
            "iterations": 0,
            "current_move": None,
            "analyzed_moves": {},  # Store analysis results by move
            "development_phase": "argument",
        }

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        return self.prompts.get_development_argument_prompt(
            move=input_data.parameters["move"],
            abstract=input_data.context.get("abstract"),
            outline=input_data.context.get("outline"),
            prior_moves=self._state.get("analyzed_moves"),
        )

    def process_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Prepare input for key moves analysis"""
        print("\nPreparing input for key moves analysis...")
        print("\nReceived state keys:", list(state.keys()))

        if "framework" not in state or "outline" not in state:
            raise ValueError("Missing required state: framework and outline")

        # Get moves from framework
        moves = state["framework"].get("key_moves", [])
        if not moves:
            raise ValueError("No key moves found in framework")

        # Set current move if not already set
        if self._state["current_move"] is None and moves:
            self._state["current_move"] = moves[0]

        return WorkerInput(
            context={
                "framework": state["framework"],
                "outline": state["outline"],
                "lit_readings": state.get("literature", {}).get("readings"),
                "lit_synthesis": state.get("literature", {}).get("synthesis"),
                "lit_narrative": state.get("literature", {}).get("narrative"),
            },
            parameters={
                "outline_state": state,
                "phase": "key_moves_analysis",
                "move": self._state["current_move"],
            },
        )

    def process_output(self, response: str) -> WorkerOutput:
        """Process API response into structured output"""
        try:
            return WorkerOutput(
                modifications={"content": response.strip()},
                notes={
                    "move": self._state["current_move"],
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

    def validate_output(self, output: WorkerOutput) -> bool:
        """Verify output meets requirements"""
        print("\nValidating key moves output...")

        if not output.modifications:
            print("Failed: No modifications")
            return False

        content = output.modifications.get("content")
        if not content:
            print("Failed: No content")
            return False

        # Check for required sections
        required_sections = ["Scratch Work", "Final Argument Development"]

        sections = content.split("# ")
        section_titles = [s.split("\n")[0].strip() for s in sections if s]

        print("\nFound sections:", section_titles)
        print("Required sections:", required_sections)

        if not all(req in section_titles for req in required_sections):
            print("Failed: Missing required sections")
            return False

        print("Validation passed!")
        return True
