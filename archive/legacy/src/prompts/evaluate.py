# src/prompts/evaluate.py

class TopicEvaluationPrompt:
    """Manages prompts for topic evaluation and culling"""
    
    def __init__(self):
        self.CONTEXT = """
CONTEXT:
These topics will be developed entirely through a series of LLM (Large Language Model) interactions. The final paper will be written by AI systems, so we need topics that play to LLM strengths and avoid their weaknesses."""

        self.LLM_CAPABILITIES = """
LLM STRENGTHS:
- Logical analysis and formal reasoning
- Identifying conceptual tensions and paradoxes
- Systematic evaluation of arguments
- Clear exposition of defined concepts
- Working with explicit premises and conclusions
- Finding connections between clearly stated ideas

LLM WEAKNESSES:
- Heavy reliance on recent or obscure literature
- Deeply original conceptual innovation
- Complex historical interpretation
- Detailed empirical analysis
- Subtle linguistic intuitions
- Heavy context-dependent reasoning"""

        self.JOURNAL_REQUIREMENTS = """
ANALYSIS JOURNAL REQUIREMENTS:
- Papers must be 3,000-4,000 words
- Need clear, single philosophical contribution
- Require precise argumentation
- Must engage with relevant literature
- Should advance philosophical understanding"""

        self.EVALUATION_CRITERIA = """
EVALUATION CRITERIA:
1. **AI Feasibility**:
   - Can this topic be effectively handled by LLMs?
   - Does it play to AI strengths rather than weaknesses?
   - Is the required knowledge base manageable?

2. **Philosophical Merit**:
   - Is there a clear, novel contribution?
   - Is the philosophical significance evident?
   - Is the argument structure promising?

3. **Practical Viability**:
   - Can this fit in 4,000 words?
   - Is the literature engagement manageable?
   - Are the key moves clear and executable?"""

        self.OUTPUT_FORMAT = """
Sort topics into three categories:
- DEVELOP: High potential for AI development, clear philosophical merit, manageable scope
- POSSIBLE: Has promise but faces significant challenges for AI development
- REJECT: Poor fit for AI capabilities or other clear problems

Your response must be a JSON object with this structure:
{
    "categorized_topics": {
        "develop": [
            {
                "title": "string",
                "quick_assessment": "string",
                "ai_strengths_alignment": "string",
                "key_philosophical_merit": "string",
                "main_challenge": "string"
            }
        ],
        "possible": [...],
        "reject": [...]
    },
    "culling_rationale": "string",
    "ai_development_recommendations": "string"
}"""

    def get_prompt(self, topics_json: str) -> str:
        """Construct the full evaluation prompt"""
        return f"""You are an expert in analytic philosophy tasked with quickly identifying the most promising paper topics for Analysis journal from a given set. This is an initial culling phase to identify which topics deserve further development.

{self.CONTEXT}

{self.LLM_CAPABILITIES}

{self.JOURNAL_REQUIREMENTS}

{self.EVALUATION_CRITERIA}

{self.OUTPUT_FORMAT}

Be ruthlessly practical: we need topics that can realistically be developed into strong papers through AI interaction.

Here are the topics for evaluation:
{topics_json}"""