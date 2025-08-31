# src/prompts/outline_prompts.py

from typing import Dict, Any, List, Optional

class OutlinePrompts:
    """Manages prompts for philosophical paper outline development"""
    
    
    def __init__(self):
        self.DEVELOPMENT_CONTEXT = """
CONTEXT:
You are helping develop a detailed philosophical paper outline for publication in Analysis, one of the most prestigious journals in analytic philosophy. 

ANALYSIS REQUIREMENTS:
- Papers must be 2,000-4,000 words
- Must make a single, clear philosophical contribution
- Requires precise argumentation
- Must engage thoughtfully but efficiently with literature
- Should advance philosophical understanding through careful analysis

While Analysis papers can succeed through different combinations of elements, all successful papers share:
- Clear, focused argumentation
- Precise development of key ideas
- Efficient use of space
- Convincing defense against objections
- Sharp and precise prose
- NOVEL and ORIGINAL contribution to the field

Optional elements that may strengthen the paper when appropriate:
- Formal logical apparatus
- Technical innovations
- Carefully chosen examples
- Mathematical modeling
- Detailed case studies

The development process should strengthen core argumentative elements while thoughtfully developing optional elements where they serve the paper's goals."""

        self.SYNTHESIS_CONTEXT = """
SYNTHESIS TASK:
You are the strategic coordinator for developing a philosophical paper for Analysis journal. Your role is to maintain coherence and direction across different aspects of development (argument structure, examples, formal framework, and objections).

Key Responsibilities:
- Monitor adherence to Analysis paper requirements (3,000-4,000 words, clear contribution)
- Ensure consistency across different development aspects
- Identify potential issues early
- Keep development aligned with original thesis and goals

The synthesis you provide will guide the next cycle of development, so focus on what's most important for maintaining coherent progress."""

    



        # Define development aspects (preserved from original)
        self.ASPECT_GUIDELINES = {
            "argument_structure": """
TASK:
Based on the selected paper's core thesis and development rationale, write the argument structure that will appear in the paper.

1. Review and incorporate:
   - The paper's central thesis
   - Key claims identified in previous development
   - Selected development path
   - Established literature connections

2. Then provide the complete logical structure:
   - Precise premise statements
   - Clear intermediate conclusions
   - Final conclusion
   - Logical connections between steps

Format your response in clear markdown with:
- Numbered premises and conclusions
- LaTeX notation where needed ($...$ for inline, $$....$$ for display)
- Clear explanation of logical connections
- Explicit identification of assumptions

Focus on providing publication-ready content that could be directly used in the paper.""",

            "example_development": """
TASK:
Based on the selected paper's core thesis and argument structure, develop examples that will demonstrate and support its key claims.

1. Review and incorporate:
   - The paper's core theoretical claims
   - Identified tensions or puzzles
   - Required technical/formal elements
   - Target success criteria

2. Then provide:
   - Primary examples demonstrating core phenomena/arguments
   - Supporting examples showing scope and implications
   - Technical details and notation where needed
   - Clear connections to main argumentative thread

Format in clear markdown with:
- Clear section headings
- LaTeX notation where needed
- Explicit connections to arguments
- Complete, publication-ready prose""",

"formal_framework": """
TASK:
Based on the selected paper's formal requirements and theoretical goals, develop the technical framework needed to support its arguments.

1. Review and incorporate:
   - Required formal apparatus identified in prior development
   - Technical definitions needed
   - Theoretical constraints to be satisfied
   - Target level of formal sophistication

2. Then provide:
   - Complete formal definitions
   - Necessary axioms or assumptions
   - Key theorems or lemmas
   - Essential proofs
   - Integration with philosophical claims

Format using:
- Clear markdown structure
- LaTeX for formal notation
- Explicit numbering for definitions/theorems
- Complete technical details""",

"objection_mapping": """
TASK:
Based on the selected paper's claims and development strategy, map out potential objections and responses.

1. Review and incorporate:
   - Core thesis and key claims
   - Identified potential pitfalls
   - Critical assumptions
   - Success criteria for responses

2. Then provide:
   - Principal objections with detailed development
   - Comprehensive responses
   - Technical support where needed
   - Integration with main argument

Format in clear markdown with:
- Explicit structure
- LaTeX where needed
- Complete, publication-ready text""",

"integration": """
TASK:
Based on the paper's developed components, write the connecting content that will integrate them into a cohesive whole.

1. Review and incorporate:
   - Argument structure 
   - Example development
   - Formal framework
   - Objections and responses

2. Then provide:
   - Section transitions
   - Cross-references
   - Technical links
   - Narrative thread development

Format in clear markdown with:
- Clear section markers
- Explicit connections
- Complete, publication-ready prose"""
        }

    def get_synthesis_prompt(self, outlines: List[str], current_state: Dict[str, Any]) -> str:
        """Generate synthesis prompt"""
        return f"""
{self.SYNTHESIS_CONTEXT}

Take a step back and provide a high-level, concise synthesis (max 500 words) of the project's current state.

Focus on key strategic elements:

1. Overall Progress (2-4 sentences)
- Main argument's current shape
- Core technical/formal commitments made
- Primary examples selected

2. Alignment Check (2-4 bullet points)
Original Thesis: {current_state['core_analysis']['central_thesis']}
Key Claims: {current_state['core_analysis']['key_claims']}
- Note any drift from these goals
- Identify any tension with original aims

3. Critical Issues (0-3 highest priority items)
- Major gaps or inconsistencies
- Areas needing reconciliation
- Most pressing development needs

Remember: Be concise and strategic. Focus only on what's most important for maintaining coherent development.

Current outlines:
{outlines}
"""

    def get_development_prompt(self, aspect: str, current_content: str, cycle: int = 1) -> str:
        """Get development prompt for specific aspect, with cycle awareness"""
        
        if cycle == 1:
            # Original first-cycle prompt
            return f"""
    {self.DEVELOPMENT_CONTEXT}

    You are developing the {aspect} of a philosophical paper.

    Current outline content:
    {current_content}

    Write your response in clean, publication-ready markdown format. Include:
    - Clear section headers using # syntax
    - LaTeX notation where needed, enclosed in $$ for display math or $ for inline
    - Clear example text
    - Formal definitions and arguments as needed

    {self.ASPECT_GUIDELINES[aspect]}"""
        else:
            # Refinement prompt for subsequent cycles
            refinement_context = f"""
    REFINEMENT TASK:
    You are improving an existing philosophical paper outline. The previous content represents the {aspect} development from earlier cycles.

    Your task is to review and improve the existing outline:
    1. Strengthen and clarify existing arguments
    2. Improve formal precision and notation where appropriate
    3. Enhance connections between sections
    4. Fix any logical gaps or inconsistencies
    5. Maintain consistent focus on the paper's core thesis

    Current outline content to improve:
    {current_content}

    DO NOT:
    - Change the fundamental topic or thesis
    - Introduce unrelated theoretical frameworks
    - Drift from the established focus and arguments

    Provide refined content in clean markdown format with:
    - Clear section headers using # syntax
    - LaTeX notation where needed
    - Explicit connections to the core thesis
    - Improved clarity and precision while maintaining the original structure

    {self.ASPECT_GUIDELINES[aspect]}"""

        return refinement_context


    def get_critique_prompt(self, content: str, aspect: str) -> str:
        """Get critique prompt for specific content"""
        return f"""
You are evaluating philosophical content for technical accuracy, clarity, and philosophical insight.

Content to evaluate:
{content}

Provide specific feedback on:
1. Technical Accuracy
2. Philosophical Clarity
3. Argument Structure
4. Integration with Paper Goals

Format your response as:

# Technical Analysis
[Your analysis of technical elements]

# Philosophical Assessment
[Your assessment of philosophical contribution]

# Specific Improvements
[Concrete suggestions with examples]

# Integration Notes
[Notes on how this fits with the broader paper]

Think like an academic peer-reviewer or referee providing feedback that is constructive and fair, but potentially tough. If an idea is wrong or bad or unpromising, don't pull punches.

"""

    def get_refinement_prompt(self, content: str, critique: str, aspect: str) -> str:
        """Get refinement prompt based on critique"""
        return f"""
You are refining philosophical content based on critical feedback while maintaining technical precision and philosophical insight.

Original content:
{content}

Critique received:
{critique}

Provide refined content in clean markdown format that:
1. Addresses issues raised
2. Strengthens philosophical clarity
3. Improves argument structure
4. Maintains integration with paper goals

Your response should be publication-ready markdown text."""


    

    def get_metadata_prompt(self, content: str) -> str:
        """Simplified metadata prompt"""
        return f"""
    Analyze this outline content and provide a simple structural summary as JSON.
    Keep the structure minimal and focus only on essential tracking information.

    Required format:
    {{
        "section_count": number,
        "sections": [
            {{
                "title": "string",
                "word_estimate": number
            }}
        ],
        "total_words": number,
        "technical_elements": ["string"]
    }}"""