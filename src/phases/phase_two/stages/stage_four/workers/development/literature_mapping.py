from typing import Dict, Any
from datetime import datetime

from src.phases.core.base_worker import WorkerInput, WorkerOutput
from src.phases.core.worker_types import DevelopmentWorker
from src.phases.phase_two.stages.stage_four.prompts.development.literature_mapping_prompts import (
    LiteratureMappingPrompt,
)


class LiteratureMappingWorker(DevelopmentWorker):
    """
    Worker responsible for mapping literature to outline sections.
    
    This worker identifies which literature from phase II.1 should be used in each
    section, specifies how each source should be engaged, and ensures comprehensive
    coverage of relevant sources.
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.prompts = LiteratureMappingPrompt()
        self.stage_name = "literature_mapping"

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        """Construct the prompt for literature mapping."""
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
        """Prepare input for literature mapping."""
        print("\nPreparing input for literature mapping...")
        print("\nReceived state keys:", list(state.keys()))

        # Validate required inputs
        if "framework" not in state or "outline" not in state or "developed_key_moves" not in state:
            raise ValueError("Missing required state: framework, outline, developed_key_moves")
        
        # Get current development - this should be the output of the framework integration phase
        current_outline_development = state.get("current_outline_development")
        if current_outline_development:
            print(f"Found current outline development of type: {type(current_outline_development)}")
        else:
            print(f"Warning: No current outline development found - literature mapping may be less effective.")
        
        return WorkerInput(
            context={
                "framework": state["framework"],
                "outline": state["outline"],
                "developed_key_moves": state["developed_key_moves"],
                "literature": state.get("literature", {}),
                "current_outline_development": current_outline_development,
            },
            parameters={
                "phase": "literature_mapping",
            },
        )

    def process_output(self, raw_output: str) -> WorkerOutput:
        """Process the raw output from the worker."""
        print(f"\nProcessing literature mapping output")
        
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
            sections = {"Literature Mapping": core_content}
        
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
        print("\nValidating literature mapping output...")

        if not output.modifications:
            print("Failed: No modifications")
            return False

        content = output.modifications.get("core_content")
            
        if not content or not content.strip():
            print("Failed: No content")
            return False

        # Debug output
        print(f"\nOutput content (first 200 chars): {content[:200]}...")
        
        # Check for key literature mapping elements
        required_elements = [
            # Check for section references
            lambda c: any(f"Section" in c or f"{i}." in c for i in range(1, 10)),
            # Check for literature references 
            lambda c: any(kw in c.lower() for kw in ["literature", "source", "reference", "citation"]),
            # Check for engagement types
            lambda c: any(kw in c.lower() for kw in ["supporting", "contrasting", "extending", "primary", "secondary"])
        ]
        
        missing_elements = [i for i, check in enumerate(required_elements) if not check(content)]
        
        if missing_elements:
            print(f"Failed: Missing required elements {missing_elements}")
            return False
            
        # Check if we have sufficient content length
        if len(content.strip()) > 1000:  # Require at least 1000 characters
            print("Content length validation passed")
            return True
        else:
            print("Failed: Content too short")
            return False 