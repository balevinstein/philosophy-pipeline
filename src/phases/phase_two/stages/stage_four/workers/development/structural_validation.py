from typing import Dict, Any
from datetime import datetime

from src.phases.core.base_worker import WorkerInput, WorkerOutput
from src.phases.core.worker_types import DevelopmentWorker
from src.phases.phase_two.stages.stage_four.prompts.development.structural_validation_prompts import (
    StructuralValidationPrompt,
)


class StructuralValidationWorker(DevelopmentWorker):
    """
    Worker responsible for validating and finalizing the complete outline.
    
    This worker analyzes the logical flow from section to section, ensures key
    moves are properly sequenced and developed, validates word count allocations,
    and makes necessary adjustments to improve coherence and balance.
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.prompts = StructuralValidationPrompt()
        self.stage_name = "structural_validation"

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        """Construct the prompt for structural validation."""
        framework = input_data.context.get("framework", {})
        outline = input_data.context.get("outline", {})
        developed_key_moves = input_data.context.get("developed_key_moves", [])
        literature = input_data.context.get("literature", {})
        current_outline_development = input_data.context.get("current_outline_development")
        
        return self.prompts.get_prompt(
            framework=framework,
            initial_outline=outline,
            current_outline=current_outline_development,
            developed_key_moves=developed_key_moves,
            literature=literature,
        )

    def process_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Prepare input for structural validation."""
        print("\nPreparing input for structural validation...")
        print("\nReceived state keys:", list(state.keys()))

        # Validate required inputs
        if "framework" not in state or "outline" not in state or "developed_key_moves" not in state:
            raise ValueError("Missing required state: framework, outline, developed_key_moves")
        
        # Get current development - this should include all previous phases
        current_outline_development = state.get("current_outline_development")
        if current_outline_development:
            print(f"Found current outline development of type: {type(current_outline_development)}")
        else:
            print(f"Warning: No current outline development found - structural validation may be less effective.")
        
        return WorkerInput(
            context={
                "framework": state["framework"],
                "outline": state["outline"],
                "developed_key_moves": state["developed_key_moves"],
                "literature": state.get("literature", {}),
                "current_outline_development": current_outline_development,
            },
            parameters={
                "phase": "structural_validation",
            },
        )

    def process_output(self, raw_output: str) -> WorkerOutput:
        """Process the raw output from the worker."""
        print(f"\nProcessing structural validation output")
        
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
            sections = {"Final Validated Outline": core_content}
        
        # Create structured output
        modifications = {
            "core_content": core_content,
            "full_content": core_content,
            "timestamp": datetime.now().isoformat(),
            "sections": sections
        }
        
        # Create the worker output with the correct parameters
        output = WorkerOutput(
            modifications=modifications,
            notes={
                "section_count": len(sections)
            },
            status="completed"
        )
        
        return output

    def validate_output(self, output: WorkerOutput) -> bool:
        """Verify output meets requirements."""
        print("\nValidating structural validation output...")

        if not output.modifications:
            print("Failed: No modifications")
            return False

        content = output.modifications.get("core_content")
            
        if not content or not content.strip():
            print("Failed: No content")
            return False

        # Debug output
        print(f"\nOutput content (first 200 chars): {content[:200]}...")
        
        # Check for key structural validation elements
        required_elements = [
            # Check for section numbering
            lambda c: any(f"{i}." in c for i in range(1, 10)),
            # Check for key move references
            lambda c: "Key Move" in c or "key move" in c,
            # Check for word count allocations
            lambda c: any(kw in c.lower() for kw in ["word", "words", "count"])
        ]
        
        missing_elements = [i for i, check in enumerate(required_elements) if not check(content)]
        
        if missing_elements:
            print(f"Failed: Missing required elements {missing_elements}")
            return False
            
        # Check if we have sufficient content length - this should be the most comprehensive
        if len(content.strip()) > 2000:  # Require at least 2000 characters for final validation
            print("Content length validation passed")
            return True
        else:
            print("Failed: Content too short")
            return False 