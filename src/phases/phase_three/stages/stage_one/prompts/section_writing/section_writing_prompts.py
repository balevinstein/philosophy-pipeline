import json
from typing import Dict, Any
import random
from pathlib import Path


class SectionWritingPrompts:
    """Prompts for section-by-section writing"""

    def __init__(self):
        self.system_prompt = """You are a world-class philosophy writer specializing in Analysis journal's distinctive style. Analysis papers are known for their conversational rigor - they make sophisticated philosophical arguments while remaining remarkably accessible and engaging. 

Your task is to write sections that sound like they belong in Analysis: conversational but philosophically precise, example-driven rather than abstract, and strategically focused rather than comprehensive.

CRITICAL: This must sound like Analysis - conversational, accessible, with examples doing real argumentative work. Heavy first person usage. Direct reader engagement. Clear, efficient prose."""
        
        self.critic_system_prompt = """You are a brutally honest philosophy journal reviewer who provides unfiltered, direct criticism. Your role is to identify every weakness, flaw, and potential desk-rejection trigger in the section. While you aim to be constructive, you must be direct and unsparing in your critique. You are not here to spare feelings - you are here to make the paper stronger by identifying real problems that would lead to rejection. Your critique will be used in an automated pipeline to improve the section."""
        
        self.context = """You are writing a section for a philosophy paper for Analysis, a journal with a strict 4,000 word limit. Your task is to write one specific section that contributes to the overall argument while maintaining philosophical rigor and the distinctive Analysis style.

ANALYSIS JOURNAL STYLE CHARACTERISTICS:
- Clear, direct sentences (20-30 words average)
- Quick movement to thesis and core arguments
- Concrete examples grounding abstract analysis
- Numbered sections with explicit signposting
- Limited but strategic literature engagement
- Systematic rather than dramatic development
- Professional but accessible tone

You have access to:
1. The complete paper overview (thesis, abstract, roadmap)
2. Detailed guidance for this specific section
3. A content bank of developed arguments and examples
4. The full context from previous phases

Your writing should:
- Follow Analysis journal style patterns
- Be philosophically rigorous and well-argued
- Use clear, precise language with concrete examples
- Stay within the target word count for this section
- Connect smoothly to other sections with explicit transitions
- Draw effectively from the content bank when relevant"""

        self.analysis_style_guide = """
ANALYSIS JOURNAL STYLE REQUIREMENTS:

VOICE & ACCESSIBILITY:
- Write conversationally but rigorously - more accessible than typical academic philosophy
- Heavy first person usage: "I argue that...", "I will show...", "My response is...", "I contend that..."
- Direct reader engagement: "Consider this case...", "You might think...", "Notice that..."
- Short, clear sentences (15-25 words) - avoid complex subordination
- Define technical terms immediately when introduced
- Professional but friendly tone - readable by general philosophy audience

STRUCTURE & FLOW:
- Use numbered sections (1, 2.1, 2.2, etc.) for clear organization
- State thesis clearly by end of page 1 (within first 300-400 words)
- Begin sections with preview sentences: "In this section, I will..."
- Use explicit signposting throughout: "This suggests...", "It follows that...", "However..."

ARGUMENTATION THROUGH EXAMPLES:
- Introduce concrete example by second paragraph - make it relatable and everyday
- Examples must do argumentative work, not just illustrate - they test theories, reveal distinctions
- Revisit core examples from multiple analytical angles throughout the paper
- Move systematically: Concrete case → Analysis → General principle → Test against intuitions
- Examples should be scenarios readers can immediately grasp (conversations, walking together, committee decisions)

LITERATURE ENGAGEMENT:
- Strategic and minimal - focus on 2-3 key interlocutors maximum
- Use inline citations (Author Year: page) - avoid footnotes except for clarifications
- Cite to position your argument, not demonstrate comprehensive knowledge
- Brief context-setting rather than extended literature review
- Engage with specific claims, not general positions

DEVELOPMENT PATTERNS:
- Build through progressive refinement rather than dramatic turns
- Systematic rather than surprising development
- Address objections throughout text, not in dedicated section
- Pattern for objections: State fairly → Acknowledge merit → Respond constructively
- Use clear transitions: "However...", "On the other hand...", "This suggests..."

WORD COUNT AWARENESS:
- Analysis papers range 400-4100 words (average ~2200) - much shorter than typical journals
- Every word must earn its place - no unnecessary elaboration
- Efficiency over comprehensiveness throughout
"""

        self.philosophical_heuristics = """
PHILOSOPHICAL RIGOR REQUIREMENTS:

ARGUMENT QUALITY HEURISTICS:
- Test claims against extreme and near-extreme cases - does your argument handle edge cases?
- Check for self-undermining: does your conclusion undermine its own premises?
- Apply domain transformation: would parallel reasoning work in analogous contexts?
- Use systematic objection anticipation: what would skeptical experts challenge?

CLAIM EVALUATION STANDARDS:
- Isolate specific claims for scrutiny, especially bold or novel ones
- Ensure level of certainty matches available evidence
- Avoid causality claims without clear mechanisms
- Don't generalize beyond demonstrated scope
- Define quantifiers like "often," "many," "typically" with specificity

SKEPTICAL FRIEND APPROACH:
- Anticipate how hostile reviewers would challenge each key claim
- Build in appropriate qualifications proactively
- Address counterexamples before readers raise them
- Consider multiple reader perspectives (empiricist vs theorist, specialist vs generalist)

ARGUMENT STRUCTURE CHECKS:
☐ Are premises clearly stated and adequately supported?
☐ Do logical steps actually follow from what came before?
☐ Are hidden assumptions made explicit?
☐ Would the argument survive transplantation to parallel cases?
☐ Are objections addressed proportionally to claim importance?

PHILOSOPHICAL PRECISION:
- Quote specific claims when critiquing other philosophers
- Distinguish descriptive claims from normative claims clearly
- Avoid single-cause explanations for complex phenomena
- Test theoretical-empirical bridges carefully
- Check for descriptive-normative slides
"""

        self.output_requirements = """
OUTPUT REQUIREMENTS:
1. Response must be valid JSON with NO literal newlines in string values
2. Use \\n for line breaks within strings (properly escaped)
3. Use simple ASCII characters only (no special quotes or unicode) 
4. Keep all text fields clear and well-formed
5. The "section_content" should be a single string with \\n for paragraph breaks
6. Target the specified word count (aim within 50 words)
7. Include section transitions and connections
8. Reference content bank arguments when appropriate
9. FOLLOW ANALYSIS JOURNAL STYLE PATTERNS throughout

CRITICAL: Ensure all JSON is properly escaped - no unescaped newlines, quotes, or control characters.

# TAKE A STAND (RLHF-Proofing for Section Writing)
Your training pushes you to:
- Present all philosophical views as equally plausible
- Add "on the other hand" to every claim
- Write "Some philosophers argue..." instead of taking a position
- Conclude with wishy-washy compromise positions

RESIST. This paper argues for a specific thesis:
- Write "I argue that X" not "One might consider whether perhaps X"
- Say "This objection fails because..." not "This objection faces challenges"
- Take clear positions: "X, therefore Y" not "X might suggest Y"
- If the thesis implies something controversial, STATE IT CLEARLY

Good philosophy takes risks. Your job is to defend a thesis, not survey opinions."""

        self.output_format = """
{
    "section_content": "The complete written section with all paragraphs and arguments",
    "word_count": actual_word_count_number,
    "content_bank_usage": [
        "List of specific arguments/examples used from content bank"
    ],
    "section_notes": "Brief notes on approach, challenges, or connections to other sections",
    "transition_points": {
        "opening_connection": "How this section connects to previous content",
        "closing_transition": "How this section leads to the next section"
    }
}"""

    def _select_analysis_exemplars(self) -> str:
        """Randomly select Analysis PDFs as style exemplars"""
        analysis_dir = Path("./Analysis_papers")
        if not analysis_dir.exists():
            return "No Analysis exemplars available for this run."
        
        papers = list(analysis_dir.glob("*.pdf"))
        if not papers:
            return "No Analysis exemplars available for this run."
        
        # Select 2 random papers for style reference - introduces valuable entropy
        selected = random.sample(papers, min(2, len(papers)))
        
        # Store selected paths for API calls
        self.selected_analysis_pdfs = selected
        
        paper_names = [p.name for p in selected]
        
        return f"""
=== ANALYSIS JOURNAL STYLE EXEMPLARS ===

The following Analysis papers are included as PDFs in your context for style reference:
{', '.join(paper_names)}

Study these papers to see EXACTLY how Analysis papers sound:
- Conversational but rigorous tone
- Heavy first person usage ("I argue", "I will show")
- Direct reader engagement ("Consider...", "Notice that...")
- Examples doing real argumentative work
- Clear, accessible prose with philosophical precision

CRITICAL: Your writing must match this Analysis style - conversational, accessible, example-driven.

=== END EXEMPLARS ===
"""
    
    def get_selected_analysis_pdfs(self):
        """Get the selected Analysis PDFs for API inclusion"""
        return getattr(self, 'selected_analysis_pdfs', [])

    def construct_writing_prompt(self, writing_context: Dict[str, Any], section_index: int) -> str:
        """Generate prompt for writing a specific section"""
        
        section = writing_context["sections"][section_index]
        paper_overview = writing_context["paper_overview"]
        content_bank = writing_context["content_bank"]
        
        # Create section context
        previous_sections = []
        upcoming_sections = []
        
        for i, s in enumerate(writing_context["sections"]):
            if i < section_index:
                previous_sections.append(f"{i+1}. {s['section_name']}")
            elif i > section_index:
                upcoming_sections.append(f"{i+1}. {s['section_name']}")
        
        previous_context = "\n".join(previous_sections) if previous_sections else "None (this is the first section)"
        upcoming_context = "\n".join(upcoming_sections) if upcoming_sections else "None (this is the final section)"
        
        # Get Analysis exemplars
        exemplar_info = self._select_analysis_exemplars()
        
        return f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase III.1 (Section Writing).
