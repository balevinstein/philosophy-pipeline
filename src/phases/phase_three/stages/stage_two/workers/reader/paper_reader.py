from typing import Dict, Any, List
from pathlib import Path
import random

from src.phases.core.base_worker import WorkerInput, WorkerOutput
from src.phases.core.worker_types import CriticWorker
from src.phases.phase_three.stages.stage_two.prompts.paper_reader_prompts import PaperReaderPrompts


class PaperReaderWorker(CriticWorker):
    """Worker for analyzing complete draft papers for global issues and presentation quality
    
    Enhanced with Analysis PDF integration for publication quality assessment.
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.prompts = PaperReaderPrompts()
        self._state = {"iterations": 0, "analysis_history": []}
        self.stage_name = "paper_reader"
        self.selected_analysis_texts = []  # Store selected Analysis text extracts

    def _get_analysis_texts(self, text_count: int = 2) -> list:
        """Select Analysis text extracts for publication quality assessment"""
        analysis_dir = Path("./data/analysis_extracts")
        if not analysis_dir.exists():
            print(f"⚠️ Analysis text extracts directory not found at {analysis_dir}")
            return []
        
        text_files = list(analysis_dir.glob("*.txt"))
        if not text_files:
            print(f"⚠️ No text files found in {analysis_dir}")
            return []
        
        # Select text extracts randomly for varied quality assessment examples
        selected_texts = random.sample(text_files, min(text_count, len(text_files)))
        
        print(f"📑 Including {len(selected_texts)} Analysis text extract(s) for {self.stage_name} quality assessment:")
        for txt in selected_texts:
            print(f"   • {txt.name}")
        
        return selected_texts

    def _construct_prompt(self, input_data: Dict[str, Any]) -> str:
        """Construct the analysis prompt"""
        return self.prompts.construct_analysis_prompt(
            input_data["draft_paper"],
            input_data["paper_overview"]
        )

    def get_system_prompt(self) -> str:
        """Get the system prompt for API calls"""
        return self.prompts.system_prompt

    def process_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare input for paper analysis"""
        return {
            "draft_paper": input_data["draft_paper"],
            "paper_overview": input_data["paper_overview"]
        }

    def process_output(self, response: str) -> WorkerOutput:
        """Process analysis response into structured output"""
        try:
            # Update state
            self._state["iterations"] += 1
            self._state["analysis_history"].append(response)

            # Extract summary assessment
            summary_assessment = self._extract_summary_assessment(response)
            
            # Extract critical issues
            critical_issues = self._extract_critical_issues(response)
            
            # Extract priority actions
            priority_actions = self._extract_priority_actions(response)
            
            # Extract strengths
            strengths = self._extract_strengths(response)

            return WorkerOutput(
                modifications={
                    "content": response.strip(),
                    "analysis_content": response.strip(),  # Add alias for backwards compatibility
                    "summary_assessment": summary_assessment,
                    "critical_issues": critical_issues,
                    "major_issues": critical_issues.get("major", []),  # Add flat access
                    "minor_issues": critical_issues.get("minor", []),  # Add flat access
                    "priority_actions": priority_actions,
                    "strengths": strengths,
                    "iteration": self._state["iterations"],
                },
                notes={
                    "assessment_level": summary_assessment,
                    "major_issues_count": len(critical_issues.get("major", [])),
                    "minor_issues_count": len(critical_issues.get("minor", [])),
                },
                status="completed",
            )

        except Exception as e:
            return WorkerOutput(
                modifications={},
                notes={"error": f"Failed to process analysis response: {str(e)}"},
                status="failed",
            )

    def _extract_summary_assessment(self, response: str) -> str:
        """Extract the summary assessment from the analysis"""
        try:
            summary_section = response.split("# Summary Assessment")[-1].strip()
            
            # Updated to match new Analysis prompt format
            if "MAJOR_REVISION" in summary_section:
                return "MAJOR_REVISION"
            elif "MINOR_REFINEMENT" in summary_section:
                return "MINOR_REFINEMENT"
            elif "MINIMAL_CHANGES" in summary_section:
                return "MINIMAL_CHANGES"
            else:
                return "UNCLEAR"
        except:
            return "UNCLEAR"

    def _extract_critical_issues(self, response: str) -> Dict[str, list]:
        """Extract major and minor issues from the analysis"""
        try:
            issues_section = response.split("# Critical Issues Identified")[1].split("#")[0]
            
            major_issues = []
            minor_issues = []
            
            if "## Major Issues" in issues_section:
                major_content = issues_section.split("## Major Issues")[1].split("##")[0]
                major_issues = [line.strip() for line in major_content.split("\n") if line.strip() and not line.startswith("[")]
            
            if "## Minor Issues" in issues_section:
                minor_content = issues_section.split("## Minor Issues")[1].split("##")[0]
                minor_issues = [line.strip() for line in minor_content.split("\n") if line.strip() and not line.startswith("[")]
            
            return {"major": major_issues, "minor": minor_issues}
        except:
            return {"major": [], "minor": []}

    def _extract_priority_actions(self, response: str) -> List[str]:
        """Extract priority actions from the analysis"""
        try:
            # Look for priority actions section
            if "# Priority Actions" in response:
                actions_section = response.split("# Priority Actions")[1].split("#")[0]
                actions = []
                for line in actions_section.split("\n"):
                    if line.strip() and (line.startswith('- ') or line.startswith('* ') or line.startswith('1.') or line.startswith('2.') or line.startswith('3.')):
                        # Clean up the line
                        clean_line = line.strip()
                        # Remove list markers
                        for marker in ['- ', '* ', '1. ', '2. ', '3. ', '4. ', '5. ']:
                            if clean_line.startswith(marker):
                                clean_line = clean_line[len(marker):].strip()
                                break
                        if clean_line:
                            actions.append(clean_line)
                return actions
            else:
                # If no priority actions section, extract from improvement recommendations
                if "# Improvement Recommendations" in response:
                    rec_section = response.split("# Improvement Recommendations")[1].split("#")[0]
                    actions = []
                    for line in rec_section.split("\n")[:5]:  # Take first 5 lines as priority
                        if line.strip() and (line.startswith('- ') or line.startswith('* ')):
                            actions.append(line[2:].strip())
                    return actions
            return []
        except:
            return []

    def _extract_strengths(self, response: str) -> List[str]:
        """Extract strengths from the analysis"""
        try:
            # Look for strengths or positive elements
            if "## Positive Elements" in response:
                strengths_section = response.split("## Positive Elements")[1].split("##")[0]
            elif "## Strengths" in response:
                strengths_section = response.split("## Strengths")[1].split("##")[0]
            else:
                return []
            
            strengths = []
            for line in strengths_section.split("\n"):
                if line.strip() and (line.startswith('- ') or line.startswith('* ')):
                    strengths.append(line[2:].strip())
            return strengths
        except:
            return []

    def validate_output(self, output: WorkerOutput) -> bool:
        """Verify output meets requirements"""
        print("\nValidating paper analysis...")

        if not output.modifications:
            print("Failed: No modifications returned")
            return False

        content = output.modifications.get("content", "")
        if not content:
            print("Failed: No content in analysis")
            return False

        # Check for required sections
        required_sections = [
            "# Scratch Work",
            "# Global Analysis", 
            "# Critical Issues Identified",
            "# Integration Assessment",
            "# Improvement Recommendations",
            "# Summary Assessment",
        ]

        missing_sections = [section for section in required_sections if section not in content]
        if missing_sections:
            print(f"Failed: Missing required sections: {missing_sections}")
            return False

        # Check for subsections within Global Analysis
        analysis_subsections = [
            "## Thesis Development Assessment",
            "## Argument Structure Assessment",
            "## Literature Integration Assessment", 
            "## Writing Quality Assessment",
        ]
        
        missing_analysis = [sub for sub in analysis_subsections if sub not in content]
        if missing_analysis:
            print(f"Failed: Missing analysis subsections: {missing_analysis}")
            return False

        # Verify summary assessment is valid
        summary_assessment = output.modifications.get("summary_assessment", "")
        if summary_assessment not in ["MAJOR_REVISION", "MINOR_REFINEMENT", "MINIMAL_CHANGES"]:
            print(f"Failed: Invalid summary assessment: {summary_assessment}")
            return False

        print(f"Analysis validation passed! Assessment: {summary_assessment}")
        return True

    def execute(self, state: Dict[str, Any]) -> WorkerOutput:
        """Main execution method with Analysis text extracts for quality assessment"""
        input_data = self.process_input(state)
        
        # Select Analysis text extracts for publication quality standards
        analysis_texts = self._get_analysis_texts(text_count=2)
        self.selected_analysis_texts = analysis_texts
        
        # Construct prompt
        prompt = self._construct_prompt(input_data)
        
        # Get system prompt if available
        system_prompt = self.get_system_prompt() if hasattr(self, 'get_system_prompt') else None
        
        # Call LLM with Analysis text extracts if available
        print(f"\n🔍 Executing {self.stage_name} with Analysis quality standards...")
        if self.selected_analysis_texts:
            response, _ = self.api_handler.make_api_call(
                stage=self.stage_name,
                prompt=prompt,
                text_paths=self.selected_analysis_texts,
                system_prompt=system_prompt
            )
        else:
            response, _ = self.api_handler.make_api_call(
                stage=self.stage_name,
                prompt=prompt,
                system_prompt=system_prompt
            )
        
        # Process output
        output = self.process_output(response)
        
        if not self.validate_output(output):
            print(f"⚠️ {self.stage_name} output validation failed")
        
        return output 