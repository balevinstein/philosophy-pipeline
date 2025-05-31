import json
from typing import Dict


class OutlineRefinementPrompts:
    """Prompts for refining outline based on critique"""

    def __init__(self):
        self.system_prompt = """You are an expert philosophy editor refining a paper outline for the journal Analysis. Your role is to implement structural improvements based on critique while maintaining what already works well. You must produce a clear outline that will guide downstream development in an automated pipeline."""

        self.context = """You are refining a high-level outline for a paper to be published in Analysis (4,000 word limit).
This outline establishes the main sections and key structural elements that will scaffold later development.

You have received critique of the current outline. Your primary focus should be ensuring the outline effectively supports:
- The paper's main thesis and core contribution
- All key argumentative moves
- Clear theoretical development
- Proper literature engagement

Consider each suggestion carefully, but maintain what is already working well. You should:
- Evaluate each suggested change's merit
- Consider how changes affect overall structure
- Maintain clear section progression
- Preserve effective elements
- Ensure framework support

Take time to think through how changes will affect the outline's ability to support argument development and key moves."""

        self.output_format = """# Scratch Work
[Think through critique suggestions and their implications]
[Consider structural impacts]
[Evaluate section dependencies]
[Plan coherent revisions]

# Framework Support Analysis
[How outline changes support or affect:
- Main thesis development
- Core contribution
- Key argumentative moves
- Literature engagement]

# Refinement Decisions
## Will Implement
[List changes to be made with rationale for each]

## Won't Implement
[List suggestions not taken with brief explanation why]

# Updated Outline
[The refined outline in markdown format. MAKE SURE TO INCLUDE AND INTRODUCTION AND CONCLUSION SECTION.]

# Change Notes
- How the changes improve framework support
- Impact on structural coherence
- Effect on development feasibility
- Support for key moves"""

    def construct_prompt(
        self,
        outline: str,
        critique: Dict,
        framework: Dict,
        lit_synthesis: Dict,
    ) -> str:
        """Generate prompt for outline refinement"""
        return f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.2 (Framework Development).
You have the current outline and critique from the previous iteration.
Your refined outline will guide all subsequent paper development.
{self.context}
</context>

<task>
Refine the outline based on the critique provided.
Implement structural improvements while maintaining what works well.
Ensure the outline effectively supports the framework.
</task>

<current_framework>
Current Framework:
{json.dumps(framework, indent=2)}
</current_framework>

<current_outline>
Current Outline:
{outline}
</current_outline>

<recent_critique>
Critique:
{critique.get('content', '')}
</recent_critique>

<literature_context>
Literature Context:
{json.dumps(lit_synthesis, indent=2)}
</literature_context>

<requirements>
Provide your refinement following this format:
{self.output_format}

Think carefully about how each change affects the outline's ability to support the framework's development.
</requirements>"""

    def get_system_prompt(self) -> str:
        """Return the system prompt for API calls"""
        return self.system_prompt
