from typing import Dict, Any, List

from src.phases.core.base_worker import WorkerInput, WorkerOutput
from src.phases.core.worker_types import CriticWorker


class PaperReaderWorker(CriticWorker):
    """Analyzes complete draft paper for global issues and presentation quality"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self._state = {"iterations": 0, "previous_analyses": []}
        self.stage_name = "paper_reader"

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        return self.construct_paper_analysis_prompt(
            draft_paper=input_data.context["draft_paper"],
            paper_overview=input_data.context["paper_overview"],
            sections_metadata=input_data.context["sections_metadata"]
        )

    def construct_paper_analysis_prompt(self, draft_paper: str, paper_overview: Dict[str, Any], 
                                      sections_metadata: List[Dict[str, Any]]) -> str:
        """Generate prompt for analyzing the complete paper"""
        
        # Calculate paper statistics
        total_words = len(draft_paper.split())
        section_count = len(sections_metadata)
        
        return f"""
You are an expert philosophy editor analyzing a complete draft paper for global presentation and writing quality. Your task is to identify paper-level issues that affect overall coherence, flow, and readability.

PAPER OVERVIEW:
Title: {paper_overview['thesis'][:100]}...
Target Length: {paper_overview['target_words']} words
Actual Length: {total_words} words
Sections: {section_count}

ANALYSIS FOCUS:
Your analysis should focus on PRESENTATION and WRITING QUALITY, not intellectual content. The core arguments have been developed - you're evaluating how well they're presented as a unified paper.

EVALUATION AREAS:

1. GLOBAL ARGUMENT FLOW
   - Does the paper build a coherent case from introduction to conclusion?
   - Are key concepts introduced at the right time?
   - Does each section clearly advance the main thesis?
   - Are there logical gaps or jumps in the overall progression?

2. SECTION TRANSITIONS
   - Do sections connect smoothly to each other?
   - Are there abrupt shifts or missing bridges?
   - Do opening/closing paragraphs create good handoffs?
   - Is the overall narrative flow clear?

3. CONSISTENCY AND COHERENCE
   - Is terminology used consistently throughout?
   - Does the writing maintain consistent tone and style?
   - Are there contradictions or tensions between sections?
   - Is the thesis consistently supported throughout?

4. REPETITION AND REDUNDANCY
   - Are key points repeated unnecessarily across sections?
   - Are examples or citations redundantly used?
   - Could any content be consolidated or streamlined?
   - Are transitions repetitive (e.g., "having established...")?

5. PACING AND BALANCE
   - Is appropriate depth given to each major component?
   - Are any sections disproportionately long or short?
   - Does the paper maintain reader engagement throughout?
   - Is the conclusion satisfying given the buildup?

6. PRESENTATION QUALITY
   - Is the writing clear and accessible?
   - Are technical terms properly introduced?
   - Are examples well-integrated into arguments?
   - Is the overall structure easy to follow?

COMPLETE DRAFT PAPER:
{draft_paper}

OUTPUT FORMAT:

# Global Analysis

## Argument Flow Assessment
[Evaluate how well the paper builds its case from start to finish]

## Transition Quality Assessment
[Analyze connections between sections and overall narrative flow]

## Consistency Assessment
[Check for consistent terminology, tone, and thesis support]

## Repetition Analysis
[Identify unnecessary repetition or redundancy]

## Pacing and Balance Assessment
[Evaluate word distribution and depth across sections]

## Presentation Quality Assessment
[Analyze clarity, accessibility, and overall readability]

# Issues Identified

## Major Issues
[Significant problems that affect overall paper quality - limit to 3-5 most important]

## Minor Issues
[Smaller improvements that would enhance presentation - limit to 5-7 items]

## Strengths
[What works well in the current draft]

# Integration Recommendations

## Structural Improvements
[Changes to section organization, transitions, or flow]

## Content Consolidation
[Opportunities to reduce repetition or improve efficiency]

## Presentation Enhancements
[Improvements to clarity, consistency, or accessibility]

# Summary Assessment
[Overall judgment: MAJOR INTEGRATION NEEDED, MINOR REFINEMENTS NEEDED, or MINIMAL CHANGES NEEDED]

