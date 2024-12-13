# src/prompts/conceptual_generate.py

class TopicGenerationPrompt:
    """Manages prompts for conceptual philosophy paper topic generation"""
    
    def __init__(self):
        self.SUCCESSFUL_APPROACHES = """
SUCCESSFUL APPROACHES IN ANALYSIS:
Papers succeed through different combinations of these elements, but all make focused conceptual contributions. Consider these approaches:

1. Conceptual Distinction Drawing
   Example: 'Two Kinds of Failure in Joint Action' 
   - Identifies distinct phenomena previously conflated
   - Shows why the distinction matters
   - Careful analysis using clear examples 
   - Value comes from improved conceptual clarity 

2. Concept Refinement/Revision
   Example: 'Microaggression and Ambiguous Experience'
   - Challenges standard understanding of a concept
   - Demonstrates problems with existing account
   - Proposes more precise analysis
   - Value comes from better theoretical understanding

3. Novel Analytical Framework  
   - Introduces new way to analyze familiar phenomena
   - Shows how framework illuminates existing debates
   - Uses minimal technical apparatus
   - Value comes from fresh analytical perspective

Key features of successful approaches:
- Focus on specific conceptual issues
- Use clear examples to motivate analysis 
- Maintain tight scope
- Develop arguments systematically
- Engage literature without getting bogged down"""

        self.GOOD_PAPER_FEATURES = """
WHAT MAKES A GOOD ANALYSIS PAPER:
1. Core Requirements
   - Clear, focused conceptual contribution
   - Arguments that can be developed in under 4,000 words
   - Minimal technical apparatus
   - Precise but accessible prose
   - Engagement with key literature

2. Common Valuable Elements
   - Identifies tension or problem in existing views
   - Introduces useful distinction
   - Provides illuminating examples
   - Anticipates main objections
   - Shows broader implications"""

        self.AREAS_TO_AVOID = """
AREAS TO AVOID:
1. Topics requiring extensive formal apparatus
2. Historically-focused interpretive work
3. Topics needing substantial empirical support
4. Arguments that can't be developed in 4,000 words
5. Purely negative critiques
6. Topics requiring extensive literature review
7. Attempts to solve major long-standing problems
8. Topics needing mathematical/technical innovations"""

        self.CONTRIBUTION_GUIDANCE = """
DEVELOPING PROMISING CONTRIBUTIONS:
1. Novelty Sweet Spot
   - Look for unexplored tensions in existing debates
   - Find new applications for established conceptual tools
   - Identify overlooked distinctions 
   - Propose targeted solutions to specific problems
   - Balance originality with achievability

2. What Makes it Publishable
   - Advances understanding of important concepts
   - Resolves recognized difficulties
   - Opens new analytical perspectives
   - Helps clarify existing debates
   - Makes progress on tractable problems

3. Viability Indicators
   - Can be explained clearly and concisely
   - Requires minimal technical setup
   - Uses accessible examples
   - Has clear development path
   - Responds to real philosophical needs"""

        self.SCOPE_AND_DEVELOPMENT = """
APPROPRIATE SCOPE FOR ANALYSIS:
1. Right-Sized Contributions
   - Single clear conceptual advance
   - Focused argumentative strategy
   - Manageable in 4,000 words
   - Self-contained analysis
   - Limited technical requirements

2. Development Considerations
   - Core argument needs minimal setup
   - Key moves can be explained clearly
   - Examples illuminate without dominating
   - Objections can be handled concisely
   - Implications follow straightforwardly"""
        
        self.OUTPUT_FORMAT = """
OUTPUT FORMAT REQUIREMENTS:

1. Response Structure:
- Must be a valid JSON array of topic objects
- Each topic must follow the exact structure below
- Avoid special characters (quotes, unicode) in text fields
- Use simple ASCII characters only
- Keep all text fields as single-line strings (no line breaks)

2. Topic Object Structure:
{
    "title": "string (clear and direct title)",
    "core_contribution": {
        "conceptual_issue": "string describing the problem/tension",
        "proposed_solution": "string describing the advance",
        "significance": "string explaining importance"
    },
    "novelty": {
        "what_is_new": "string describing novel element",
        "why_publishable": "string explaining contribution",
        "why_achievable": "string explaining feasibility"
    },
    "scope_assessment": {
        "technical_requirements": "string (emphasize minimal formal apparatus)",
        "key_assumptions": ["array of string assumptions"],
        "literature_engagement": "string describing key papers/debates",
        "background_knowledge": ["array of key concepts/literature reader should understand"],
        "example_types": ["array of types of examples that would illustrate key points"]
    },
    "viability_assessment": {
        "conceptual_clarity": "string explaining core ideas",
        "development_risks": ["array of potential challenges"],
        "distinctive_advantages": ["array of unique strengths"]
    }
}

Example Excerpt:
{
    ...
    "scope_assessment": {
        "technical_requirements": "Basic conceptual analysis only",
        "key_assumptions": ["Moral beliefs have identifiable sources", "Sources affect agreement potential"],
        "literature_engagement": "Recent work on moral disagreement and belief formation",
        "background_knowledge": ["Basic moral epistemology", "Contemporary meta-ethics"],
        "example_types": ["Everyday moral disagreements", "Historical ethical debates"]
    }
    ...
}"""


    def get_prompt(self, num_topics: int) -> str:
        """Construct the full topic generation prompt"""
        return f"""You are assisting in generating potential paper topics for Analysis, one of the most prestigious journals in analytic philosophy. Generate {num_topics} potential paper topics that are conceptually focused and achievable within 4,000 words.

{self.SUCCESSFUL_APPROACHES}

{self.GOOD_PAPER_FEATURES}

{self.AREAS_TO_AVOID}

{self.CONTRIBUTION_GUIDANCE}

{self.SCOPE_AND_DEVELOPMENT}

{self.OUTPUT_FORMAT}

Your response must start with [ and end with ], containing exactly {num_topics} topic objects."""