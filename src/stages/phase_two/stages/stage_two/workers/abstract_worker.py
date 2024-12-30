# src/stages/phase_two/stages/stage_two/workers/abstract_worker.py

import json
from ....base.framework import FrameworkWorker
from ....base.worker import WorkerInput, WorkerOutput
from ..prompts.abstract_prompts import AbstractPrompts
from typing import Dict, Any

class AbstractDevelopmentWorker(FrameworkWorker):
    """Worker for developing the paper's abstract and high-level framework"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.stage_name = "abstract_development"
        self.prompts = AbstractPrompts()
        self._state = {
            "iterations": 0,
            "current_abstract": None
        }

    def validate_output(self, output: WorkerOutput) -> bool:
        """Verify output meets requirements"""
        print("\nValidating output...")
        
        if not output.modifications:
            print("Failed: No modifications")
            return False
            
        required_fields = {
            "abstract", "main_thesis", "core_contribution", 
            "key_moves", "development_notes", "validation_status"
        }
        
        missing_fields = required_fields - set(output.modifications.keys())
        if missing_fields:
            print(f"Failed: Missing required fields: {missing_fields}")
            return False
            
        # Print actual output for inspection
        print("\nReceived modifications:")
        print(json.dumps(output.modifications, indent=2))
            
        # Validate abstract length
        abstract_words = len(output.modifications["abstract"].split())
        print(f"\nAbstract length: {abstract_words} words")
        if not 120 <= abstract_words <= 300:
            print("Failed: Abstract length not between 120-300 words")
            return False
            
        # Validate key moves
        if not output.modifications["key_moves"] or \
        not all(output.modifications["key_moves"]):
            print("Failed: Empty or missing key moves")
            return False
            
        # Check validation status fields
        required_status = {
            "scope_appropriate", "clearly_articulated",
            "sufficiently_original", "feasibly_developable"
        }
        
        status = output.modifications["validation_status"]
        missing_status = required_status - set(status.keys())
        if missing_status:
            print(f"Failed: Missing validation status fields: {missing_status}")
            return False
            
        print("Validation passed!")
        return True

    def get_state(self) -> Dict[str, Any]:
        """Get current worker state"""
        return self._state.copy()

    def prepare_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Prepare input for abstract development"""
        return WorkerInput(
            outline_state=state,
            context={
                "literature": state["literature"],
                "final_selection": state["final_selection"]
            },
            task_specific={
                "stage": "abstract_development",
                "iteration": self._state["iterations"]
            }
        )

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        """Construct prompt for abstract development"""
        return self.prompts.get_development_prompt(
            lit_readings=input_data.context["literature"]["readings"],
            lit_synthesis=input_data.context["literature"]["synthesis"],
            lit_narrative=input_data.context["literature"]["narrative"],
            final_selection=input_data.context["final_selection"]
        )

    def process_output(self, response: str) -> WorkerOutput:
        """Process API response into structured output"""
        try:
            # Parse JSON response
            modifications = json.loads(response)
            
            # Update state
            self._state["iterations"] += 1
            self._state["current_abstract"] = modifications
            
            return WorkerOutput(
                modifications=modifications,
                notes={
                    "iteration": self._state["iterations"],
                    "validation_passed": True
                },
                status="completed"
            )
            
        except json.JSONDecodeError as e:
            return WorkerOutput(
                modifications={},
                notes={"error": f"Failed to parse response: {str(e)}"},
                status="failed"
            )