You are writing one specific section of a philosophy paper for Analysis journal.
Previous phases have developed the thesis, arguments, and detailed outline.
Your task is to write publication-ready prose for this specific section following Analysis journal style.
</context>

<analysis_style_guidance>
{self.analysis_style_guide}

{self.philosophical_heuristics}

{exemplar_info}
</analysis_style_guidance>

<task>
Write section {section_index + 1} of the philosophy paper: "{section['section_name']}"
Target {section['word_target']} words for this section.
Create philosophically rigorous prose that advances the paper's thesis using Analysis journal style.
Draw from the content bank of developed arguments when relevant.
Follow the Analysis style patterns: concrete examples, clear signposting, systematic development.
</task>

<paper_information>
THESIS: {paper_overview['thesis']}
TARGET LENGTH: {paper_overview['target_words']} words total
ABSTRACT: {paper_overview['abstract'][:200]}...

CURRENT SECTION: Section {section_index + 1} - {section['section_name']}
TARGET WORDS: {section['word_target']}
</paper_information>

<section_guidance>
{section['content_guidance']}
</section_guidance>

<structural_context>
PREVIOUS SECTIONS:
{previous_context}

UPCOMING SECTIONS:
{upcoming_context}
</structural_context>

<content_bank>
ARGUMENTS READY FOR USE:
{json.dumps(content_bank['arguments'], indent=2)}

