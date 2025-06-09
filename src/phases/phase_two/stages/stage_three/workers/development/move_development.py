from typing import Dict, Any
from datetime import datetime

from src.phases.core.base_worker import WorkerInput, WorkerOutput
from src.phases.core.worker_types import DevelopmentWorker
from src.phases.phase_two.stages.stage_three.prompts.development.development_prompts import (
    MoveDevelopmentPrompts,
)
from src.utils.analysis_pdf_utils import enhance_development_prompt
from src.phases.core.exceptions import ValidationError


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
        self.selected_analysis_pdfs = []  # Store selected Analysis PDFs

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        """Construct the appropriate prompt based on the development phase."""
        move = input_data.parameters.get("move", "")
        framework = input_data.context.get("framework", {})
        outline = input_data.context.get("outline", {})
        literature = input_data.context.get("literature", {})
        move_index = input_data.parameters.get("move_index", 0)
        current_development = input_data.context.get("current_move_development")
        previously_developed_moves = input_data.context.get("previously_developed_moves", None)

        development_phase = self._state.get("development_phase", "initial")

        # Get base prompt depending on phase
        if development_phase == "examples":
            base_prompt = self.prompts.get_examples_development_prompt(
                move=move,
                current_development=current_development,
                framework=framework,
                outline=outline,
                literature=literature,
            )
        elif development_phase == "literature":
            base_prompt = self.prompts.get_literature_integration_prompt(
                move=move,
                current_development=current_development,
                framework=framework,
                outline=outline,
                literature=literature,
            )
        else:
            # Default to initial development
            base_prompt = self.prompts.get_initial_development_prompt(
                move=move,
                framework=framework,
                outline=outline,
                literature=literature,
                move_index=move_index,
                previously_developed_moves=previously_developed_moves,
            )

        # Create phase-specific identifier for Analysis PDF selection
        phase_identifier = f"key moves development ({development_phase})"

        # Enhance with Analysis patterns (phase-aware PDF selection)
        enhanced_prompt, analysis_pdfs = enhance_development_prompt(
            base_prompt, phase_identifier
        )
        
        # Store selected PDFs for API call
        self.selected_analysis_pdfs = analysis_pdfs
        
        if analysis_pdfs:
            print(f"Including {len(analysis_pdfs)} Analysis papers for {phase_identifier} guidance")
        
        return enhanced_prompt

    def execute(self, state: Dict[str, Any]) -> WorkerOutput:
        """Execute with Analysis PDF support"""
        input_data = self.process_input(state)
        
        # Get system prompt if available
        system_prompt = self.get_system_prompt()
        
        # Construct prompt first - this triggers Analysis PDF selection
        prompt = self._construct_prompt(input_data)
        
        # Make API call with Analysis PDFs if available
        if self.selected_analysis_pdfs:
            response, duration = self.api_handler.make_api_call(
                stage=self.stage_name,
                prompt=prompt,
                text_paths=self.selected_analysis_pdfs,  # Changed from pdf_paths to text_paths
                system_prompt=system_prompt
            )
        else:
            response, duration = self.api_handler.make_api_call(
                stage=self.stage_name,
                prompt=prompt,
                system_prompt=system_prompt
            )
            
        output = self.process_output(response)
        if not self.validate_output(output):
            print(response)
            raise ValidationError("Worker output failed validation: ", self.stage_name)
        return output

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

        # Get previously developed moves if available
        previously_developed_moves = state.get("previously_developed_moves", None)
        if previously_developed_moves:
            print(f"Found {len(previously_developed_moves)} previously developed moves for context")

        return WorkerInput(
            context={
                "framework": state["framework"],
                "outline": state["outline"],
                "key_moves": state["key_moves"],
                "literature": state.get("literature", {}),
                "current_move_development": current_move_development,  # May be None for initial phase
                "previously_developed_moves": previously_developed_moves,  # Add this for inter-move awareness
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
        """Validate the key move development output."""
        if output.status != "completed":
            return False

        content = output.modifications.get("core_content", "")
        if not content or len(content) < 100:
            print(f"Warning: Very short key move development ({len(content)} chars)")
            return False

        print(f"Key move development validation passed! Content: {len(content)} chars")
        return True
