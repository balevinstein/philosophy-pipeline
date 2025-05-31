from typing import Dict, Any, List


class PaperReaderPrompts:
    """Prompts for analyzing complete draft papers in Phase III.2"""
    
    def __init__(self):
        self.system_prompt = """You are a rigorous philosophy journal reviewer analyzing complete papers for global coherence and presentation quality. Your role is to identify paper-level issues affecting flow, consistency, and readability. You must provide actionable feedback for improving the paper's presentation. Your analysis will guide automated refinement."""

    def construct_paper_analysis_prompt(self, draft_paper: str, paper_overview: Dict[str, Any], 
                                      sections_metadata: List[Dict[str, Any]]) -> str:
        """Generate prompt for analyzing the complete paper"""
        
        # Calculate paper statistics
        total_words = len(draft_paper.split())
        section_count = len(sections_metadata)
        
        return f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase III.2 (Global Integration).
You are analyzing a complete draft paper for presentation and writing quality.
The core arguments have been developed - you're evaluating how well they're presented as a unified paper.
Your analysis will guide final integration and polishing.
</context>

<task>
Analyze the complete draft paper for global presentation and writing quality.
Focus on coherence, flow, transitions, and overall readability.
Identify paper-level issues that affect the unified presentation.
Provide actionable feedback for improving paper quality.
</task>

<paper_information>
TITLE: {paper_overview['thesis'][:100]}...
TARGET LENGTH: {paper_overview['target_words']} words
ACTUAL LENGTH: {total_words} words
SECTIONS: {section_count}
</paper_information>

<analysis_focus>
Your analysis should focus on PRESENTATION and WRITING QUALITY, not intellectual content. 
The core arguments have been developed - you're evaluating how well they're presented as a unified paper.
</analysis_focus>

<evaluation_areas>
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
</evaluation_areas>

<draft_paper>
{draft_paper}
</draft_paper>

<output_format>
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
</output_format>

<requirements>
Focus on actionable feedback that will improve the paper's presentation and coherence while respecting the existing intellectual content.
Be specific about issues and provide clear guidance for improvements.
Prioritize the most impactful changes that will enhance paper quality.
</requirements>"""
    
    def get_system_prompt(self) -> str:
        """Return the system prompt for API calls"""
        return self.system_prompt 