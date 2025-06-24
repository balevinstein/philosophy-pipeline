from typing import Dict, Any
import json
from datetime import datetime

from src.phases.core.base_worker import BaseWorker, WorkerInput, WorkerOutput
from src.phases.phase_two.stages.stage_five.prompts.quality_audit_prompts import QualityAuditPrompts
from src.utils.api import APIHandler
from src.utils.json_utils import JSONHandler


class QualityAuditWorker(BaseWorker):
    """
    Worker for Phase II.5b Targeted Quality Audit - focused quality standards application.
    
    This worker:
    1. Takes synthesis results and applies quality standards to priority areas
    2. Provides specific, actionable remediation guidance
    3. Creates detailed roadmap for II.6-8 refinement stages
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.name = "targeted_quality_audit"
        self.description = "Targeted quality standards application with remediation guidance"
        self.prompts = QualityAuditPrompts()
        self.api_handler = APIHandler(config)
        self.json_handler = JSONHandler()
        self.stage_name = "phase_2_5b_quality_audit"
    
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the quality audit"""
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
        """Prepare input for quality audit"""
        print("\nPreparing input for quality audit...")
        
        # Validate required inputs
        required_keys = ["synthesis_results", "abstract_framework", "developed_moves", "detailed_outline"]
        for key in required_keys:
            if key not in state:
                raise ValueError(f"Missing required state: {key}")
        
        return WorkerInput(
            context={
                "synthesis_results": state["synthesis_results"],
                "abstract_framework": state["abstract_framework"],
                "developed_moves": state["developed_moves"],
                "detailed_outline": state["detailed_outline"]
            },
            parameters={
                "phase": "quality_audit",
                "timestamp": datetime.now().isoformat()
            }
        )
    
    def _construct_prompt(self, input_data: WorkerInput) -> str:
        """Construct the quality audit prompt"""
        return self.prompts.get_audit_prompt(
            synthesis_results=input_data.context["synthesis_results"],
            abstract_framework=json.dumps(input_data.context["abstract_framework"], indent=2),
            key_moves=json.dumps(input_data.context["developed_moves"], indent=2),
            outline_sections=json.dumps(input_data.context["detailed_outline"], indent=2)
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
        print("\nProcessing quality audit output...")
        
        # Debug: Save raw output for inspection
        with open("outputs/debug_quality_audit_response.txt", "w") as f:
            f.write(raw_output)
        print("Debug: Raw output saved to outputs/debug_quality_audit_response.txt")
        
        try:
            # Extract JSON portion if response has narrative text before it
            json_start = raw_output.find('```json\n{')
            if json_start != -1:
                json_end = raw_output.rfind('}\n```')
                if json_end != -1:
                    json_content = raw_output[json_start+8:json_end+1]  # Extract just the JSON
                    audit_data = json.loads(json_content)
                else:
                    # Try without ending markers
                    json_content = raw_output[json_start+8:]
                    cleaned_output = self.json_handler.clean_json_string(json_content)
                    audit_data = json.loads(cleaned_output)
            else:
                # Standard JSON parsing
                cleaned_output = self.json_handler.clean_json_string(raw_output)
                audit_data = json.loads(cleaned_output)
            
            # Debug: Print structure
            print(f"Debug: Parsed JSON keys: {list(audit_data.keys())}")
            
            priority_analysis = audit_data.get("priority_analysis", [])
            refinement_roadmap = audit_data.get("refinement_roadmap", {})
            implementation_details = audit_data.get("implementation_details", {})
            
            print(f"Priority issues analyzed: {len(priority_analysis)}")
            print(f"Overall difficulty: {refinement_roadmap.get('overall_difficulty', 'unknown')}")
            
            # Count violations by type
            total_violations = 0
            for analysis in priority_analysis:
                violations = analysis.get("quality_violations", [])
                total_violations += len(violations)
            
            urgent_fixes = len(implementation_details.get("urgent_fixes", []))
            important_fixes = len(implementation_details.get("important_improvements", []))
            
            print(f"Total quality violations found: {total_violations}")
            print(f"Urgent fixes needed: {urgent_fixes}")
            print(f"Important improvements: {important_fixes}")
            
            return WorkerOutput(
                modifications={
                    "quality_audit_results": audit_data,
                    "audit_summary": {
                        "issues_analyzed": len(priority_analysis),
                        "total_violations": total_violations,
                        "urgent_fixes": urgent_fixes,
                        "important_improvements": important_fixes,
                        "overall_difficulty": refinement_roadmap.get("overall_difficulty"),
                        "stage_6_focus": refinement_roadmap.get("stage_6_planning_focus", []),
                        "stage_7_targets": refinement_roadmap.get("stage_7_refinement_targets", []),
                        "stage_8_optimization": refinement_roadmap.get("stage_8_writing_optimization", [])
                    },
                    "timestamp": datetime.now().isoformat()
                },
                notes={
                    "phase": "quality_audit",
                    "violations_found": total_violations,
                    "refinement_difficulty": refinement_roadmap.get("overall_difficulty")
                },
                status="completed"
            )
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Raw output preview: {raw_output[:500]}...")
            raise ValueError(f"Failed to parse quality audit response: {e}")
        except Exception as e:
            print(f"Error processing quality audit output: {e}")
            raise
    
    def validate_output(self, output: WorkerOutput) -> bool:
        """Validate the quality audit output"""
        print("\nValidating quality audit output...")
        
        if not output.modifications:
            print("Failed: No modifications")
            return False
        
        audit_results = output.modifications.get("quality_audit_results")
        if not audit_results:
            print("Failed: No audit results")
            return False
        
        # Check for required sections
        required_sections = [
            "priority_analysis",
            "refinement_roadmap",
            "implementation_details"
        ]
        
        for section in required_sections:
            if section not in audit_results:
                print(f"Failed: Missing required section '{section}'")
                return False
        
        print("Validation passed!")
        return True 