from typing import Dict, Any
from datetime import datetime

from src.phases.core.base_worker import WorkerInput, WorkerOutput
from src.phases.core.worker_types import DevelopmentWorker
from src.phases.phase_two.stages.stage_four.prompts.development.content_development_prompts import (
    ContentDevelopmentPrompt,
)


class ContentDevelopmentWorker(DevelopmentWorker):
    """
    Worker responsible for developing specific content guidance for each section.
    
    This worker analyzes the existing outline structure and literature mapping
    to create specific content guidance for each section, specifying what
    arguments should be made, which examples should be used, and how
    counterarguments should be addressed.
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.prompts = ContentDevelopmentPrompt()
        self.stage_name = "content_development"

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        """Construct the prompt for content development."""
        framework = input_data.context.get("framework", {})
        outline = input_data.context.get("outline", {})
        current_outline = input_data.context.get("current_outline_development", None)
        developed_key_moves = input_data.context.get("developed_key_moves", [])
        literature = input_data.context.get("literature", {})
        
        # DEBUG: Print framework structure
        print("\nDEBUG: Framework object contents:")
        print(f"Framework type: {type(framework)}")
        print(f"Framework keys: {list(framework.keys()) if isinstance(framework, dict) else 'Not a dict'}")
        if isinstance(framework, dict):
            print(f"Has main_thesis: {'main_thesis' in framework}")
            print(f"Has core_contribution: {'core_contribution' in framework}")
            if 'main_thesis' in framework:
                print(f"Main thesis value: {framework['main_thesis'][:50]}...")
            if 'core_contribution' in framework:
                print(f"Core contribution value: {framework['core_contribution'][:50]}...")
            # Check if main_thesis is nested inside abstract_framework key
            if 'abstract_framework' in framework and isinstance(framework['abstract_framework'], dict):
                af = framework['abstract_framework']
                print(f"Abstract framework contains main_thesis: {'main_thesis' in af}")
                print(f"Abstract framework contains core_contribution: {'core_contribution' in af}")
        
        return self.prompts.get_prompt(
            framework=framework,
            initial_outline=outline,
            current_outline=current_outline,
            developed_key_moves=developed_key_moves,
            literature=literature,
        )

    def process_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Prepare input for content development."""
        print("\nPreparing input for content development...")
        print("\nReceived state keys:", list(state.keys()))

        # Validate required inputs
        if "framework" not in state or "outline" not in state or "developed_key_moves" not in state:
            raise ValueError("Missing required state: framework, outline, developed_key_moves")
        
        return WorkerInput(
            context={
                "framework": state["framework"],
                "outline": state["outline"],
                "developed_key_moves": state["developed_key_moves"],
                "literature": state.get("literature", {}),
                "current_outline_development": state.get("current_outline_development", None),
                "development_phase": state.get("development_phase", "content_development"),
            },
            parameters={
                "phase": "content_development",
            },
        )

    def process_output(self, raw_output: str) -> WorkerOutput:
        """Process the raw output from the content development worker."""
        print(f"\nProcessing content development output")
        
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
            sections = {"Complete Content Guidance": core_content}
        
        # Create structured output
        modifications = {
            "core_content": core_content,
            "full_content": core_content,
            "content_development": core_content,  # Store for later phases
            "timestamp": datetime.now().isoformat(),
            "sections": sections
        }
        
        return WorkerOutput(modifications=modifications)

    def validate_output(self, output: WorkerOutput) -> bool:
        """Verify output meets requirements."""
        print("\nValidating content development output...")

        if not output.modifications:
            print("Failed: No modifications")
            return False

        content = output.modifications.get("core_content")
            
        if not content or not content.strip():
            print("Failed: No content")
            return False

        # Debug output
        print(f"\nOutput content (first 200 chars): {content[:200]}...")
        
        # Check for key content development elements
        required_elements = [
            # Check for section references
            lambda c: any(f"Section" in c or f"{i}." in c for i in range(1, 10)),
            # Check for key move references
            lambda c: "Key Move" in c or "key move" in c,
            # Check for bullet points
            lambda c: "•" in c or "* " in c or "- " in c
        ]
        
        missing_elements = [i for i, check in enumerate(required_elements) if not check(content)]
        
        if missing_elements:
            print(f"Failed: Missing required elements {missing_elements}")
            return False
            
        # Check if we have sufficient content length
        if len(content.strip()) > 1500:  # Require at least 1500 characters for content guidance
            print("Content length validation passed")
            return True
        else:
            print("Failed: Content too short")
            return False 