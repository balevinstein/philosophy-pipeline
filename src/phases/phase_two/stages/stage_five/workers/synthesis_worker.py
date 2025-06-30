from typing import Dict, Any
import json
from datetime import datetime

from src.phases.core.base_worker import BaseWorker, WorkerInput, WorkerOutput
from src.phases.phase_two.stages.stage_five.prompts.synthesis_prompts import QuickSynthesisPrompts
from src.utils.api import APIHandler
from src.utils.json_utils import JSONHandler


class SynthesisWorker(BaseWorker):
    """
    Worker for Phase II.5a Quick Synthesis - lightweight coherence check.
    
    This worker:
    1. Performs basic coherence check of Phase II outputs
    2. Identifies major issues that would prevent publication
    3. Sets priorities for subsequent refinement stages
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.name = "quick_synthesis"
        self.description = "Quick coherence check and major issue identification"
        self.prompts = QuickSynthesisPrompts()
        self.api_handler = APIHandler(config)
        self.json_handler = JSONHandler()
        self.stage_name = "phase_2_5a_synthesis"
    
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the synthesis analysis"""
        print(f"\nRunning {self.name} worker...")
        
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
            raise ValueError(f"Output validation failed for {self.name}")
        
        return output.modifications
    
    def process_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Prepare input for synthesis"""
        print("\nPreparing input for synthesis...")
        
        # Validate required inputs
        required_keys = ["abstract_framework", "developed_moves", "detailed_outline"]
        for key in required_keys:
            if key not in state:
                raise ValueError(f"Missing required state: {key}")
        
        return WorkerInput(
            context={
                "abstract_framework": state["abstract_framework"],
                "developed_moves": state["developed_moves"],
                "detailed_outline": state["detailed_outline"]
            },
            parameters={
                "phase": "synthesis",
                "timestamp": datetime.now().isoformat()
            }
        )
    
    def _construct_prompt(self, input_data: WorkerInput) -> str:
        """Construct the synthesis prompt"""
        return self.prompts.get_synthesis_prompt(
            abstract_framework=json.dumps(input_data.context["abstract_framework"], indent=2),
            developed_moves=json.dumps(input_data.context["developed_moves"], indent=2),
            detailed_outline=json.dumps(input_data.context["detailed_outline"], indent=2)
        )
    
    def _execute_llm_call(self, prompt: str) -> str:
        """Execute the LLM call"""
        print(f"\nExecuting LLM call for {self.stage_name}...")
        
        # Use the API handler to make the call
        response_text, duration = self.api_handler.make_api_call(
            stage=self.stage_name,
            prompt=prompt,
            system_prompt=self.prompts.get_system_prompt()
        )
        
        print(f"LLM call completed in {duration:.1f} seconds")
        return response_text
    
    def process_output(self, raw_output: str) -> WorkerOutput:
        """Process the raw output from the LLM"""
        print("\nProcessing synthesis output...")
        
        # Debug: Save raw output for inspection
        with open("outputs/debug_synthesis_response.txt", "w") as f:
            f.write(raw_output)
        print("Debug: Raw output saved to outputs/debug_synthesis_response.txt")
        
        try:
            # Clean and parse JSON response
            cleaned_output = self.json_handler.clean_json_string(raw_output)
            synthesis_data = json.loads(cleaned_output)
            
            # Debug: Print structure
            print(f"Debug: Parsed JSON keys: {list(synthesis_data.keys())}")
            
            coherence_assessment = synthesis_data.get("coherence_assessment", {})
            priority_issues = synthesis_data.get("priority_issues", [])
            refinement_guidance = synthesis_data.get("refinement_guidance", {})
            
            print(f"Overall coherence: {coherence_assessment.get('overall_coherence', 'unknown')}")
            print(f"Priority issues identified: {len(priority_issues)}")
            print(f"Paper readiness: {refinement_guidance.get('paper_readiness', 'unknown')}")
            
            # Count issues by severity
            critical_issues = sum(1 for issue in priority_issues if issue.get("severity") == "critical")
            major_issues = sum(1 for issue in priority_issues if issue.get("severity") == "major")
            
            print(f"  - Critical issues: {critical_issues}")
            print(f"  - Major issues: {major_issues}")
            
            return WorkerOutput(
                modifications={
                    "synthesis_results": synthesis_data,
                    "synthesis_summary": {
                        "overall_coherence": coherence_assessment.get("overall_coherence"),
                        "main_story": coherence_assessment.get("main_story"),
                        "total_issues": len(priority_issues),
                        "critical_issues": critical_issues,
                        "major_issues": major_issues,
                        "paper_readiness": refinement_guidance.get("paper_readiness"),
                        "immediate_priorities": refinement_guidance.get("immediate_priorities", []),
                        "main_strengths": refinement_guidance.get("main_strengths", [])
                    },
                    "timestamp": datetime.now().isoformat()
                },
                notes={
                    "phase": "synthesis",
                    "issue_count": len(priority_issues),
                    "coherence_level": coherence_assessment.get("overall_coherence")
                },
                status="completed"
            )
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Raw output preview: {raw_output[:500]}...")
            raise ValueError(f"Failed to parse synthesis response: {e}")
        except Exception as e:
            print(f"Error processing synthesis output: {e}")
            raise
    
    def validate_output(self, output: WorkerOutput) -> bool:
        """Validate the synthesis output"""
        print("\nValidating synthesis output...")
        
        if not output.modifications:
            print("Failed: No modifications")
            return False
        
        synthesis_results = output.modifications.get("synthesis_results")
        if not synthesis_results:
            print("Failed: No synthesis results")
            return False
        
        # Check for required sections
        required_sections = [
            "coherence_assessment",
            "priority_issues", 
            "refinement_guidance"
        ]
        
        for section in required_sections:
            if section not in synthesis_results:
                print(f"Failed: Missing required section '{section}'")
                return False
        
        print("Validation passed!")
        return True 