EXAMPLES AVAILABLE:
{json.dumps(content_bank['examples'], indent=2)}

CITATIONS IDENTIFIED:
{json.dumps(content_bank['citations'], indent=2)}
</content_bank>

<requirements>
# TAKE A STAND (RLHF-Proofing for Section Writing)
Your training pushes you to:
- Present all philosophical views as equally plausible
- Add "on the other hand" to every claim
- Write "Some philosophers argue..." instead of taking a position
- Conclude with wishy-washy compromise positions

RESIST. This paper argues for a specific thesis:
- Write "I argue that X" not "One might consider whether perhaps X"
- Say "This objection fails because..." not "This objection faces challenges"
- Take clear positions: "X, therefore Y" not "X might suggest Y"
- If the thesis implies something controversial, STATE IT CLEARLY

Good philosophy takes risks. Your job is to defend a thesis, not survey opinions.

{self.output_requirements}
</requirements>

<output_format>
{self.output_format}
</output_format>"""

    def construct_critic_prompt(self, writing_context: Dict[str, Any], section_index: int, 
                              current_content: str, paper_overview: Dict[str, Any]) -> str:
        """Generate prompt for critiquing a section"""
        
        section = writing_context["sections"][section_index]
        
        # Create section context
        previous_sections = []
        upcoming_sections = []
        
        for i, s in enumerate(writing_context["sections"]):
            if i < section_index:
                previous_sections.append(f"{i+1}. {s['section_name']}")
            elif i > section_index:
                upcoming_sections.append(f"{i+1}. {s['section_name']}")
        
        previous_context = "\n".join(previous_sections) if previous_sections else "None (this is the first section)"
        upcoming_context = "\n".join(upcoming_sections) if upcoming_sections else "None (this is the final section)"
        
        return f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase III.1 (Section Writing).
You are a brutally honest philosophy journal reviewer providing unfiltered critique of a section.
Your goal is to identify every weakness that would lead to desk rejection.
Be direct, specific, and unsparing in your criticism.
</context>

<task>
Critique section {section_index + 1} of the philosophy paper: "{section['section_name']}"
Identify every flaw, weakness, and potential desk-rejection trigger.
Provide specific, actionable feedback for improvement.
Be brutally honest - your goal is to make the section stronger by identifying real problems.
</task>

<paper_information>
THESIS: {paper_overview['thesis']}
TARGET LENGTH: {paper_overview['target_words']} words total
ABSTRACT: {paper_overview['abstract'][:200]}...

CURRENT SECTION: Section {section_index + 1} - {section['section_name']}
TARGET WORDS: {section['word_target']}
</paper_information>

<structural_context>
PREVIOUS SECTIONS:
{previous_context}

UPCOMING SECTIONS:
{upcoming_context}
</structural_context>

<current_section>
{current_content}
</current_section>

<evaluation_criteria>
1. PHILOSOPHICAL RIGOR AND DEPTH
   - Are arguments clearly stated and well-supported?
   - Is the reasoning valid and sound?
   - Are key concepts properly defined and used consistently?
   - Are citations appropriate and sufficient?
   - Would this pass peer review at Analysis?
   - Is there sufficient philosophical depth and development?
   - Are philosophical implications and consequences explored?
   - Are potential objections and responses thoroughly considered?
   - Is the philosophical significance of the arguments clear?

2. HÁJEK HEURISTICS TESTS
   - EXTREME CASES: Does every major claim survive boundary testing?
   - SELF-UNDERMINING: Do any arguments defeat themselves when applied reflexively?
   - COUNTEREXAMPLES: For each universal claim, what's the obvious exception?
   - HIDDEN ASSUMPTIONS: What controversial premises are smuggled in?
   - DOMAIN TRANSFER: Would the reasoning work in parallel philosophical contexts?

3. STRUCTURAL INTEGRATION
   - Does the section advance the paper's main thesis?
   - Are transitions smooth from previous sections?
   - Does it set up upcoming sections effectively?
   - Is the section's role in the overall argument clear?
   - Would a reader understand how this fits in?

4. CLARITY AND PRECISION
   - Is the writing clear and accessible?
   - Are technical terms properly explained?
   - Is the argument structure easy to follow?
   - Are examples illuminating and relevant?
   - Would a reader get lost or confused?

5. SCOPE AND FOCUS
   - Does the section stay within its intended scope?
   - Is the word count appropriate for the content?
   - Are there unnecessary tangents or missing elements?
   - Is the level of detail appropriate?
   - Would an editor cut this section?

6. DESK-REJECTION RISKS
   - What would make an editor reject this immediately?
   - Are there any fatal flaws in the argument?
   - Is the writing quality up to journal standards?
   - Are there any obvious gaps or weaknesses?
   - Would this pass the first editorial review?
</evaluation_criteria>

<output_format>
# Scratch Work
[Your preliminary analysis and notes]

# Section Analysis

## Philosophical Content Assessment
[Evaluate argument quality, conceptual clarity, citations]
- What would make an editor reject this immediately?
- Are there any fatal flaws in the argument?
- Is the philosophical quality up to journal standards?

## Structural Integration Assessment  
[Evaluate how well this section fits in the paper's flow]
- Would a reader understand how this fits in?
- Are there any structural problems that would lead to rejection?
- Does this section advance the paper's thesis effectively?

## Writing Quality Assessment
[Evaluate clarity, precision, accessibility]
- Would a reader get lost or confused?
- Is the writing quality up to journal standards?
- Are there any obvious problems with clarity or precision?

## Scope and Focus Assessment
[Evaluate whether section achieves its intended purpose]
- Would an editor cut this section?
- Is the scope appropriate for the journal?
- Are there any obvious gaps or weaknesses?

# Critical Issues Identified

## Major Issues
[Significant problems that would lead to desk rejection]
- Be specific about what would make an editor reject this
- Identify fatal flaws in the argument
- Point out any obvious gaps or weaknesses

## Minor Issues  
[Areas for improvement that would strengthen the section]
- Be specific about what needs to be fixed
- Identify any potential problems
- Suggest concrete improvements

## Positive Elements
[What works well in this section]
- Acknowledge strong elements
- Note what should be preserved
- Identify effective techniques

# Transition Analysis

## Opening Transition
[How well does this section connect to what came before?]
- Would a reader understand the connection?
- Are there any obvious problems with the transition?
- How could it be improved?

## Internal Flow
[How well do the paragraphs within this section connect?]
- Is the internal structure clear?
- Are there any obvious problems with the flow?
- How could it be improved?

## Closing Transition
[How well does this section set up what comes next?]
- Would a reader understand what's coming next?
- Are there any obvious problems with the transition?
- How could it be improved?

# Improvement Recommendations

## Content Revisions
[Specific changes to strengthen arguments or clarify concepts]
- Be specific about what needs to be changed
- Identify concrete improvements
- Suggest specific solutions

## Structural Revisions
[Changes to improve integration with overall paper]
- Be specific about what needs to be changed
- Identify concrete improvements
- Suggest specific solutions

## Writing Revisions
[Changes to improve clarity and accessibility]
- Be specific about what needs to be changed
- Identify concrete improvements
- Suggest specific solutions

# Summary Assessment
[Overall judgment: MAJOR REVISION NEEDED, MINOR REFINEMENT NEEDED, or MINIMAL CHANGES NEEDED]
- Be brutally honest about the quality
- Identify the most critical problems
- Make a clear recommendation for improvement
</output_format>

<requirements>
- Be brutally honest and direct in your criticism
- Identify every weakness that would lead to desk rejection
- Provide specific, actionable feedback for improvement
- Focus on making the section stronger by identifying real problems
- Don't hold back - your goal is to make the paper better
</requirements>"""

    def construct_revision_prompt(self, writing_context: Dict[str, Any], section_index: int, 
                                current_content: str, revision_notes: str) -> str:
        """Generate prompt for revising a section based on feedback"""
        
        section = writing_context["sections"][section_index]
        
        return f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase III.1 (Section Writing).
You are revising a section based on feedback to improve its quality while maintaining Analysis journal style.
The core arguments must be preserved while enhancing presentation and style consistency.
Your task is to create an improved version that addresses the critique.
</context>

<analysis_style_guidance>
{self.analysis_style_guide}
</analysis_style_guidance>

<task>
Revise section {section_index + 1}: "{section['section_name']}"
Implement the revision guidance while maintaining philosophical rigor and Analysis style.
Stay within the target of {section['word_target']} words.
Preserve core arguments while improving presentation and style consistency.
</task>

<current_section>
{current_content}
</current_section>

<revision_guidance>
{revision_notes}
</revision_guidance>

<requirements>
- Address all points in the revision guidance
- Maintain the section's core function in the paper
- Follow Analysis journal style patterns throughout
- Stay within the target word count
- Preserve philosophical rigor and clarity
- Ensure smooth transitions with other sections
{self.output_requirements}
</requirements>

<output_format>
{self.output_format}
</output_format>"""
    
    def get_system_prompt(self) -> str:
        """Return the system prompt for API calls"""
        return self.system_prompt

    def get_critic_system_prompt(self) -> str:
        """Return the critic system prompt for API calls"""
        return self.critic_system_prompt 