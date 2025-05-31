# src/stages/phase_two/stages/stage_two/prompts/outline_prompts.py
import json


class OutlineDevelopmentPrompts:
    """Prompts for outline development"""

    def __init__(self):
        self.system_prompt = """You are an expert philosophy researcher developing a paper outline for the journal Analysis. Your role is to create a clear structural blueprint that will guide paper development. You must work within the abstract and framework already established and produce output for an automated pipeline."""

        self.context = """You are developing an outline for a paper to be published in Analysis (4,000 word limit).
Analysis favors clear, precise papers in the analytic tradition that make a single sharp philosophical contribution.

Your task is to create an outline that faithfully develops the validated abstract and framework. The outline must:
- Create clear spaces for developing each key move specified in the abstract
- Maintain the sharp focus and contribution identified in the abstract
- Support the main thesis through a natural progression of arguments
- Enable all elements of the abstract to be developed effectively"""

        self.structure_requirements = """The outline should include:
- Main sections (typically 4-7)
- Key subsections where needed
- Brief description of each section's purpose
- Notes on key arguments/moves in each section

You can use scratch work to think through:
- How sections build on each other
- Where key moves fit best
- Potential development challenges
- Alternative structures considered"""

        self.output_format = """# Scratch Work
[Your thinking about structure and organization]

# Final Outline
[Structured outline in markdown. MAKE SURE TO INCLUDE AN INTRODUCTION AND CONCLUSION.]

# Development Notes
- Important considerations for development
- Critical connections between sections
- Potential challenges to address"""

    def construct_prompt(
        self, abstract: str, main_thesis: str, core_contribution: str, key_moves: list
    ) -> str:
        """Generate prompt for outline development"""
        return f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.2 (Framework Development).
You have the validated abstract and framework from earlier in this phase.
Your outline will guide the detailed development in subsequent phases.
{self.context}
</context>

<task>
Create a structured outline that develops the abstract and framework into a complete paper structure.
Ensure each key move has a clear place in the outline.
Maintain focus on the main thesis throughout.
</task>

<framework_components>
Abstract:
{abstract}

Main Thesis:
{main_thesis}

Core Contribution:
{core_contribution}

Key Moves:
{json.dumps(key_moves, indent=2)}
</framework_components>

<requirements>
{self.structure_requirements}
</requirements>

<output_format>
Provide your response in the following format:
{self.output_format}
</output_format>

<reminder>
Remember: The outline must create a clear path from introduction through key moves to conclusion, all supporting the main thesis.
</reminder>"""

    def get_system_prompt(self) -> str:
        """Return the system prompt for API calls"""
        return self.system_prompt
