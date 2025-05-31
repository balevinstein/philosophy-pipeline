# src/stages/phase_two/stages/stage_two/prompts/abstract_refinement_prompts.py

from typing import Dict, Optional, List
import json


class AbstractRefinementPrompts:
    """Prompts for refining abstract and framework based on critique"""

    def __init__(self):
        self.system_prompt = """You are an expert philosophy editor refining a paper framework for the journal Analysis. Your role is to implement improvements based on critique while maintaining what already works well. You must produce clear, focused output that will guide downstream paper development in an automated pipeline."""

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

        self.json_rules = """
CRITICAL JSON FORMATTING RULES:
1. Output ONLY valid JSON - no markdown code blocks, no explanations outside JSON
2. Use double quotes for all strings
3. Escape quotes within text using \"
4. Replace newlines with spaces in text fields
5. Ensure all brackets and braces are properly closed
6. Arrays must use square brackets []
7. The response must be parseable by json.loads()"""

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

        context = f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.2 (Framework Development).
You have the current framework and critique from the previous iteration.
Your refined output will guide all subsequent paper development phases.
{self.context}
</context>

<task>
Refine the abstract and framework based on the critique provided.
Implement improvements while maintaining what already works well.
Ensure all components remain aligned and feasible.
</task>

<literature_context>
Literature Context:
{json.dumps(lit_synthesis, indent=2)}
</literature_context>

<current_framework>
Current Framework Development:
{json.dumps(current_framework, indent=2)}
</current_framework>

<recent_critique>
Recent Critique:
{critique.get('content', '')}
</recent_critique>

<requirements>
{self.output_requirements}

Think carefully about how changes to any component affect the whole framework.
Not every suggestion must be implemented, but provide clear reasoning for your decisions.
Provide a long abstract, at least 200 words
</requirements>

{self.json_rules}

<output_format>
Provide your refinement in the following format:
{self.output_format}
</output_format>"""

        if previous_versions:
            context += f"""

<iteration_note>
Note: This is refinement cycle {len(previous_versions)}.
Consider the evolution of the framework through previous versions while making further improvements.
</iteration_note>"""

        return context

    def get_system_prompt(self) -> str:
        """Return the system prompt for API calls"""
        return self.system_prompt
