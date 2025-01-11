# src/stages/phase_two/stages/stage-two/prompts/abstract_prompts.py

import json

class AbstractPrompts:
    """Prompts for abstract development"""
    
    def __init__(self):
        self.ANALYSIS_CONTEXT = """You are helping write a paper for Analysis, a philosophical journal with a strict 4,000 word limit. Papers in Analysis make a single, clear philosophical contribution that can be effectively developed in this space. The abstract should clearly state the main thesis and philosophical contribution while being engaging and precise."""

        self.OUTPUT_REQUIREMENTS = """
OUTPUT REQUIREMENTS:
1. Response must be valid JSON
2. Use simple ASCII characters only (no special quotes or unicode)
3. Keep all text fields clear and well-formed
4. Abstract should be 150-220 words (aim for this range)
5. Main thesis must be a single clear sentence
6. Key moves should be concrete and specific
7. Development notes should explain your choices"""

        self.OUTPUT_FORMAT = """
{
    "abstract": "Complete abstract for the paper",
    "main_thesis": "Clear and precise statement of the paper's main thesis",
    "core_contribution": "Specific explanation of the philosophical contribution",
    "key_moves": [
        "Concrete description of each key argumentative move",
        "Each move should be something we can actually develop"
    ],
    "development_notes": "Explanation of choices and approach",
    "validation_status": {
        "scope_appropriate": boolean,
        "clearly_articulated": boolean,
        "sufficiently_original": boolean,
        "feasibly_developable": boolean
    }
}"""

    def get_development_prompt(self, 
                             lit_readings: dict,
                             lit_synthesis: dict, 
                             lit_narrative: str,
                             final_selection: dict) -> str:
        """Generate prompt for initial abstract development"""
        return f"""
{self.ANALYSIS_CONTEXT}

Your task is to develop an abstract and framework for the paper that builds on our literature analysis and selected topic.

You have access to:
1. Detailed readings of each paper
2. A structured synthesis of the literature
3. A narrative analysis of how the papers fit together
4. Our final topic selection and initial development plans

Focus on creating an abstract that:
- Makes a clear and novel contribution
- Can be developed effectively in 4,000 words
- Engages meaningfully with our literature
- Has concrete, developable key moves

{self.OUTPUT_REQUIREMENTS}

Literature Analysis:
{json.dumps(lit_synthesis, indent=2)}

Selected Topic and Development:
{json.dumps(final_selection, indent=2)}

Provide your output in the following format:
{self.OUTPUT_FORMAT}

The full paper readings and narrative synthesis are available if you need to check specific details."""