# src/stages/phase_two/stages/stage_two/prompts/key_moves_prompts.py

from typing import Dict, Optional
import json


class KeyMovesDevelopmentPrompts:
    """Prompts for analyzing individual key moves"""

    def __init__(self):
        self.system_prompt = """You are an expert philosophy researcher developing key argumentative moves for a paper. Your role is to create concrete, detailed arguments that advance the thesis. You must produce specific content (not meta-commentary) that will guide paper development in an automated pipeline."""

    def construct_argument_prompt(
        self, move: str, abstract: str, outline: str, prior_moves: Optional[Dict] = None
    ) -> str:
        context = f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.2 (Framework Development).
You are developing a key argumentative move that was identified in the abstract.
Your output will guide the detailed development of this argument in later phases.

You are developing the argument for a key move in our Analysis paper (4,000 word limit).
Your task is to develop this move in a way that:
1. Advances the paper's main thesis
2. Fits coherently with the overall framework
3. Can be executed within the established structure
4. Is CONCRETE and developed. E.g., an actual argument with details or a real example could be good. "The argument should have compelling premises" is not. The latter is just meta-commentary rather than an actual contribution to the paper.
</context>

<framework>
Paper Vision (Abstract):
{abstract}

Paper Structure:
{outline}

Key Move to Develop:
{move}"""

        if prior_moves:
            context += f"""

Previously Developed Moves:
{json.dumps(prior_moves, indent=2)}"""

        context += """
</framework>"""

        return f"""{context}

<task>
Develop this key move with concrete arguments and specific examples.
Create actual philosophical content, not descriptions of what content should be.
Ensure the argument advances the thesis and fits the framework.
</task>

<thinking>
Take time to think through how this argument could work before presenting your final version.
You can use the scratch space to explore different approaches and work through potential issues.
</thinking>

<output_format>
# Scratch Work
[Think through different approaches to developing this argument]
[Consider various examples and how they might work]
[Explore how different argumentative strategies would fit with the paper]
[Work through any complex steps or connections]
[EVEN IF YOU'RE A REASONING MODEL, BE SURE TO INCLUDE THIS SECTION FOR VALIDATION]

# Final Argument Development
## Argument Sketch
[Detail how the argument would actually develop. Again, be concrete.]

## Initial Examples
[Specific examples/illustrations that would support this move. Real examples, not just descriptions of what sorts of general features would make the example good.]

## Key Steps
[Critical steps in executing this argument. Again, concrete steps, not generic features.]

## Integration Notes
[How this argument fits with the paper's broader framework. BE SURE TO INCLUDE THIS SECTION FOR VALIDATION.]
</output_format>"""

    def construct_challenges_prompt(
        self, move: str, argument_sketch: str, abstract: str, outline: str
    ) -> str:
        return f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.2 (Framework Development).
You are analyzing potential challenges and feasibility for a key move that has been developed.
Your analysis will determine whether this move needs modification before paper development.
</context>

<task>
Analyze potential challenges and feasibility for this key move.
Identify concrete issues that could prevent successful development.
Suggest specific mitigations for identified challenges.
</task>

<framework>
Paper Vision (Abstract):
{abstract}

Paper Structure:
{outline}

Key Move:
{move}

Proposed Argument:
{argument_sketch}
</framework>

<thinking>
Think carefully through potential issues before presenting your final analysis.
Use the scratch space to explore concerns and think through their implications.
</thinking>

<output_format>
# Scratch Work
[Think through potential failure modes]
[Consider interactions with other parts of the paper]
[Explore severity of different challenges]
[Work through possible mitigations]

# Final Analysis
## Potential Challenges
- [Challenge 1]
  - Severity: high/medium/low
  - Description: [Detailed, concrete explanation]
  - Possible mitigation: [How we might address this with concrete steps forward]

## Critical Dependencies
- [List of what must be true/established for this argument to work]
- [Key assumptions that need to be valid]

## Feasibility Assessment
- Overall assessment: feasible/needs modification/problematic
- Confidence level: high/medium/low
- Key considerations: [Critical factors in this assessment]

## Risk Mitigation
[Specific suggestions for addressing identified risks while maintaining the move's essential contribution]
</output_format>"""

    def get_system_prompt(self) -> str:
        """Return the system prompt for API calls"""
        return self.system_prompt
