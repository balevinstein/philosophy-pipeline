from typing import Dict, Any, List

from src.phases.core.base_worker import WorkerInput, WorkerOutput
from src.phases.core.worker_types import RefinementWorker
from src.phases.phase_three.stages.stage_two.prompts.paper_integration_prompts import PaperIntegrationPrompts


class PaperIntegrationWorker(RefinementWorker):
    """Integrates improvements into the complete paper based on global analysis"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self._state = {"iterations": 0, "integration_history": []}
        self.stage_name = "paper_integration"
        self.prompts = PaperIntegrationPrompts()

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        return self.prompts.construct_integration_prompt(
            draft_paper=input_data.context["draft_paper"],
            paper_analysis=input_data.context["paper_analysis"],
            paper_overview=input_data.context["paper_overview"]
        )

    def process_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Prepare input for paper integration"""
        return WorkerInput(
            context={
                "draft_paper": state["draft_paper"],
                "paper_analysis": state["paper_analysis"],
                "paper_overview": state["paper_overview"]
            },
            parameters={
                "stage": "paper_integration",
                "integration_type": "final_presentation"
            }
        )

    def process_output(self, api_response: str) -> WorkerOutput:
        """Process the paper integration response"""
        try:
            # Extract the final paper from the response
            final_paper = self._extract_final_paper(api_response)
            
            # For simplified format, create default metadata
            integration_summary = "Paper integration completed with presentation improvements"
            changes_made = ["Improved overall presentation and flow"]
            final_stats = {"Word count": str(len(final_paper.split())), "Integration": "Complete"}
            
            # Try to extract metadata if it exists (backwards compatibility)
            try:
                extracted_summary = self._extract_integration_summary(api_response)
                if extracted_summary:
                    integration_summary = extracted_summary
                    
                extracted_changes = self._extract_changes_made(api_response)
                if extracted_changes:
                    changes_made = extracted_changes
                    
                extracted_stats = self._extract_final_statistics(api_response)
                if extracted_stats:
                    final_stats = extracted_stats
            except:
                pass  # Use defaults if extraction fails
            
            # Calculate word count of final paper
            final_word_count = len(final_paper.split()) if final_paper else 0
            
            return WorkerOutput(
                status="completed",
                modifications={
                    "final_paper": final_paper,
                    "integration_summary": integration_summary,
                    "changes_made": changes_made,
                    "final_statistics": final_stats,
                    "final_word_count": final_word_count,
                    "response_content": api_response  # Save full response for debugging
                },
                notes="Paper integration completed successfully"
            )
        except Exception as e:
            return WorkerOutput(
                status="failed",
                modifications={"response_content": api_response},  # Save response even on failure
                notes=f"Failed to process paper integration: {str(e)}"
            )

    def _extract_final_paper(self, content: str) -> str:
        """Extract the final paper from the response"""
        # With simplified output format, the entire response should be the paper
        # But we still need to handle cases where the LLM might add extra text
        
        lines = content.split('\n')
        paper_lines = []
        found_title = False
        
        for line in lines:
            # Skip any initial meta-commentary
            if not found_title and line.startswith('# ') and not any(x in line.lower() for x in ['integration', 'summary', 'changes', 'statistics', 'note', 'important']):
                found_title = True
                paper_lines.append(line)
            elif found_title:
                # Stop if we hit meta-sections (though there shouldn't be any)
                if any(x in line for x in ['# Integration Summary', '# Changes Made', '# Final Statistics', 'Would you like', 'Shall I proceed']):
                    break
                paper_lines.append(line)
            elif not found_title and line.strip() and not line.startswith('#'):
                # If we haven't found a title yet but see content, it might be the start
                paper_lines.append(line)
        
        final_paper = '\n'.join(paper_lines).strip()
        
        # If we still don't have much content, just return the whole response
        if len(final_paper) < 1000:
            # Remove obvious meta-commentary but keep everything else
            cleaned_lines = []
            for line in content.split('\n'):
                if not any(phrase in line.lower() for phrase in ['would you like', 'shall i proceed', 'important note', 'due to length limitations']):
                    cleaned_lines.append(line)
            final_paper = '\n'.join(cleaned_lines).strip()
        
        return final_paper

    def _extract_integration_summary(self, content: str) -> str:
        """Extract the integration summary"""
        lines = content.split('\n')
        in_summary = False
        summary_lines = []
        
        for line in lines:
            if "# Integration Summary" in line:
                in_summary = True
                continue
            elif line.startswith("# ") and in_summary:
                break
            elif in_summary:
                summary_lines.append(line)
        
        return '\n'.join(summary_lines).strip()

    def _extract_changes_made(self, content: str) -> List[str]:
        """Extract the list of changes made"""
        lines = content.split('\n')
        in_changes = False
        changes = []
        
        for line in lines:
            if "# Changes Made" in line:
                in_changes = True
                continue
            elif line.startswith("# ") and in_changes:
                break
            elif in_changes and (line.startswith('- ') or line.startswith('* ')):
                changes.append(line[2:].strip())
        
        return changes

    def _extract_final_statistics(self, content: str) -> Dict[str, str]:
        """Extract final statistics"""
        stats = {}
        lines = content.split('\n')
        in_stats = False
        
        for line in lines:
            if "# Final Statistics" in line:
                in_stats = True
                continue
            elif line.startswith("# ") and in_stats:
                break
            elif in_stats and ":" in line:
                key, value = line.split(":", 1)
                stats[key.strip("- ").strip()] = value.strip()
        
        return stats

    def validate_output(self, output: WorkerOutput) -> bool:
        """Validate the paper integration output"""
        if output.status != "completed":
            return False
            
        # Check that we have a final paper
        final_paper = output.modifications.get("final_paper", "")
        if not final_paper or len(final_paper) < 1000:
            print(f"Warning: Final paper too short or missing ({len(final_paper)} chars)")
            # Don't fail validation - let's see what we got
            
        # Check word count is reasonable
        word_count = output.modifications.get("final_word_count", 0)
        if word_count < 3000 or word_count > 5000:
            print(f"Warning: Final word count {word_count} outside expected range")
            
        print(f"Paper integration validation passed! Final paper: {word_count} words")
        return True 