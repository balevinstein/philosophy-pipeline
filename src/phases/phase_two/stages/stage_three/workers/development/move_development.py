from typing import Dict, Any
from datetime import datetime

from src.phases.core.base_worker import WorkerInput, WorkerOutput
from src.phases.core.worker_types import DevelopmentWorker
from src.phases.phase_two.stages.stage_three.prompts.development.development_prompts import (
    MoveDevelopmentPrompts,
)


class MoveDevelopmentWorker(DevelopmentWorker):
    """
    Worker responsible for developing a single key move in detail.

    This worker takes a key move and develops it with detailed arguments,
    examples, literature connections, and addresses potential challenges.
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.prompts = MoveDevelopmentPrompts()
        self.stage_name = "move_development"
        self._state = {
            "iterations": 0,
            "development_phase": "initial",  # Start with the initial phase
        }

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        """Construct the appropriate prompt based on the development phase."""
        move_index = input_data.parameters.get("move_index", 0)
        move = input_data.parameters.get("move", "")
        framework = input_data.context.get("framework", {})
        outline = input_data.context.get("outline", {})
        current_move_development = input_data.context.get("current_move_development")

        # Get development phase from input parameters
        development_phase = input_data.parameters.get(
            "development_phase", self._state["development_phase"]
        )

        print(f"Constructing prompt for development phase: {development_phase}")

        # Determine which prompt to use based on the development phase
        if development_phase == "initial":
            return self.prompts.get_initial_development_prompt(
                move=move,
                framework=framework,
                outline=outline,
                literature=input_data.context.get("literature", {}),
                move_index=move_index,
            )
        elif development_phase == "examples":
            return self.prompts.get_examples_development_prompt(
                move=move,
                current_development=current_move_development,
                framework=framework,
                outline=outline,
                literature=input_data.context.get("literature", {}),
            )
        elif development_phase == "literature":
            return self.prompts.get_literature_integration_prompt(
                move=move,
                current_development=current_move_development,
                framework=framework,
                outline=outline,
                literature=input_data.context.get("literature", {}),
            )
        else:
            # Default to initial development
            return self.prompts.get_initial_development_prompt(
                move=move,
                framework=framework,
                outline=outline,
                literature=input_data.context.get("literature", {}),
                move_index=move_index,
            )

    def process_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Prepare input for key move development."""
        print("\nPreparing input for key move development...")
        print("\nReceived state keys:", list(state.keys()))

        if (
            "framework" not in state
            or "outline" not in state
            or "key_moves" not in state
        ):
            raise ValueError("Missing required state: framework, outline, key_moves")

        move_index = state.get("move_index", 0)

        # Get the development phase from input if available
        if "development_phase" in state:
            self._state["development_phase"] = state["development_phase"]
            print(f"Setting development phase to: {self._state['development_phase']}")

        # Get current development if available, but don't require it
        current_move_development = state.get("current_move_development")
        if current_move_development:
            print(
                f"Found current move development of type: {type(current_move_development)}"
            )
        else:
            print(
                f"No current move development found - this is normal for initial phase. {move_index}"
            )

        # Get the specific move we're working on
        framework = state["framework"]
        moves_list = framework.get("key_moves", [])
        if move_index >= len(moves_list):
            raise ValueError(
                f"Invalid move index: {move_index}, only {len(moves_list)} moves available"
            )

        current_move = moves_list[move_index]
        print(f"Processing move {move_index+1}: {current_move}")

        return WorkerInput(
            context={
                "framework": state["framework"],
                "outline": state["outline"],
                "key_moves": state["key_moves"],
                "literature": state.get("literature", {}),
                "current_move_development": current_move_development,  # May be None for initial phase
            },
            parameters={
                "move_index": move_index,
                "phase": "move_development",
                "development_phase": self._state["development_phase"],
                "move": current_move,  # Pass the actual move text
            },
        )

    def process_output(self, response: str) -> WorkerOutput:
        """Process the raw output from the worker."""
        print(
            f"\nProcessing move development output for phase: {self._state.get('development_phase', 'initial')}"
        )

        # Extract the core content from the raw output
        core_content = response.strip()

        # Create a basic sections dictionary with the full content
        sections = {"Content": core_content}

        # Create structured output
        modifications = {
            "core_content": core_content,
            "full_content": core_content,  # For now, these are the same
            "move_name": self._state.get("move_name", "Untitled Move"),
            "development_phase": self._state.get("development_phase", "initial"),
            "timestamp": datetime.now().isoformat(),
            "sections": sections,  # Add the sections dictionary
        }

        # Create the worker output with the correct parameters
        output = WorkerOutput(
            modifications=modifications,
            notes={
                "development_phase": self._state.get("development_phase", "initial"),
                "move_name": self._state.get("move_name", "Untitled Move"),
            },
            status="completed",
        )

        return output

    def validate_output(self, output: WorkerOutput) -> bool:
        """Verify output meets requirements."""
        print("\nValidating key move development output...")

        if not output.modifications:
            print("Failed: No modifications")
            return False

        # Check for content in different possible locations
        content = None
        if "core_content" in output.modifications:
            content = output.modifications["core_content"]
        elif "full_content" in output.modifications:
            content = output.modifications["full_content"]

        if not content or not content.strip():
            print("Failed: No content")
            return False

        # Debug output to see what we're getting
        print(f"\nOutput content (first 200 chars): {content[:200]}...")

        # Check if we have sufficient content length - a basic check for all phases
        if len(content.strip()) > 500:  # Require at least 500 characters
            print("Content length validation passed")
            return True
        else:
            print("Failed: Content too short")
            return False
