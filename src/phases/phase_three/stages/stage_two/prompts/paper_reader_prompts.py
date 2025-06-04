from typing import Dict, Any, List


class PaperReaderPrompts:
    """Prompts for analyzing complete draft papers in Phase III.2"""
    
    def __init__(self):
        self.system_prompt = """You are a rigorous Analysis journal reviewer analyzing complete papers for global coherence and publication quality. Your role is to assess papers against Analysis journal standards - evaluating conversational rigor, example-driven argumentation, and accessible presentation. You must provide actionable feedback for achieving Analysis publication standards."""

        self.analysis_journal_standards = """
ANALYSIS JOURNAL QUALITY STANDARDS:

VOICE & ACCESSIBILITY ASSESSMENT:
- Does the paper maintain conversational rigor throughout?
- Heavy first person usage present? ("I argue that...", "I will show...", "My response is...")
- Direct reader engagement evident? ("Consider this case...", "Notice that...", "You might think...")
- Short, clear sentences (15-25 words average) or excessive complexity?
- Technical terms defined immediately upon introduction?
- Professional but accessible tone maintained throughout?

STRUCTURAL ORGANIZATION:
- Clear numbered sections (1, 2.1, 2.2, etc.) with explicit organization?
- Thesis stated clearly within first 300-400 words?
- Preview sentences at section beginnings? ("In this section, I will...")
- Explicit signposting throughout? ("This suggests...", "It follows that...", "However...")
- Smooth transitions between sections and within sections?

ARGUMENTATION THROUGH EXAMPLES:
- Concrete examples introduced early (by second paragraph)?
- Examples doing genuine argumentative work, not just illustration?
- Core examples revisited from multiple analytical angles?
- Systematic development: Concrete case → Analysis → General principle → Test against intuitions?
- Examples relatable and immediately graspable?

LITERATURE ENGAGEMENT EVALUATION:
- Strategic and minimal literature use (2-3 key interlocutors maximum)?
- Inline citations (Author Year: page) used appropriately?
- Brief context-setting rather than extended literature review?
- Engagement with specific claims, not general positions?
- Literature positioned to support argument rather than demonstrate knowledge?

DEVELOPMENT PATTERNS:
- Progressive refinement rather than dramatic turns?
- Systematic rather than surprising development?
- Objections addressed throughout text, not isolated in dedicated section?
- Clear transition patterns ("However...", "On the other hand...", "This suggests...")?

ANALYSIS PUBLICATION READINESS:
- Efficiency over comprehensiveness (every word earns its place)?
- Word count appropriate for Analysis (typically 2000-4000 words)?
- Professional but friendly tone suitable for general philosophy audience?
- Publication-ready presentation quality?
"""

    def construct_analysis_prompt(self, draft_paper: str, paper_overview: Dict[str, Any]) -> str:
        """Generate prompt for analyzing the complete paper against Analysis standards"""
        
        # Calculate paper statistics
        total_words = len(draft_paper.split())
        
        return f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase III.2 (Global Integration).
You are analyzing a complete draft paper for Analysis journal publication quality.
Your analysis will guide final integration and polishing to meet Analysis standards.
You have access to Analysis journal papers as exemplars for comparison.
</context>

<analysis_journal_standards>
{self.analysis_journal_standards}
</analysis_journal_standards>

<task>
Analyze the complete draft paper against Analysis journal publication standards.
Focus on conversational rigor, example-driven argumentation, and accessible presentation.
Identify gaps between current quality and Analysis publication standards.
Provide actionable feedback for achieving Analysis publication quality.
</task>

<paper_information>
THESIS: {paper_overview['thesis']}
TARGET LENGTH: {paper_overview['target_words']} words
ACTUAL LENGTH: {total_words} words
TARGET JOURNAL: Analysis
</paper_information>

<evaluation_areas>
1. ANALYSIS VOICE & STYLE ASSESSMENT
   - Does this sound like an Analysis paper? (conversational but rigorous)
   - Appropriate first person usage and reader engagement?
   - Clear, accessible prose with philosophical precision?
   - Professional but friendly tone throughout?

2. ANALYSIS STRUCTURE PATTERNS
   - Numbered sections with clear organization?
   - Thesis clearly stated within first page?
   - Explicit signposting and preview sentences?
   - Smooth transitions matching Analysis patterns?

3. EXAMPLE-DRIVEN ARGUMENTATION
   - Concrete examples doing real argumentative work?
   - Examples introduced early and revisited systematically?
   - Clear progression from cases to general principles?
   - Examples relatable and immediately graspable?

4. ANALYSIS LITERATURE INTEGRATION
   - Strategic, minimal literature use (not comprehensive surveys)?
   - Inline citations and brief context-setting?
   - Engagement with specific claims rather than general positions?
   - Literature positioned to advance argument?

5. ANALYSIS DEVELOPMENT PATTERNS
   - Progressive refinement rather than dramatic turns?
   - Objections addressed throughout rather than isolated?
   - Systematic development with clear logic?
   - Analysis-style transition patterns?

6. PUBLICATION READINESS FOR ANALYSIS
   - Word efficiency and precision (every word earns its place)?
   - Appropriate length for Analysis journal?
   - Publication-quality presentation?
   - Suitable for Analysis readership?
</evaluation_areas>

<draft_paper>
{draft_paper}
</draft_paper>

<output_format>
# Scratch Work
[Your preliminary analysis and notes on Analysis journal fit]

# Global Analysis

## Thesis Development Assessment
[How well is the thesis developed and supported throughout?]

## Argument Structure Assessment
[Does the argumentative structure match Analysis patterns?]

## Literature Integration Assessment
[Is literature used strategically in Analysis style?]

## Writing Quality Assessment
[Does the writing meet Analysis publication standards?]

# Critical Issues Identified

## Major Issues
[Significant gaps from Analysis publication standards - limit to 3-5 most critical]

## Minor Issues
[Areas for improvement to better match Analysis style - limit to 5-7 items]

## Analysis Style Gaps
[Specific ways the paper differs from Analysis journal patterns]

# Integration Assessment

## Analysis Voice Evaluation
[How well does this match Analysis conversational rigor?]

## Example Integration Quality
[Are examples used effectively in Analysis style?]

## Structural Organization
[Does the organization follow Analysis patterns?]

# Improvement Recommendations

## Analysis Style Enhancements
[Specific changes to match Analysis journal patterns]

## Structural Improvements
[Changes to better align with Analysis organization standards]

## Presentation Refinements
[Improvements for Analysis publication quality]

# Summary Assessment
[Overall judgment: MAJOR_REVISION (significant gaps from Analysis standards), MINOR_REFINEMENT (mostly aligned but needs polish), or MINIMAL_CHANGES (publication-ready for Analysis)]

# Priority Actions
[Top 3-5 most important changes for Analysis publication standards]
</output_format>

<requirements>
- Assess specifically against Analysis journal standards, not general academic writing
- Focus on conversational rigor, example-driven argumentation, and accessible presentation
- Identify concrete gaps from Analysis publication patterns
- Provide actionable feedback for achieving Analysis publication quality
- Reference Analysis style characteristics throughout your assessment
</requirements>"""
    
    def get_system_prompt(self) -> str:
        """Return the system prompt for API calls"""
        return self.system_prompt 