# src/stages/phase_two/stages/stage_two/prompts/abstract_refinement_prompts.py

from typing import Dict, Optional, List
import json


class AbstractRefinementPrompts:
    """Prompts for refining abstract and framework based on critique"""

    def __init__(self):
        self.context = """You are refining an abstract and framework for a paper to be published in Analysis (4,000 word limit).
Analysis favors clear, precise papers in the analytic tradition that make a single sharp philosophical contribution.

You have received critique of the current framework. Consider each suggestion carefully, but maintain and preserve
what is already working well. You should:
- Evaluate each suggestion's merit
- Consider how changes interact across components
- Maintain coherence between abstract and framework
- Preserve effective elements
- Ensure all components remain feasible

The paper will be written by AI models that:
- Have access to the specific papers provided in our literature analysis
- Cannot freely access additional academic literature
- Must develop arguments without extensive citation requirements"""

        self.output_requirements = """
OUTPUT REQUIREMENTS:
1. Response must be valid JSON
2. Use simple ASCII characters only
3. Keep all text fields clear and well-formed
4. Abstract should aim for 160-220 words AND NEVER BE UNDER 140 OR OVER 270 WORDS!
5. Main thesis must be a single clear sentence
6. Key moves must be concrete and developable
7. All components must maintain alignment
8. Development notes should explain choices"""

        self.output_format = """# Scratch Work
[Think through suggested changes and their impacts across components]
[Consider interactions between abstract and framework elements]
[Evaluate feasibility of proposed changes]
[Plan coherent integration]

# Refinement Decisions
[Explain which suggestions you'll implement and why]
[Note which suggestions you won't implement and why]
[Address impacts across components]

# Updated Framework Development
{
   "abstract": "The refined abstract text",
   "main_thesis": "Clear and precise thesis statement that aligns with abstract",
   "core_contribution": "Specific explanation of philosophical contribution",
   "key_moves": [
       "List of concrete, developable argumentative moves that support abstract claims",
       "Each move must be feasible and align with framework"
   ],
   "development_notes": "Explanation of refinement choices and approach",
   "validation_status": {
       "scope_appropriate": boolean,
       "clearly_articulated": boolean,
       "sufficiently_original": boolean,
       "feasibly_developable": boolean
   },
   "changes_made": [
       "List significant changes and rationale",
       "Include changes to all components",
       "Explain maintenance of coherence"
   ]
}"""

    def construct_prompt(
        self,
        current_framework: Dict,
        critique: Dict,
        lit_synthesis: Dict,
        previous_versions: Optional[List[Dict]] = None,
    ) -> str:
        """Generate prompt for comprehensive framework refinement"""

        context = f"""
{self.context}

Literature Context:
{json.dumps(lit_synthesis, indent=2)}

Current Framework Development:
{json.dumps(current_framework, indent=2)}

Recent Critique:
{critique.get('content', '')}

{self.output_requirements}

Think carefully about how changes to any component affect the whole framework.
Not every suggestion must be implemented, but provide clear reasoning for your decisions.

Provide your refinement in the following format:
{self.output_format}"""

        if previous_versions:
            context += f"""

Note: This is refinement cycle {len(previous_versions)}.
Consider the evolution of the framework through previous versions while making further improvements."""

        return context
