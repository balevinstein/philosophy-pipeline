import json
from typing import Dict


class OutlineRefinementPrompts:
    """Prompts for refining outline based on critique"""

    def __init__(self):
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
        return f"""
{self.context}

Current Framework:
{json.dumps(framework, indent=2)}

Current Outline:
{outline}

Critique:
{critique.get('content', '')}

Literature Context:
{json.dumps(lit_synthesis, indent=2)}

Provide your refinement following this format:
{self.output_format}

Think carefully about how each change affects the outline's ability to support the framework's development."""
