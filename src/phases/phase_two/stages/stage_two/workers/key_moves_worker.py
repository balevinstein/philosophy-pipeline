# src/stages/phase_two/stages/stage_two/workers/key_moves_worker.py

import json
from typing import Dict, Any, List, Optional
from ....base.framework import FrameworkWorker
from ....base.worker import WorkerInput, WorkerOutput
from ..prompts.key_moves_prompts import KeyMovesPrompts

class KeyMovesWorker(FrameworkWorker):
    """Worker for analyzing feasibility of individual key moves"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.prompts = KeyMovesPrompts()
        self.stage_name = "key_moves_development"
        self._state = {
            "iterations": 0,
            "current_move": None,
            "analyzed_moves": {},  # Store analysis results by move
            "development_phase": "argument"
        }
        
    def get_state(self) -> Dict[str, Any]:
        """Get current worker state"""
        return self._state.copy()

    def prepare_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Prepare input for key moves analysis"""
        print("\nPreparing input for key moves analysis...")
        print("\nReceived state keys:", list(state.keys()))
        
        if "framework" not in state or "outline" not in state:
            raise ValueError("Missing required state: framework and outline")
                
        # Get moves from framework
        moves = state["framework"].get("key_moves", [])
        if not moves:
            raise ValueError("No key moves found in framework")

        # Set current move if not already set
        if self._state["current_move"] is None and moves:
            self._state["current_move"] = moves[0]
                
        return WorkerInput(
            outline_state=state,
            context={
                "framework": state["framework"],
                "outline": state["outline"],
                "lit_readings": state.get("literature", {}).get("readings"),
                "lit_synthesis": state.get("literature", {}).get("synthesis"),
                "lit_narrative": state.get("literature", {}).get("narrative")
            },
            task_specific={
                "phase": "key_moves_analysis",
                "move": self._state["current_move"]
            }
        )
    
    def _construct_prompt(self, input_data: WorkerInput) -> str:
        """Construct prompt based on current phase"""
        return self.prompts.get_argument_prompt(
            move=input_data.task_specific["move"],
            abstract=input_data.context.get("abstract"),
            outline=input_data.context.get("outline"),
            prior_moves=self._state.get("analyzed_moves")
        )

    def validate_output(self, output: WorkerOutput) -> bool:
        """Verify output meets requirements"""
        print("\nValidating key moves output...")
        
        if not output.modifications:
            print("Failed: No modifications")
            return False
            
        content = output.modifications.get("content")
        if not content:
            print("Failed: No content")
            return False
            
        # Check for required sections
        required_sections = ["Scratch Work", "Final Argument Development"]
        
        sections = content.split("# ")
        section_titles = [s.split("\n")[0].strip() for s in sections if s]
        
        print("\nFound sections:", section_titles)
        print("Required sections:", required_sections)
        
        if not all(req in section_titles for req in required_sections):
            print("Failed: Missing required sections")
            return False
            
        print("Validation passed!")
        return True

    def analyze_move(self, 
                    move: str, 
                    abstract: str,
                    outline: str,
                    prior_moves: Optional[Dict] = None) -> Dict[str, Any]:
        """Analyze a single key move"""
        # Set up state for this move
        self._state["current_move"] = move
        
        input_data = WorkerInput(
            outline_state={"current_move": move},
            context={
                "abstract": abstract,
                "outline": outline,
                "prior_moves": prior_moves
            },
            task_specific={
                "phase": "analysis"
            }
        )
        
        result = self.run(input_data)
        
        return {
            "move": move,
            "analysis": result.modifications["content"],
            "feasibility_assessment": result.modifications.get("feasibility", {}),
            "development_notes": result.modifications.get("notes", {})
        }

    def process_output(self, response: str) -> WorkerOutput:
        """Process API response into structured output"""
        try:
            return WorkerOutput(
                modifications={
                    "content": response.strip()
                },
                notes={
                    "move": self._state["current_move"],
                    "iteration": self._state["iterations"]
                },
                status="completed"
            )
            
        except Exception as e:
            return WorkerOutput(
                modifications={},
                notes={"error": f"Failed to process response: {str(e)}"},
                status="failed"
            )