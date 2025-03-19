from typing import Dict, Any
from datetime import datetime

from src.phases.core.base_worker import WorkerInput, WorkerOutput
from src.phases.core.worker_types import DevelopmentWorker
from src.phases.phase_two.stages.stage_four.prompts.development.development_prompts import (
    OutlineDevelopmentPrompts,
)


class OutlineDevelopmentWorker(DevelopmentWorker):
    """
    Worker responsible for developing a detailed outline for the paper.
    
    This worker takes the initial outline from Phase II.2 and the fully developed
    key moves from Phase II.3 and creates a comprehensive, detailed outline
    that will guide the actual writing in Phase III.
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.prompts = OutlineDevelopmentPrompts()
        self.stage_name = "detailed_outline_development"
        self._state = {
            "iterations": 0,
            "development_phase": "structure",  # Start with the structure phase
        }

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        """Construct the appropriate prompt based on the development phase."""
        framework = input_data.context.get("framework", {})
        outline = input_data.context.get("outline", {})
        developed_key_moves = input_data.context.get("developed_key_moves", [])
        current_outline_development = input_data.context.get("current_outline_development")
        
        # Get development phase from input parameters
        development_phase = input_data.parameters.get("development_phase", self._state["development_phase"])
        
        print(f"Constructing prompt for development phase: {development_phase}")
        
        # Determine which prompt to use based on the development phase
        if development_phase == "structure":
            return self.prompts.get_structure_development_prompt(
                framework=framework,
                initial_outline=outline,
                developed_key_moves=developed_key_moves,
                literature=input_data.context.get("literature", {}),
            )
        elif development_phase == "content":
            return self.prompts.get_content_development_prompt(
                framework=framework,
                initial_outline=outline,
                current_outline=current_outline_development,
                developed_key_moves=developed_key_moves,
                literature=input_data.context.get("literature", {}),
            )
        elif development_phase == "transitions":
            return self.prompts.get_transitions_development_prompt(
                framework=framework,
                initial_outline=outline,
                current_outline=current_outline_development,
                developed_key_moves=developed_key_moves,
                literature=input_data.context.get("literature", {}),
            )
        else:
            # Default to structure development
            return self.prompts.get_structure_development_prompt(
                framework=framework,
                initial_outline=outline,
                developed_key_moves=developed_key_moves,
                literature=input_data.context.get("literature", {}),
            )

    def process_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Prepare input for detailed outline development."""
        print("\nPreparing input for detailed outline development...")
        print("\nReceived state keys:", list(state.keys()))

        # Validate required inputs
        if "framework" not in state or "outline" not in state or "developed_key_moves" not in state:
            raise ValueError("Missing required state: framework, outline, developed_key_moves")
        
        # Get the development phase from input if available
        if "development_phase" in state:
            self._state["development_phase"] = state["development_phase"]
            print(f"Setting development phase to: {self._state['development_phase']}")
        
        # Get current development if available, but don't require it
        current_outline_development = state.get("current_outline_development")
        if current_outline_development:
            print(f"Found current outline development of type: {type(current_outline_development)}")
        else:
            print(f"No current outline development found - this is normal for initial phase.")
        
        return WorkerInput(
            context={
                "framework": state["framework"],
                "outline": state["outline"],
                "developed_key_moves": state["developed_key_moves"],
                "literature": state.get("literature", {}),
                "current_outline_development": current_outline_development,  # May be None for initial phase
            },
            parameters={
                "phase": "outline_development",
                "development_phase": self._state["development_phase"],
            },
        )

    def process_output(self, raw_output: str) -> WorkerOutput:
        """Process the raw output from the worker."""
        print(f"\nProcessing outline development output for phase: {self._state.get('development_phase', 'structure')}")
        
        # Extract the core content from the raw output
        core_content = raw_output.strip()
        
        # Attempt to split into sections if headings exist
        sections = {}
        current_section = None
        current_content = []
        section_markers = ["# ", "## "]  # Look for both H1 and H2 headings

        for line in raw_output.split("\n"):
            is_section_header = False
            for marker in section_markers:
                if line.startswith(marker):
                    if current_section:
                        sections[current_section] = "\n".join(current_content).strip()
                    current_section = line[len(marker):].strip()
                    current_content = []
                    is_section_header = True
                    break
            
            if not is_section_header and current_section is not None:
                current_content.append(line)

        if current_section:
            sections[current_section] = "\n".join(current_content).strip()
        
        # If we couldn't find any sections, use the entire content as one section
        if not sections:
            sections = {"Complete Outline": core_content}
        
        # Create structured output
        modifications = {
            "core_content": core_content,
            "full_content": core_content,
            "development_phase": self._state.get("development_phase", "structure"),
            "timestamp": datetime.now().isoformat(),
            "sections": sections
        }
        
        # Create the worker output with the correct parameters
        output = WorkerOutput(
            modifications=modifications,
            notes={
                "development_phase": self._state.get("development_phase", "structure"),
                "section_count": len(sections)
            },
            status="completed"
        )
        
        return output

    def validate_output(self, output: WorkerOutput) -> bool:
        """Verify output meets requirements."""
        print("\nValidating detailed outline development output...")

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