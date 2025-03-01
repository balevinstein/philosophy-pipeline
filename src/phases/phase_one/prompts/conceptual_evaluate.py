# src/prompts/conceptual_evaluate.py


class TopicEvaluationPrompt:
    """Manages prompts for evaluating philosophy paper topics"""

    def __init__(self, cull_min: int, cull_max: int):
        """Initialize prompt manager with culling parameters"""
        self.cull_min = cull_min
        self.cull_max = cull_max

        self.evaluation_principles = """
EVALUATION PRINCIPLES:
We are looking for topics that represent the right balance across multiple dimensions:

1. Contribution Level
   - Novel but not revolutionary
   - Clear advance in existing debates
   - Interesting without trying to solve major open problems
   - Professional and scholarly but not paradigm-shifting

2. Development Potential
   - Plays to LLM strengths in systematic reasoning
   - Takes LLMs to their edge without exceeding capabilities
   - Clear argumentative moves with room for sophistication
   - Examples that can be generated without being trivial

3. Literature Engagement
   - Clear point of departure from 2-3 key papers
   - Manageable background knowledge requirements
   - Room for scholarly depth without endless review
   - Natural connection to existing debates

4. Scope Management
   - Achievable in 4,000 words
   - Technical requirements within LLM capabilities
   - Example needs that are manageable
   - Clear but sophisticated argumentation"""

        self.evaluation_process = f"""
EVALUATION PROCESS:
For each topic:
1. Analyze core contribution
   - Assess novelty and significance
   - Evaluate current formulation
   - Identify potential improvements
   - Consider development pathways

2. Assess development potential
   - Alignment with LLM capabilities
   - Clarity of reasoning pathway
   - Example and technical requirements
   - Anticipated challenges

3. Evaluate literature needs
   - Identify key debates and papers
   - Consider engagement strategy
   - Assess background requirements
   - Flag any potential issues

4. Consider refinement opportunities
   - Possible core-preserving changes
   - Development suggestions
   - Scope adjustments
   - Strengthening approaches

After evaluating all topics:
1. Compare topics systematically
2. Identify key differentiators
3. Select {self.cull_min} to {self.cull_max} most promising topics
4. Rank selected topics
5. Provide clear rationales"""

        self.selection_guidance = f"""
SELECTION GUIDANCE:
Choose {self.cull_min} to {self.cull_max} topics that best balance:
1. Clear and novel contribution
2. Strong development potential
3. Manageable literature needs
4. Room for productive refinement

Favor topics that:
- Make clear conceptual distinctions
- Identify specific tensions
- Propose targeted solutions
- Use minimal technical machinery
- Have natural development paths

Avoid topics that:
- Require extensive literature review
- Need complex formal apparatus
- Depend heavily on specific examples
- Risk being too ambitious
- Lack clear development strategy"""

        self.output_requirements = """
1. Response Structure:
- Must be a valid JSON array of topic objects
- Each topic must follow the exact structure below
- Avoid special characters (quotes, unicode) in text fields
- Use simple ASCII characters only
- Keep all text fields as single-line strings (no line breaks)

Output must be valid JSON matching this structure exactly:
{
  "topic_evaluations": [
    {
      "title": "string",
      "core_analysis": {
        "original_contribution": "string",
        "key_strength": "string",
        "current_formulation": "string",
        "potential_improvements": ["string"]
      },
      "development_assessment": {
        "llm_alignment": "string",
        "reasoning_pathway": "string",
        "example_needs": "string",
        "technical_requirements": "string",
        "anticipated_challenges": ["string"]
      },
      "literature_assessment": {
        "key_debates": ["string"],
        "engagement_strategy": "string",
        "background_requirements": ["string"]
      },
      "refinement_opportunities": {
        "core_preserving_changes": ["string"],
        "development_suggestions": ["string"],
        "scope_adjustments": ["string"]
      },
      "viability_summary": {
        "strengths": ["string"],
        "concerns": ["string"],
        "overall_assessment": "string"
      }
    }
  ],
  "selection_decision": {
    "selected_topics": [
      {
        "title": "string",
        "rank": "integer",
        "selection_rationale": "string",
        "comparative_advantages": ["string"]
      }
    ],
    "rejected_topics": [
      {
        "title": "string",
        "rejection_rationale": ["string"]
      }
    ],
    "comparative_analysis": {
      "key_differentiators": ["string"],
      "ranking_rationale": "string"
    }
  },
  "stage_guidance": {
    "development_priorities": ["string"],
    "next_stage_considerations": "string"
  }
}

IMPORTANT:
- Every string field must be a complete sentence
- Array items should be distinct and substantive
- Maintain consistent detail level across topics
- Ensure all rationales are clear and specific"""

    def get_prompt(self, topics_json: str) -> str:
        """Construct the full evaluation prompt"""
        return f"""You are an expert in analytic philosophy tasked with evaluating potential paper topics for Analysis journal. Your goal is to identify the {self.cull_min} to {self.cull_max} most promising topics that are well-suited for AI development while maintaining appropriate scholarly ambition.

{self.evaluation_principles}

{self.evaluation_process}

{self.selection_guidance}

{self.output_requirements}

Here are the topics for evaluation:
{topics_json}

Proceed by first evaluating each topic thoroughly, then making comparative judgments and selections."""
