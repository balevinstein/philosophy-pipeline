from typing import Dict, Any, List
import re
from datetime import datetime

from src.phases.core.base_worker import WorkerInput, WorkerOutput
from src.phases.core.worker_types import CriticWorker
from src.phases.phase_two.stages.stage_four.prompts.critic.critic_prompts import OutlineCriticPrompts
from src.utils.api import APIHandler  # Add import for API handler


class OutlineCriticWorker(CriticWorker):
    """
    Worker responsible for critiquing detailed outline development.
    
    This worker assesses the outline development based on the current
    phase (framework integration, literature mapping, etc).
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.prompts = OutlineCriticPrompts()
        self.stage_name = "detailed_outline_critique"
        self._state = {
            "iterations": 0,
            "development_phase": "framework_integration",  # Default phase
        }
        self.api_handler = APIHandler(config)  # Initialize API handler
    
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the critic worker to evaluate outline development."""
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
        # The config has a model configuration for detailed_outline_critic
        model_stage = "detailed_outline_critic"
        
        # API handler returns (response_text, duration) tuple, we only need the response text
        response_text, _ = self.api_handler.make_api_call(model_stage, prompt)
        return response_text

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        """Construct the appropriate critique prompt based on the development phase."""
        framework = input_data.context.get("framework", {})
        developed_key_moves = input_data.context.get("developed_key_moves", [])
        current_outline_development = input_data.context.get("current_outline_development", "")
        previous_versions = input_data.context.get("previous_versions", [])
        
        # Get development phase from input parameters
        development_phase = input_data.parameters.get("development_phase", self._state["development_phase"])
        
        print(f"Constructing critique prompt for development phase: {development_phase}")
        
        # Use the generic get_critique_prompt method which will select the right prompt
        return self.prompts.get_critique_prompt(
            outline_development=current_outline_development,
            framework=framework,
            developed_key_moves=developed_key_moves,
            development_phase=development_phase,
            previous_versions=previous_versions,
            iteration=self._state.get("iterations", 0)
        )

    def process_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Prepare input for outline critique."""
        print("\nPreparing input for outline critique...")
        print("\nReceived state keys:", list(state.keys()))

        # Validate required inputs
        if "framework" not in state or "current_outline_development" not in state:
            raise ValueError("Missing required state: framework, current_outline_development")
        
        # Get the development phase from state if available
        if "development_phase" in state:
            self._state["development_phase"] = state["development_phase"]
            print(f"Setting development phase to: {self._state['development_phase']}")
        
        # Increment iterations counter
        self._state["iterations"] += 1
        
        return WorkerInput(
            context={
                "framework": state["framework"],
                "outline": state.get("outline", {}),
                "developed_key_moves": state.get("developed_key_moves", []),
                "current_outline_development": state["current_outline_development"],
                "previous_versions": state.get("previous_versions", []),
            },
            parameters={
                "phase": "outline_critique",
                "development_phase": self._state["development_phase"],
                "iteration": self._state["iterations"],
            },
        )

    def process_output(self, raw_output: str) -> WorkerOutput:
        """Process the raw output from the critique."""
        print(f"\nProcessing outline critique for phase: {self._state.get('development_phase', 'unknown')}")
        
        # Extract the assessment and recommendations from the critique
        assessment = self._extract_assessment(raw_output)
        recommendations = self._extract_recommendations(raw_output)
        
        print(f"Extracted assessment: {assessment}")
        print(f"Extracted {len(recommendations)} recommendations")
        
        # Create structured output
        modifications = {
            "critique": raw_output.strip(),
            "assessment": assessment,
            "recommendations": recommendations,
            "development_phase": self._state.get("development_phase", "unknown"),
            "timestamp": datetime.now().isoformat(),
        }
        
        # Create the worker output with the correct parameters
        output = WorkerOutput(
            modifications=modifications,
            notes={
                "development_phase": self._state.get("development_phase", "unknown"),
                "assessment": assessment,
                "recommendation_count": len(recommendations),
            },
            status="completed"
        )
        
        return output

    def _extract_assessment(self, content: str) -> str:
        """Extract the assessment from the critique."""
        # Look for assessment indicators
        assessment_indicators = [
            "MAJOR REVISION NEEDED", 
            "MINOR REFINEMENT NEEDED", 
            "GOOD", 
            "VERY GOOD", 
            "EXCELLENT"
        ]
        
        for indicator in assessment_indicators:
            if indicator in content:
                return indicator
        
        # Check for "Overall Assessment" section
        if "Overall Assessment:" in content:
            assessment_section = content.split("Overall Assessment:", 1)[1].strip()
            first_line = assessment_section.split("\n", 1)[0].strip()
            
            for indicator in assessment_indicators:
                if indicator in first_line:
                    return indicator
        
        # Default assessment
        return "NEEDS REFINEMENT"

    def _extract_recommendations(self, content: str) -> List[str]:
        """Extract the list of recommendations from the critique."""
        recommendations = []
        
        # Try to find the "Recommendations" section
        if "Recommendations" in content:
            recommendations_section = content.split("Recommendations", 1)[1].split("##", 1)[0].strip()
            
            # Extract numbered or bulleted items
            pattern = r"(?:^|\n)[\s]*(?:[0-9]+\.|\-|\*)\s*(.+?)(?=(?:\n[\s]*(?:[0-9]+\.|\-|\*))|$)"
            matches = re.findall(pattern, recommendations_section, re.DOTALL)
            
            if matches:
                recommendations = [match.strip() for match in matches if match.strip()]
        
        # If no recommendations found in a specific section, look for "Areas for Improvement"
        if not recommendations and "Areas for Improvement" in content:
            improvements_section = content.split("Areas for Improvement", 1)[1].split("##", 1)[0].strip()
            
            # Extract numbered or bulleted items
            pattern = r"(?:^|\n)[\s]*(?:[0-9]+\.|\-|\*)\s*(.+?)(?=(?:\n[\s]*(?:[0-9]+\.|\-|\*))|$)"
            matches = re.findall(pattern, improvements_section, re.DOTALL)
            
            if matches:
                recommendations = [match.strip() for match in matches if match.strip()]
        
        # Default recommendation if none found
        if not recommendations:
            recommendations = ["Consider reviewing the outline structure for logical flow and framework alignment"]
        
        return recommendations

    def validate_output(self, output: WorkerOutput) -> bool:
        """Verify output meets requirements."""
        print("\nValidating outline critique output...")

        if not output.modifications:
            print("Failed: No modifications")
            return False

        # Check for critique content
        critique = output.modifications.get("critique")
        if not critique or not critique.strip():
            print("Failed: No critique content")
            return False

        # Check for assessment
        assessment = output.modifications.get("assessment")
        if not assessment:
            print("Failed: No assessment")
            return False

        # Check for recommendations
        recommendations = output.modifications.get("recommendations", [])
        if not recommendations:
            print("Warning: No recommendations")

        # Debug output
        print(f"\nCritique assessment: {assessment}")
        print(f"Recommendation count: {len(recommendations)}")
        if recommendations:
            print(f"First recommendation: {recommendations[0]}")
        
        return True 