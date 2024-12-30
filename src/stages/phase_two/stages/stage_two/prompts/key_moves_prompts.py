# src/stages/phase_two/stages/stage_two/prompts/key_moves_prompts.py

from typing import Dict, Optional
import json

class KeyMovesPrompts:
    """Prompts for analyzing individual key moves"""
    
    def get_argument_prompt(self, 
                          move: str, 
                          abstract: str,
                          outline: str,
                          prior_moves: Optional[Dict] = None) -> str:
        context = f"""
You are developing the argument for a key move in our Analysis paper (4,000 word limit).
Your task is to develop this move in a way that:
1. Advances the paper's main thesis
2. Fits coherently with the overall framework
3. Can be executed within the established structure
4. Is CONCRETE and developed. E.g., an actual argument with details or a real example could be good. "The argument should have compeling premises" is not. The latter is just meta-commentary rather than an actual contribution to the paper.

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

        return f"""{context}

Take time to think through how this argument could work before presenting your final version.
You can use the scratch space to explore different approaches and work through potential issues.

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
[Critical steps in executing this argument. Again, concerete steps, not generic features.]

## Integration Notes
[How this argument fits with the paper's broader framework. BE SURE TO INCLUDE THIS SECTION FOR VALIDATION.]"""

    def get_challenges_prompt(self, 
                            move: str,
                            argument_sketch: str,
                            abstract: str,
                            outline: str) -> str:
        return f"""
You are analyzing potential challenges and feasibility for a key move in our Analysis paper.

Paper Vision (Abstract):
{abstract}

Paper Structure:
{outline}

Key Move:
{move}

Proposed Argument:
{argument_sketch}

Think carefully through potential issues before presenting your final analysis.
Use the scratch space to explore concerns and think through their implications.

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
  - Possible mitigation: [How we might address this with conrete steps forward]

## Critical Dependencies
- [List of what must be true/established for this argument to work]
- [Key assumptions that need to be valid]

## Feasibility Assessment
- Overall assessment: feasible/needs modification/problematic
- Confidence level: high/medium/low
- Key considerations: [Critical factors in this assessment]

## Risk Mitigation
[Specific suggestions for addressing identified risks while maintaining the move's essential contribution]"""