# Priority Actions
[Top 3-5 most important changes for improving paper quality]

Focus on actionable feedback that will improve the paper's presentation and coherence while respecting the existing intellectual content.
"""

    def process_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Prepare input for paper analysis"""
        return WorkerInput(
            context={
                "draft_paper": state["draft_paper"],
                "paper_overview": state["paper_overview"],
                "sections_metadata": state["sections_metadata"]
            },
            parameters={
                "stage": "paper_reader",
                "analysis_type": "global_integration"
            }
        )

    def process_output(self, api_response: str) -> WorkerOutput:
        """Process the paper analysis response"""
        try:
            # Extract key sections from the analysis
            analysis_sections = self._parse_analysis_sections(api_response)
            
            # Determine assessment level
            assessment = self._extract_assessment(api_response)
            
            # Extract priority actions
            priority_actions = self._extract_priority_actions(api_response)
            
            return WorkerOutput(
                status="completed",
                modifications={
                    "analysis_content": api_response,
                    "summary_assessment": assessment,
                    "major_issues": analysis_sections.get("major_issues", []),
                    "minor_issues": analysis_sections.get("minor_issues", []),
                    "strengths": analysis_sections.get("strengths", []),
                    "priority_actions": priority_actions,
                    "structural_improvements": analysis_sections.get("structural_improvements", []),
                    "content_consolidation": analysis_sections.get("content_consolidation", []),
                    "presentation_enhancements": analysis_sections.get("presentation_enhancements", [])
                },
                notes="Paper analysis completed successfully"
            )
        except Exception as e:
            return WorkerOutput(
                status="failed",
                modifications={},
                notes=f"Failed to process paper analysis: {str(e)}"
            )

    def _parse_analysis_sections(self, content: str) -> Dict[str, list]:
        """Extract structured information from analysis"""
        sections = {}
        
        # Basic parsing - look for bullet points under each major section
        major_issues = self._extract_list_items(content, "## Major Issues")
        minor_issues = self._extract_list_items(content, "## Minor Issues")
        strengths = self._extract_list_items(content, "## Strengths")
        structural_improvements = self._extract_list_items(content, "## Structural Improvements")
        content_consolidation = self._extract_list_items(content, "## Content Consolidation")
        presentation_enhancements = self._extract_list_items(content, "## Presentation Enhancements")
        
        return {
            "major_issues": major_issues,
            "minor_issues": minor_issues,
            "strengths": strengths,
            "structural_improvements": structural_improvements,
            "content_consolidation": content_consolidation,
            "presentation_enhancements": presentation_enhancements
        }

    def _extract_list_items(self, content: str, section_header: str) -> list:
        """Extract list items from a section"""
        items = []
        lines = content.split('\n')
        in_section = False
        
        for line in lines:
            if section_header in line:
                in_section = True
                continue
            elif line.startswith('##') and in_section:
                break
            elif in_section and (line.startswith('- ') or line.startswith('* ')):
                items.append(line[2:].strip())
        
        return items

    def _extract_assessment(self, content: str) -> str:
        """Extract the summary assessment"""
        if "MAJOR INTEGRATION NEEDED" in content:
            return "MAJOR_INTEGRATION_NEEDED"
        elif "MINOR REFINEMENTS NEEDED" in content:
            return "MINOR_REFINEMENTS_NEEDED"
        elif "MINIMAL CHANGES NEEDED" in content:
            return "MINIMAL_CHANGES_NEEDED"
        else:
            return "ASSESSMENT_UNCLEAR"

    def _extract_priority_actions(self, content: str) -> list:
        """Extract priority actions"""
        return self._extract_list_items(content, "# Priority Actions")

    def validate_output(self, output: WorkerOutput) -> bool:
        """Validate the paper analysis output"""
        if output.status != "completed":
            return False
            
        required_fields = {
            "analysis_content", "summary_assessment", "major_issues", 
            "minor_issues", "priority_actions"
        }
        
        missing_fields = required_fields - set(output.modifications.keys())
        if missing_fields:
            print(f"Missing required fields: {missing_fields}")
            return False
            
        print("Paper analysis validation passed!")
        return True 