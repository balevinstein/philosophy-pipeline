# src/prompts/generate.py

class TopicGenerationPrompt:
    """Manages prompts for topic generation"""
    
    def __init__(self):
        self.CORE_PRINCIPLES = """
CORE PRINCIPLES:
- Papers should make a single, clear philosophical contribution
- Arguments must be precise (whether formal or informal)
- Length is strictly limited (3,000-4,000 words)
- Engagement with literature should be focused
- Quality of argument matters more than methodology"""

        self.SUCCESSFUL_APPROACHES = """
DIVERSITY OF SUCCESSFUL APPROACHES:
Not every successful Analysis paper needs the same characteristics. Papers succeed through different combinations of strengths:

1. Pure Conceptual Analysis
   Example: 'Against the No-Difference Argument' (Elga, 2024)
   - Clear counterexample to accepted view
   - Minimal formal apparatus
   - Precise argumentation without technical tools
   - Value from exposing flaws in common reasoning

2. Novel Formal Treatment
   Example: 'Counterfactuals and Indeterminate Possibility' (Werner, 2024)
   - New technical approach to known problem
   - Careful formal development
   - Clear philosophical payoff
   - Value from systematic treatment

3. Puzzle Identification
   Example: 'A Puzzle About Weak Belief' (Pearson, 2024)
   - Reveals new philosophical tension
   - May be largely informal
   - Precise articulation of the problem
   - Value from exposing important difficulties

4. Unexpected Connections
   Example: 'Can the Dimples on a Golf Ball Be Evenly Spaced?' (Brown, 2024)
   - Links between distinct philosophical issues
   - May use varying levels of formality
   - Clear philosophical significance
   - Value from novel insight"""

        self.GOOD_PAPER_FEATURES = """
WHAT MAKES A GOOD ANALYSIS PAPER:
1. Essential Features
   - Novel philosophical insight
   - Precise argumentation
   - Clear significance
   - Manageable scope
   - Focused engagement with literature

2. Optional Features (papers may include some but need not include all)
   - Formal logical apparatus
   - Technical innovations
   - Mathematical modeling
   - Detailed literature review
   - Complex theoretical framework"""

        self.AREAS_TO_AVOID = """
AREAS TO AVOID:
1. Primarily historical or exegetical work
2. Topics requiring extensive empirical evidence
3. Broad survey-style treatments
4. Topics too large for 4,000 words
5. Purely negative critiques without constructive element"""

        self.LITERATURE_ENGAGEMENT = """
LITERATURE ENGAGEMENT:
- Focus on at most 2-3 key recent papers
- Clear point of departure from existing work
- Precise engagement with specific arguments
- Show why current solutions inadequate
- Demonstrate clear advance"""

        self.OUTPUT_FORMAT = """
Your response must be a JSON array of topics. Specifically:
1. Use square brackets [] to contain all topics
2. Each topic should be an object with the following structure
3. DO NOT use "topic1", "topic2" etc. - just put the objects directly in an array

Example format:
[
    {
        "title": "First Topic Title",
        "type": "Puzzle Identification",
        [rest of first topic structure]
    },
    {
        "title": "Second Topic Title",
        "type": "Conceptual Analysis",
        [rest of second topic structure]
    }
]

Each topic object should have this structure:
{
    "title": "string",
    "type": "string",
    "formal_apparatus": "string",
    "core_contribution": {
        "insight": "string",
        "significance": "string",
        "advancement": "string"
    },
    "argument_structure": {
        "premises": ["string"],
        "conclusion": "string",
        "key_moves": ["string"]
    },
    "literature_connection": {
        "key_papers": ["string"],
        "advancement": "string"
    },
    "development_strategy": {
        "steps": ["string"],
        "objections": ["string"],
        "responses": ["string"]
    },
    "viability": {
        "scope": "string",
        "novelty": "string",
        "challenges": "string"
    }
}"""

    def get_prompt(self, num_topics: int) -> str:
        """Construct the full prompt"""
        return f"""You are assisting in generating potential paper topics for Analysis, one of the most prestigious journals in analytic philosophy. Generate {num_topics} potential paper topics.

{self.CORE_PRINCIPLES}

{self.SUCCESSFUL_APPROACHES}

{self.GOOD_PAPER_FEATURES}

{self.AREAS_TO_AVOID}

{self.LITERATURE_ENGAGEMENT}

{self.OUTPUT_FORMAT}

Your response must start with [ and end with ], containing exactly {num_topics} topic objects."""