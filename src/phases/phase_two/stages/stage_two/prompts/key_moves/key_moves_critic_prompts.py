from typing import Dict, Any
import json


class KeyMovesCriticPrompts:
    """Prompts for analyzing feasibility and integration of key moves"""

    def __init__(self):
        self.context = """You are evaluating key argumentative moves for an Analysis paper (4,000 word limit). Each move must be:
1. Concretely developable within the space constraints
2. Well-integrated with the paper's framework
3. Supported by available literature
4. Aligned with the paper's main thesis
5. Is detailed and concrete enough to be useful for further development rather than just having a lot of meta-commentary.

Your goal is to identify both strengths and potential issues while maintaining focus on what matters most for successful development. Different moves may require different types of support - some may rely heavily on examples, others on formal argumentation, others on careful conceptual development.
"""

        self.evaluation_focus = """
Key areas requiring careful evaluation:

Argument Structure:
- If formal arguments are present, evaluate their logical structure
- If the argument is more informal, assess the reasoning chain
- Identify any unstated assumptions or missing steps
- Consider whether additional argumentative moves are needed
- Are actual claims being made, or is it just meta-commentary on the kind of argument that would be good to think about in the future?

Examples and Cases (if present):
- Are examples well-chosen and effectively used?
- Do they actually demonstrate what's claimed?
- Are they developed in sufficient detail?
- Would different or additional examples strengthen the move?
- Is there a real example here, or just a gesture at some high-level features an example should have?

Development Path:
- Is the progression from sketch to implementation clear?
- Are all necessary steps identified?
- Are dependencies and prerequisites handled?
- Is the scope realistic within space constraints?

Conceptual Clarity:
- Are terms used clearly and consistently?
- Are important distinctions maintained?
- Is the theoretical development clear?
- Are any key concepts underdeveloped?

Integration and Completeness:
- How well does this move fit with others?
- Are there important gaps in the overall argument?
- Would additional moves strengthen the framework?
- Is the balance between moves appropriate?

Your critique should:
1. Evaluate what's actually present in each move
2. Identify what might be missing
3. Suggest improvements or additions where needed
4. Consider how moves work together to advance the paper's thesis"""

        self.literature_guidance = """
Literature Support:
- What specific resources from our literature base support this move?
- Are there potential tensions with existing work?
- Are we making appropriate use of available theoretical tools?
- Would different literature engagement strengthen the move?

Remember you only have access to the specific papers provided in the literature files - evaluate support and engagement possibilities within these constraints."""

        self.output_guidance = """Consider carefully:
- How effectively does this move advance the paper's thesis?
- What specific development challenges might arise?
- How well does it integrate with other moves and the overall framework?
- What literature support can we draw on?
- Are there hidden dependencies or assumptions?
- Are additional moves or support needed?

Frame your critique to help improve the move while preserving what works.

Remember that different moves may require different types of development and support. Your critique should be responsive to the specific needs of each move while ensuring the overall argument structure is sound and complete."""

        self.output_format = """
        You MUST include the Scratch Work and Summary Assessment sections listed below in the output format. The major output sections are marked by heading notation "#".

# Scratch Work // Required Section
[Think through the moves' interactions, dependencies, and overall coherence]

# Move Analysis
[For each key move, provide:]

## [Move Name]
- Argument assessment
- Development feasibility
- Literature support
- Integration with framework
- Specific recommendations

# Cross-Cutting Considerations
[Address any issues that span multiple moves]
- Dependencies between moves
- Overall argument structure
- Literature coverage
- Framework support

# Summary Assessment // Required Section
MAJOR REVISION [if significant rework needed]
MINOR REFINEMENT [if targeted improvements needed]
MINIMAL CHANGES [if moves are fundamentally sound]
"""

    def construct_prompt(
        self,
        current_moves: Dict[str, Any],
        framework: Dict[str, Any],
        outline: str,
        lit_readings: Dict[str, Any],
        lit_synthesis: Dict[str, Any],
        lit_narrative: str,
    ) -> str:
        """Generate prompt for key moves critique"""

        return f"""
{self.context}

Current Framework Development:
{json.dumps(framework, indent=2)}

Current Outline:
{outline}

Key Moves Analysis:
{json.dumps(current_moves, indent=2)}

Literature Context:
1. Paper Readings:
{json.dumps(lit_readings, indent=2)}

2. Literature Synthesis:
{json.dumps(lit_synthesis, indent=2)}

3. Synthesis Narrative:
{lit_narrative}

{self.evaluation_focus}

{self.literature_guidance}

{self.output_guidance}

OUTPUT FORMAT

Your output should exactly follow the format described below. DO NOT include any reasoning or description besides the output:

{self.output_format}
"""
