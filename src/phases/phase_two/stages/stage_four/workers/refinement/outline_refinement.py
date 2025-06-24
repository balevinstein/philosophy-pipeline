from typing import Dict, Any, List
import re
from datetime import datetime

from src.phases.core.base_worker import WorkerInput, WorkerOutput
from src.phases.core.worker_types import RefinementWorker
from src.phases.phase_two.stages.stage_four.prompts.refinement.refinement_prompts import OutlineRefinementPrompts
from src.utils.api import APIHandler  # Add import for API handler


class OutlineRefinementWorker(RefinementWorker):
    """
    Worker responsible for refining detailed outline development.
    
    This worker implements improvements based on critique for the current
    development phase (framework_integration, literature_mapping, etc).
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.prompts = OutlineRefinementPrompts()
        self.stage_name = "detailed_outline_refinement"
        self._state = {
            "iterations": 0,
            "development_phase": "framework_integration",  # Default phase
        }
        self.api_handler = APIHandler(config)  # Initialize API handler

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the refinement worker to improve outline development."""
        print(f"\nRunning {self.stage_name} worker...")
        
        # Process input data
        input_data = self.process_input(state)
        
        # Construct prompt
        prompt = self._construct_prompt(input_data)
        
        # Execute LLM call
        raw_output = self._execute_llm_call(prompt)
        
        # Process output
        output = self.process_output(raw_output)
        
        # Validate output
        if not self.validate_output(output):
            raise ValueError(f"Output validation failed for {self.stage_name}")
        
        return output.modifications

    def _execute_llm_call(self, prompt: str) -> str:
        """Execute the LLM call with the given prompt."""
        print(f"\nExecuting LLM call for {self.stage_name} (phase: {self._state['development_phase']})...")
        
        # Use the API handler to make actual API calls
        # The config has a model configuration for detailed_outline_refinement
        model_stage = "detailed_outline_refinement"
        
        # API handler returns (response_text, duration) tuple, we only need the response text
        response_text, _ = self.api_handler.make_api_call(model_stage, prompt)
        return response_text

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        """Construct the appropriate refinement prompt based on the development phase."""
        current_outline_development = input_data.context.get("current_outline_development", "")
        critique = input_data.context.get("critique", {})
        framework = input_data.context.get("framework", {})
        developed_key_moves = input_data.context.get("developed_key_moves", [])
        previous_versions = input_data.context.get("previous_versions", [])
        
        # Get development phase from input parameters
        development_phase = input_data.parameters.get("development_phase", self._state["development_phase"])
        
        print(f"Constructing refinement prompt for development phase: {development_phase}")
        
        # Use the appropriate refinement prompt based on the development phase
        return self.prompts.get_refinement_prompt(
            outline_development=current_outline_development,
            critique=critique,
            framework=framework,
            developed_key_moves=developed_key_moves,
            development_phase=development_phase,
            previous_versions=previous_versions,
            iteration=self._state.get("iterations", 0)
        )

    def process_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Prepare input for outline refinement."""
        print("\nPreparing input for outline refinement...")
        print("Received state keys:", list(state.keys()))

        # Validate required inputs
        if "framework" not in state or "current_outline_development" not in state or "critique" not in state:
            raise ValueError("Missing required state: framework, current_outline_development, critique")
        
        # Get the development phase from state if available
        if "development_phase" in state:
            self._state["development_phase"] = state["development_phase"]
            print(f"Setting development phase to: {self._state['development_phase']}")
        
        # Increment iterations counter
        self._state["iterations"] += 1
        
        return WorkerInput(
            context={
                "framework": state["framework"],
                "developed_key_moves": state.get("developed_key_moves", []),
                "current_outline_development": state["current_outline_development"],
                "critique": state["critique"],
                "previous_versions": state.get("previous_versions", []),
            },
            parameters={
                "phase": "outline_refinement",
                "development_phase": self._state["development_phase"],
                "iteration": self._state["iterations"],
            },
        )

    def process_output(self, raw_output: str) -> WorkerOutput:
        """Process the raw output from the refinement worker."""
        print(f"\nProcessing outline refinement output for phase: {self._state.get('development_phase', 'unknown')}")
        
        # Extract the core content from the raw output
        core_content = raw_output.strip()
        
        # Extract changes made from the output
        changes_made = self._extract_changes_made(raw_output)
        
        # Create structured output
        modifications = {
            "core_content": core_content,
            "refined_development": core_content,  # This is what gets passed to the next phase
            "changes_made": changes_made,
            "development_phase": self._state.get("development_phase", "unknown"),
            "timestamp": datetime.now().isoformat(),
        }
        
        # Create the worker output with the correct parameters
        output = WorkerOutput(
            modifications=modifications,
            notes={
                "change_count": len(changes_made),
                "development_phase": self._state.get("development_phase", "unknown"),
            },
            status="completed"
        )
        
        return output

    def _extract_changes_made(self, content: str) -> List[str]:
        """Extract the list of changes made from the refinement output."""
        changes = []
        
        # Try to find the "Changes Made" section
        matches = re.findall(r"(?:Changes Made|Changes|Refinement Changes)(.*?)(?:(?=#)|$)", content, re.DOTALL | re.IGNORECASE)
        
        if matches:
            # Take the first match and parse it
            changes_section = matches[0].strip()
            
            # Look for bullet points
            bullet_points = re.findall(r"(?:^|\n)[\s-]*([^-\n].+?)(?:(?=\n)|$)", changes_section)
            if bullet_points:
                changes = [point.strip() for point in bullet_points if point.strip()]
            else:
                # If no bullet points found, use the whole section
                changes = [changes_section]
        else:
            # If no "Changes Made" section, check for any bullet points at the end
            last_section = content.split("#")[-1]
            bullet_points = re.findall(r"(?:^|\n)[\s-]*([^-\n].+?)(?:(?=\n)|$)", last_section)
            if bullet_points:
                changes = [point.strip() for point in bullet_points if point.strip()]
            else:
                # Default to a generic change message
                changes = ["Refined the outline based on critique"]
        
        return changes

    def validate_output(self, output: WorkerOutput) -> bool:
        """Verify output meets requirements."""
        print("\nValidating outline refinement output...")

        if not output.modifications:
            print("Failed: No modifications")
            return False

        # Check for core content
        content = output.modifications.get("core_content")
        if not content or not content.strip():
            print("Failed: No content")
            return False

        # Check for refined development
        refined = output.modifications.get("refined_development")
        if not refined or not refined.strip():
            print("Failed: No refined development")
            return False

        # Check for changes made
        changes = output.modifications.get("changes_made", [])
        if not changes:
            print("Warning: No changes extracted")

        # Debug output
        print(f"\nRefinement content (first 200 chars): {content[:200]}...")
        print(f"Changes made: {changes[:3]}")
        
        # Since we're just checking the content exists, no need for complex validation
        return True 