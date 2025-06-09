from typing import Dict, Any
import json
from datetime import datetime

from src.phases.core.base_worker import BaseWorker, WorkerInput, WorkerOutput
from src.phases.phase_two.stages.stage_five.prompts import ConsolidationPrompts
from src.utils.api import APIHandler


class ConsolidationWorker(BaseWorker):
    """
    Worker responsible for intelligent consolidation of Phase II outputs.
    
    This worker:
    1. Synthesizes outputs from II.1-4 into a unified vision
    2. Performs comprehensive diagnostic analysis
    3. Identifies issues and proposes solutions
    4. Creates consolidated context for subsequent phases
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.name = "intelligent_consolidation"
        self.description = "Creates unified vision and diagnostic analysis of Phase II outputs"
        self.prompts = ConsolidationPrompts()
        self.api_handler = APIHandler(config)
        self.stage_name = "phase_2_5_consolidation"
    
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the consolidation analysis"""
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
        """Prepare input for consolidation"""
        print("\nPreparing input for consolidation...")
        
        # Validate required inputs
        required_keys = ["literature_synthesis", "abstract_framework", "developed_moves", "detailed_outline"]
        for key in required_keys:
            if key not in state:
                raise ValueError(f"Missing required state: {key}")
        
        return WorkerInput(
            context={
                "literature_synthesis": state["literature_synthesis"],
                "abstract_framework": state["abstract_framework"],
                "developed_moves": state["developed_moves"],
                "detailed_outline": state["detailed_outline"]
            },
            parameters={
                "phase": "consolidation",
                "timestamp": datetime.now().isoformat()
            }
        )
    
    def _construct_prompt(self, input_data: WorkerInput) -> str:
        """Construct the consolidation prompt"""
        return self.prompts.get_consolidation_prompt(
            literature_synthesis=json.dumps(input_data.context["literature_synthesis"], indent=2),
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
        print("\nProcessing consolidation output...")
        
        # Debug: Save raw output for inspection
        with open("outputs/debug_consolidation_response.txt", "w") as f:
            f.write(raw_output)
        print("Debug: Raw output saved to outputs/debug_consolidation_response.txt")
        
        try:
            # Parse JSON response
            consolidation_data = json.loads(raw_output)
            
            # Debug: Print structure
            print(f"Debug: Parsed JSON keys: {list(consolidation_data.keys())}")
            
            # Count issues from the identified_issues array
            issue_count = len(consolidation_data.get("identified_issues", []))
            high_priority_count = sum(
                1 for issue in consolidation_data.get("identified_issues", [])
                if issue.get("priority") == "high"
            )
            
            # Count additional issues from diagnostic details
            diagnostic_details = consolidation_data.get("diagnostic_details", {})
            quality_violations = diagnostic_details.get("quality_standard_violations", {})
            
            hajek_count = len(quality_violations.get("hajek_failures", []))
            pattern_count = len(quality_violations.get("analysis_pattern_violations", []))
            rlhf_count = len(quality_violations.get("anti_rlhf_violations", []))
            
            total_violations = hajek_count + pattern_count + rlhf_count
            
            print(f"Identified {issue_count} general issues ({high_priority_count} high priority)")
            print(f"Found {total_violations} quality standard violations:")
            print(f"  - {hajek_count} Hájek heuristic failures")
            print(f"  - {pattern_count} Analysis pattern violations") 
            print(f"  - {rlhf_count} Anti-RLHF violations")
            print(f"Paper readiness: {consolidation_data.get('overall_assessment', {}).get('paper_readiness', 'unknown')}")
            
            return WorkerOutput(
                modifications={
                    "consolidated_analysis": consolidation_data,
                    "diagnostic_summary": {
                        "total_issues": issue_count,
                        "high_priority_issues": high_priority_count,
                        "quality_violations": {
                            "hajek_failures": hajek_count,
                            "pattern_violations": pattern_count,
                            "rlhf_violations": rlhf_count,
                            "total": total_violations
                        },
                        "paper_readiness": consolidation_data.get("overall_assessment", {}).get("paper_readiness"),
                        "main_strengths": consolidation_data.get("overall_assessment", {}).get("main_strengths", []),
                        "main_weaknesses": consolidation_data.get("overall_assessment", {}).get("main_weaknesses", []),
                        "key_recommendations": [rec.get("action", "") for rec in consolidation_data.get("priority_recommendations", [])]
                    },
                    "timestamp": datetime.now().isoformat()
                },
                notes={
                    "phase": "consolidation",
                    "issue_count": issue_count,
                    "violations_count": total_violations,
                    "recommendations_provided": len(consolidation_data.get("priority_recommendations", []))
                },
                status="completed"
            )
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Raw output preview: {raw_output[:500]}...")
            raise ValueError(f"Failed to parse consolidation response: {e}")
        except Exception as e:
            print(f"Error processing consolidation output: {e}")
            raise
    
    def validate_output(self, output: WorkerOutput) -> bool:
        """Validate the consolidation output"""
        print("\nValidating consolidation output...")
        
        if not output.modifications:
            print("Failed: No modifications")
            return False
        
        consolidated_analysis = output.modifications.get("consolidated_analysis")
        if not consolidated_analysis:
            print("Failed: No consolidated analysis")
            return False
        
        # Check for required sections
        required_sections = [
            "consolidated_vision",
            "key_move_assessment",
            "identified_issues",
            "overall_assessment"
        ]
        
        for section in required_sections:
            if section not in consolidated_analysis:
                print(f"Failed: Missing required section '{section}'")
                return False
        
        # Validate key move assessment
        key_moves = consolidated_analysis.get("key_move_assessment", [])
        if len(key_moves) != 5:  # We expect 5 key moves
            print(f"Warning: Expected 5 key moves, found {len(key_moves)}")
        
        print("Validation passed!")
        return True 