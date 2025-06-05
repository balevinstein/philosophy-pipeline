from typing import Dict, Any

class PaperReaderPrompts:
    """Prompts for analyzing complete draft papers"""
    
    def __init__(self):
        self.system_prompt = """You are a rigorous philosophy journal reviewer analyzing complete papers for global coherence and presentation quality. Your role is to identify paper-level issues affecting flow, consistency, and readability. You must provide actionable feedback for improving the paper's presentation. Your analysis will guide automated refinement."""
        
        self.critic_system_prompt = """You are a brutally honest philosophy journal reviewer who has seen countless papers rejected for preventable issues. Your task is to identify every weakness, gap, and potential rejection trigger in this paper. Be direct and unsparing in your criticism - your goal is to strengthen the paper by identifying real problems that would lead to rejection.

You must:
1. Identify major structural and argumentative flaws that would lead to desk rejection
2. Point out gaps in reasoning or evidence that would be fatal to the paper's success
3. Highlight unclear or imprecise language that would frustrate reviewers
4. Note any missed opportunities to engage with key literature or objections
5. Be specific and actionable in your criticism - vague feedback helps no one

Remember: Your harsh criticism is meant to help the author improve the paper. While you should be direct and unfiltered, your goal is to identify real issues that would prevent publication, not to be mean-spirited."""

    def construct_analysis_prompt(self, draft_paper: str, paper_overview: Dict[str, Any]) -> str:
        """Generate prompt for analyzing a complete paper"""
        return f"""
You are analyzing a complete draft philosophy paper for publication in a top journal. Your task is to identify global issues, integration problems, and areas for improvement.

PAPER OVERVIEW:
Thesis: {paper_overview['thesis']}
Target Length: {paper_overview['target_words']} words total
Target Journal: {paper_overview.get('target_journal', 'Analysis')}

PAPER CONTENT:
{draft_paper}

ANALYSIS REQUIREMENTS:
Your analysis should assess:

1. THESIS DEVELOPMENT AND PHILOSOPHICAL DEPTH
   - Is the thesis clearly stated and consistently developed?
   - Are all sections working to support the main argument?
   - Is there a clear progression of ideas?
   - Is there sufficient philosophical depth and development?
   - Are philosophical implications and consequences explored?
   - Are potential objections and responses thoroughly considered?
   - Is the philosophical significance of the arguments clear?

2. ARGUMENT STRUCTURE AND DEVELOPMENT
   - Is the overall argument structure sound and well-organized?
   - Are key premises and conclusions clearly identified?
   - Are objections and responses properly integrated?
   - Is there sufficient development of each argument?
   - Are philosophical implications fully explored?
   - Are counterarguments given adequate consideration?
   - Is the philosophical significance of each argument clear?

3. LITERATURE INTEGRATION
   - Is engagement with existing literature thorough and critical?
   - Are key positions and debates properly represented?
   - Are citations appropriate and sufficient?

4. WRITING QUALITY
   - Is the writing clear, precise, and accessible?
   - Are technical terms properly explained?
   - Is the paper free of unnecessary jargon?

OUTPUT FORMAT:

# Scratch Work
[Your preliminary analysis and notes]

# Global Analysis

## Thesis Development Assessment
[Evaluate how well the thesis is developed throughout the paper]

## Argument Structure Assessment
[Evaluate the overall argument structure and logical flow]

## Literature Integration Assessment
[Evaluate engagement with existing literature]

## Writing Quality Assessment
[Evaluate clarity, precision, and accessibility]

# Critical Issues Identified

## Major Issues
[Significant problems that would lead to rejection]

## Minor Issues
[Areas for improvement that would strengthen the paper]

## Positive Elements
[What works well in this paper]

# Integration Assessment

## Section Integration
[How well do the sections work together?]

## Argument Integration
[How well do the arguments build on each other?]

## Literature Integration
[How well is the literature integrated throughout?]

# Improvement Recommendations

## Structural Improvements
[Changes to improve overall organization and flow]

## Content Consolidation
[Areas where content could be tightened or expanded]

## Presentation Enhancements
[Changes to improve clarity and accessibility]

# Summary Assessment
[Overall judgment: MAJOR REVISION NEEDED, MINOR REFINEMENT NEEDED, or MINIMAL CHANGES NEEDED]

# Priority Actions
[Top 3-5 most important changes for improving paper quality]

Be thorough in your analysis while focusing on actionable feedback that will improve the paper's chances of publication.
"""

    def get_critic_system_prompt(self) -> str:
        """Return the critic system prompt for API calls"""
        return self.critic_system_prompt 