# src/stages/phase_two/stages/stage_two/prompts/outline_prompts.py
import json

class OutlinePrompts:
    """Prompts for outline development"""
    
    def __init__(self):
        self.CONTEXT = """You are developing an outline for a paper to be published in Analysis (4,000 word limit). 
Analysis favors clear, precise papers in the analytic tradition that make a single sharp philosophical contribution.

Your task is to create an outline that faithfully develops the validated abstract and framework. The outline must:
- Create clear spaces for developing each key move specified in the abstract
- Maintain the sharp focus and contribution identified in the abstract
- Support the main thesis through a natural progression of arguments
- Enable all elements of the abstract to be developed effectively"""

        self.STRUCTURE_REQUIREMENTS = """The outline should include:
- Main sections (typically 4-7)
- Key subsections where needed
- Brief description of each section's purpose
- Notes on key arguments/moves in each section

You can use scratch work to think through:
- How sections build on each other
- Where key moves fit best
- Potential development challenges
- Alternative structures considered"""

        self.OUTPUT_FORMAT = """# Scratch Work
[Your thinking about structure and organization]

# Final Outline
[Structured outline in markdown. MAKE SURE TO INCLUDE AN INTRODUCTION AND CONCLUSION.]

# Development Notes
- Important considerations for development
- Critical connections between sections
- Potential challenges to address"""

    def get_development_prompt(self, 
                             abstract: str,
                             main_thesis: str,
                             core_contribution: str,
                             key_moves: list) -> str:
        """Generate prompt for outline development"""
        return f"""
{self.CONTEXT}

Abstract:
{abstract}

Main Thesis:
{main_thesis}

Core Contribution:
{core_contribution}

Key Moves:
{json.dumps(key_moves, indent=2)}

{self.STRUCTURE_REQUIREMENTS}

Provide your response in the following format:
{self.OUTPUT_FORMAT}
"""