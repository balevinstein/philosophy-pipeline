import json
from typing import Dict, Any
from ....base.framework import CriticWorker
from ....base.worker import WorkerInput, WorkerOutput
from ..prompts.key_moves_critic_prompts import KeyMovesCriticPrompts

class KeyMovesCritic(CriticWorker):
    """Worker for critiquing key argumentative moves"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.prompts = KeyMovesCriticPrompts()
        self.stage_name = "key_moves_critic"
        self._state = {
            "iterations": 0,
            "previous_critiques": []
        }

    def get_state(self) -> Dict[str, Any]:
        """Get current worker state"""
        return self._state.copy()

    def prepare_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Prepare input for critique"""
        print("\nPreparing input for key moves critique...")
        print("\nReceived state keys:", list(state.keys()))
        
        if "framework" not in state or "outline" not in state:
            raise ValueError("Missing required state: framework and outline")
            
        # Check for key moves data in different possible locations
        key_moves_data = state.get("key_moves_analysis")  # From initial worker
        if not key_moves_data:
            key_moves_data = state.get("current_moves")   # From refinement worker
        if not key_moves_data:
            raise ValueError("No key moves data found in state")
                
        return WorkerInput(
            outline_state=state,
            context={
                "framework": state["framework"],
                "outline": state["outline"],
                "key_moves": key_moves_data,
                "lit_readings": state.get("literature", {}).get("readings"),
                "lit_synthesis": state.get("literature", {}).get("synthesis"),
                "lit_narrative": state.get("literature", {}).get("narrative")
            },
            task_specific={
                "iteration": self._state["iterations"]
            }
        )

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        """Construct critique prompt"""
        return self.prompts.get_critique_prompt(
            current_moves=input_data.context["key_moves"],
            framework=input_data.context["framework"],
            outline=input_data.context["outline"],
            lit_readings=input_data.context.get("lit_readings"),
            lit_synthesis=input_data.context.get("lit_synthesis"),
            lit_narrative=input_data.context.get("lit_narrative")
        )

    def process_output(self, response: str) -> WorkerOutput:
        """Process response into structured output"""
        try:
            # Split into sections
            sections = {}
            current_section = None
            current_content = []
            
            for line in response.split('\n'):
                if line.startswith('# '):
                    if current_section:
                        sections[current_section] = '\n'.join(current_content).strip()
                    current_section = line[2:].strip()
                    current_content = []
                else:
                    current_content.append(line)
                    
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()


            # Extract summary assessment
            summary = self._extract_summary(sections.get('Summary Assessment', ''))
            
            # Extract key recommendations
            recommendations = []
            summary_text = sections.get('Summary Assessment', '')
            next_steps_idx = summary_text.find('Next steps:')
            if next_steps_idx != -1:
                next_steps = summary_text[next_steps_idx:].split('\n')[1:]
                recommendations = [step[3:] for step in next_steps if step.startswith('1.')]
                
            # Update state
            self._state["iterations"] += 1
            self._state["previous_critiques"].append({
                "sections": sections,
                "summary": summary,
                "recommendations": recommendations
            })
                
            return WorkerOutput(
                modifications={
                    "content": response.strip(),
                    "sections": sections,
                    "summary": summary,
                    "recommendations": recommendations,
                    "iteration": self._state["iterations"]
                },
                notes={
                    "summary_assessment": summary,
                    "key_recommendations": recommendations
                },
                status="completed"
        )
        except Exception as e:
            return WorkerOutput(
                modifications={},
                notes={"error": f"Failed to process response: {str(e)}"},
                status="failed"
            )

    def _extract_summary(self, summary_text: str) -> str:
        """Extract summary assessment from text"""
        for assessment in ["MAJOR REVISION", "MINOR REFINEMENT", "MINIMAL CHANGES"]:
            if assessment in summary_text:
                return assessment
        return "UNKNOWN"

    def validate_output(self, output: WorkerOutput) -> bool:
        """Verify output meets basic requirements"""
        print("\nValidating key moves critique output...")
        
        if not output.modifications:
            print("Failed: No modifications")
            return False
            
        content = output.modifications.get("content")
        if not content:
            print("Failed: No content")
            return False
            
        # We'll require some key sections but allow flexibility in others
        required_sections = [
            "Scratch Work",
            "Summary Assessment"
        ]
        
        sections = content.split("# ")
        section_titles = [s.split("\n")[0].strip() for s in sections if s]
        
        print("\nFound sections:", section_titles)
        print("Required sections:", required_sections)
        
        missing_sections = [section for section in required_sections 
                          if section not in section_titles]
        if missing_sections:
            print(f"Failed: Missing required sections: {missing_sections}")
            return False
            
        # Verify we have a valid summary assessment
        summary = content.split("# Summary Assessment")[-1].strip()
        valid_assessments = ["MAJOR REVISION", "MINOR REFINEMENT", "MINIMAL CHANGES"]
        if not any(assessment in summary for assessment in valid_assessments):
            print("Failed: Invalid or missing summary assessment")
            return False
            
        print("Validation passed!")
        return True

    def evaluate(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate provided content - implements abstract method"""
        result = self.run({"key_moves_analysis": content})
        return result.modifications