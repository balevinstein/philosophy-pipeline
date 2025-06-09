from typing import Dict, Any, List, Tuple
import logging
import json

from src.phases.core.worker_base import Worker
from src.phases.phase_two.stages.stage_seven.prompts.refinement_prompts import RefinementPrompts
from src.utils.api import APIHandler
from src.utils.json_utils import JSONHandler


class RefinementWorker(Worker):
    """Worker for refining key moves based on review feedback"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.prompts = RefinementPrompts()
        self.logger = logging.getLogger(__name__)
        self.api_handler = APIHandler(config)
        self.json_handler = JSONHandler()
        
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run refinement on flagged moves based on review feedback
        
        Args:
            state: Dictionary containing:
                - original_moves: List of original key moves
                - final_writing_plan: The revision plan from Phase II.6
                - referee_report: The review from Phase II.6
                - move_examples: Examples of good philosophical moves
                
        Returns:
            Dictionary containing refined moves and metadata
        """
        self.logger.info("Starting refinement of flagged moves...")
        
        # Extract inputs
        original_moves = state.get("original_moves", [])
        writing_plan = state.get("final_writing_plan", {})
        referee_report = state.get("referee_report", {})
        move_examples = state.get("move_examples", {})
        
        # Get the revised thesis for consistency
        revised_thesis = writing_plan.get("revised_thesis", "")
        revised_contribution = writing_plan.get("revised_core_contribution", "")
        
        # Process moves according to the writing plan
        refined_moves = []
        refinement_count = 0
        
        for planned_move in writing_plan.get("final_key_moves", []):
            move_index = int(planned_move.get("move_index", 0))
            status = planned_move.get("status", "Retained")
            
            # Find the original move
            original_move = None
            for move in original_moves:
                if move.get("key_move_index", move.get("index", -1)) == move_index:
                    original_move = move
                    break
                    
            if not original_move:
                self.logger.warning(f"Could not find original move {move_index}")
                continue
                
            if status == "Cut":
                self.logger.info(f"Skipping cut move {move_index}")
                continue
                
            if status == "Flagged for Redevelopment":
                # This move needs LLM-based refinement
                self.logger.info(f"Redeveloping move {move_index}")
                refined_move = self._redevelop_move(
                    original_move,
                    planned_move,
                    revised_thesis,
                    revised_contribution,
                    referee_report,
                    move_examples
                )
                refinement_count += 1
            elif status == "Merged":
                # For merged moves, we'll adapt but not fully redevelop
                refined_move = self._adapt_merged_move(
                    original_move,
                    planned_move,
                    revised_thesis
                )
            else:
                # Retained moves get minimal updates for thesis consistency
                refined_move = self._update_retained_move(
                    original_move,
                    planned_move,
                    revised_thesis
                )
                
            refined_moves.append(refined_move)
            
        # Create output state
        output_state = {
            "refined_moves": refined_moves,
            "refinement_metadata": {
                "original_count": len(original_moves),
                "refined_count": len(refined_moves),
                "redeveloped_count": refinement_count,
                "revised_thesis": revised_thesis,
                "revised_contribution": revised_contribution
            }
        }
        
        self.logger.info(f"Refinement complete. Redeveloped {refinement_count} moves.")
        return output_state
        
    def _redevelop_move(
        self, 
        original_move: Dict[str, Any],
        planned_move: Dict[str, Any],
        revised_thesis: str,
        revised_contribution: str,
        referee_report: Dict[str, Any],
        move_examples: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Completely redevelop a flagged move using LLM"""
        
        # Extract relevant critique from referee report
        relevant_critique = self._extract_relevant_critique(
            original_move["key_move_index"],
            referee_report
        )
        
        # Get the redevelopment prompt
        prompt = self.prompts.get_redevelopment_prompt(
            original_move,
            planned_move,
            revised_thesis,
            revised_contribution,
            relevant_critique,
            move_examples
        )
        
        # Make API call
        response_text, duration = self.api_handler.make_api_call(
            stage="phase_2_7_redevelopment",
            prompt=prompt,
            system_prompt=self.prompts.get_system_prompt()
        )
        
        # Parse response
        cleaned_response = self.json_handler.clean_json_string(response_text)
        refined_content = json.loads(cleaned_response)
        
        # Create refined move structure
        refined_move = {
            "key_move_index": original_move["key_move_index"],
            "key_move_text": planned_move.get("revised_description", original_move["key_move_text"]),
            "original_content": original_move.get("final_content", ""),
            "refined_content": refined_content.get("refined_content", ""),
            "refinement_notes": refined_content.get("refinement_notes", ""),
            "addressed_issues": refined_content.get("addressed_issues", []),
            "status": "Redeveloped",
            "api_duration": duration
        }
        
        return refined_move
        
    def _adapt_merged_move(
        self,
        original_move: Dict[str, Any],
        planned_move: Dict[str, Any],
        revised_thesis: str
    ) -> Dict[str, Any]:
        """Adapt a move that will be merged with another"""
        
        # For now, just update the description and flag for merging
        return {
            "key_move_index": original_move["key_move_index"],
            "key_move_text": planned_move.get("revised_description", original_move["key_move_text"]),
            "refined_content": original_move.get("final_content", ""),
            "status": "Merged",
            "merge_guidance": planned_move.get("justification", "")
        }
        
    def _update_retained_move(
        self,
        original_move: Dict[str, Any],
        planned_move: Dict[str, Any],
        revised_thesis: str
    ) -> Dict[str, Any]:
        """Minimally update a retained move for consistency"""
        
        return {
            "key_move_index": original_move["key_move_index"],
            "key_move_text": planned_move.get("revised_description", original_move["key_move_text"]),
            "refined_content": original_move.get("final_content", ""),
            "status": "Retained",
            "retention_notes": planned_move.get("justification", "")
        }
        
    def _extract_relevant_critique(
        self,
        move_index: int,
        referee_report: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extract critique relevant to a specific move from the referee report"""
        
        relevant_critique = []
        
        # Check coherence issues
        for issue in referee_report.get("coherence_issues", []):
            location = issue.get("location", {})
            if location.get("move_index") == str(move_index):
                relevant_critique.append({
                    "type": "coherence_issue",
                    "issue": issue
                })
                
        # Check argumentative weaknesses
        for weakness in referee_report.get("argumentative_weaknesses", []):
            location = weakness.get("location", "")
            if f"Move {move_index}" in location or f"Key Move {move_index}" in location:
                relevant_critique.append({
                    "type": "argumentative_weakness",
                    "issue": weakness
                })
                
        # Check Hájek test failures
        for failure in referee_report.get("hajek_test_failures", []):
            location = failure.get("location", "")
            if f"Move {move_index}" in location:
                relevant_critique.append({
                    "type": "hajek_failure",
                    "issue": failure
                })
                
        # Check anti-RLHF violations
        for violation in referee_report.get("anti_rlhf_violations", []):
            location = violation.get("location", "")
            if f"Move {move_index}" in location:
                relevant_critique.append({
                    "type": "anti_rlhf_violation",
                    "issue": violation
                })
                
        return relevant_critique 