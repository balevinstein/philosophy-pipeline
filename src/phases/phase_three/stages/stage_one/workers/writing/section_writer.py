import json
from typing import Dict, Any
from pathlib import Path

from src.phases.core.base_worker import WorkerInput, WorkerOutput
from src.phases.core.worker_types import DevelopmentWorker
from src.phases.phase_three.stages.stage_one.prompts.section_writing.section_writing_prompts import (
    SectionWritingPrompts,
)
from src.phases.phase_two.base.framework import ValidationError


class SectionWritingWorker(DevelopmentWorker):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.prompts = SectionWritingPrompts()
        self._state = {"current_section_index": 0, "sections_completed": []}
        self.stage_name = "section_writing"

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        section_index = input_data.parameters.get("section_index", 0)
        
        if input_data.parameters.get("revision_mode", False):
            return self.prompts.construct_revision_prompt(
                writing_context=input_data.context["writing_context"],
                section_index=section_index,
                current_content=input_data.parameters["current_content"],
                revision_notes=input_data.parameters["revision_notes"]
            )
        else:
            return self.prompts.construct_writing_prompt(
                writing_context=input_data.context["writing_context"],
                section_index=section_index
            )

    def process_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Prepare input for section writing"""
        section_index = state.get("section_index", 0)
        
        return WorkerInput(
            context={
                "writing_context": state["writing_context"],
            },
            parameters={
                "section_index": section_index,
                "stage": "section_writing",
                "revision_mode": state.get("revision_mode", False),
                "current_content": state.get("current_content", ""),
                "revision_notes": state.get("revision_notes", ""),
            },
        )

    def process_output(self, response: str) -> WorkerOutput:
        """Process API response into structured output"""
        try:
            # Parse JSON response - should now be properly escaped
            response_clean = response.replace("```json", "").replace("```", "").strip()
            modifications = json.loads(response_clean)
            
            # Update state
            section_index = self._state["current_section_index"]
            self._state["sections_completed"].append(section_index)

            return WorkerOutput(
                modifications=modifications,
                notes={
                    "section_index": section_index,
                    "word_count": modifications.get("word_count", 0),
                    "content_bank_usage": modifications.get("content_bank_usage", []),
                },
                status="completed",
            )

        except json.JSONDecodeError as e:
            print(f"\nJSON parsing failed. Error: {str(e)}")
            print(f"Response length: {len(response)}")
            print(f"First 200 chars: {response[:200]}")
            print(f"Last 200 chars: {response[-200:]}")
                
            return WorkerOutput(
                modifications={},
                notes={"error": f"Failed to parse response: {str(e)}"},
                status="failed",
            )

    def validate_output(self, output: WorkerOutput) -> bool:
        """Verify output meets requirements"""
        print("\nValidating section output...")

        if not output.modifications:
            print("Failed: No modifications returned")
            return False

        required_fields = {
            "section_content",
            "word_count", 
            "content_bank_usage",
            "section_notes",
            "transition_points",
        }

        missing_fields = required_fields - set(output.modifications.keys())
        if missing_fields:
            print(f"Failed: Missing required fields: {missing_fields}")
            return False

        # Validate section content exists
        section_content = output.modifications.get("section_content", "")
        if not section_content or len(section_content.strip()) < 100:
            print("Failed: Section content too short or missing")
            return False

        # Check word count
        word_count = output.modifications.get("word_count", 0)
        actual_word_count = len(section_content.split())
        
        print(f"\nSection word count: {word_count} (reported) vs {actual_word_count} (actual)")
        
        # Allow some flexibility in word count reporting
        if abs(word_count - actual_word_count) > 50:
            print("Warning: Reported word count differs significantly from actual")

        # Validate transition points structure
        transition_points = output.modifications.get("transition_points", {})
        if not isinstance(transition_points, dict):
            print("Failed: transition_points must be a dictionary")
            return False

        # Print summary for inspection
        print(f"\nSection Summary:")
        print(f"Content length: {len(section_content)} characters")
        print(f"Word count: {actual_word_count} words")
        print(f"Content bank usage: {len(output.modifications.get('content_bank_usage', []))} items")
        
        print("Validation passed!")
        return True

    def set_section_index(self, index: int):
        """Set which section to write next"""
        self._state["current_section_index"] = index 

    def execute(self, state: Dict[str, Any]) -> WorkerOutput:
        """Main execution method with Analysis PDF support"""
        input_data = self.process_input(state)
        
        # Get system prompt if available
        system_prompt = self.get_system_prompt()
        
        # Construct prompt first - this triggers PDF selection in _select_analysis_exemplars
        prompt = self._construct_prompt(input_data)
        
        # Now get selected Analysis PDFs for style reference
        analysis_pdfs = self.prompts.get_selected_analysis_pdfs()
        
        # Make API call with PDFs if available
        if analysis_pdfs:
            print(f"Including {len(analysis_pdfs)} Analysis papers as style exemplars")
            response, _ = self.api_handler.make_api_call(
                stage=self.stage_name, 
                prompt=prompt,
                pdf_paths=analysis_pdfs,
                system_prompt=system_prompt
            )
        else:
            print("No Analysis papers available, proceeding without style exemplars")
            response, _ = self.api_handler.make_api_call(
                stage=self.stage_name, 
                prompt=prompt,
                system_prompt=system_prompt
            )
            
        output = self.process_output(response)
        if not self.validate_output(output):
            print(response)
            raise ValidationError("Worker output failed validation: ", self.stage_name)
        return output 