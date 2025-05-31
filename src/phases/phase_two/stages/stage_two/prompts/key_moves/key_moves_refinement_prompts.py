from typing import Dict, Any
import json


class KeyMovesRefinementPrompts:
    """Prompts for refining key moves based on critique"""

    def __init__(self):
        self.system_prompt = """You are an expert philosophy editor refining key argumentative moves for a paper. Your role is to implement improvements based on critique while maintaining what already works. You must produce concrete, refined arguments that will guide paper development in an automated pipeline."""

        self.context = """You are refining key argumentative moves for an Analysis paper (4,000 word limit). Each move must:
1. Advance the paper's main thesis
2. Be concretely developable within space constraints
3. Integrate well with other moves
4. Draw appropriately on available literature

Consider each suggested change carefully, but maintain what works. You should:
- Evaluate each suggestion's merit
- Consider how changes affect move interactions
- Maintain framework alignment
- Preserve effective elements
- Ensure literature support

Remember you can only use the specific papers provided in the literature files - ensure all refinements are supported by these available sources."""

        self.output_format = """# Scratch Work
[Think through the changes being suggested]
[Consider interactions and dependencies]
[Evaluate theoretical implications]

# Refinement Decisions
[Overall refinement strategy]

## Will Implement
1. [Change] -- [Rationale]
2. [Change] -- [Rationale]
...

## Won't Implement
1. [Change] -- [Rationale]
2. [Change] -- [Rationale]
...

# Updated Move Development
[Complete refined version of each move]

# Change Notes
- Impact on theoretical foundations
- Effect on move interactions
- Literature integration adjustments
- Framework alignment status
- Development feasibility within word constraints
- Dependencies between refined moves"""

    def construct_prompt(
        self,
        current_moves: Dict[str, Any],
        critique: Dict[str, Any],
        framework: Dict[str, Any],
        outline: str,
        lit_synthesis: Dict[str, Any],
    ) -> str:
        """Generate prompt for key moves refinement"""

        return f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.2 (Framework Development).
You have the current key moves and critique from the previous iteration.
Your refined moves will guide all subsequent paper development.
{self.context}
</context>

<task>
Refine the key argumentative moves based on the critique provided.
Implement improvements while maintaining what works well.
Ensure all moves work together to support the thesis.
</task>

<current_framework>
Current Framework:
{json.dumps(framework, indent=2)}

Current Outline:
{outline}
</current_framework>

<current_moves>
Current Moves:
{json.dumps(current_moves, indent=2)}
</current_moves>

<recent_critique>
Recent Critique:
{json.dumps(critique, indent=2)}
</recent_critique>

<literature_context>
Literature Context:
{json.dumps(lit_synthesis, indent=2)}
</literature_context>

<requirements>
Analyze the critique and provide refinements using this structure:
You MUST include all the sections listed below in the output format. The major output sections are marked by heading notation "#"

{self.output_format}

Think carefully about how each change affects the moves' ability to support the paper's thesis and their integration with the overall framework.
</requirements>"""

    def get_system_prompt(self) -> str:
        """Return the system prompt for API calls"""
        return self.system_prompt
