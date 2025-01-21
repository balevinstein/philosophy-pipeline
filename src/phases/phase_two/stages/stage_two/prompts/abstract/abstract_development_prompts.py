# src/stages/phase_two/stages/stage-two/prompts/abstract_prompts.py

import json


class AbstractDevelopmentPrompts:
    """Prompts for abstract development"""

    def __init__(self):
        self.analysis_context = """You are helping write a paper for Analysis, a philosophical journal with a strict 4,000 word limit. Papers in Analysis make a single, clear philosophical contribution that can be effectively developed in this space. The abstract should clearly state the main thesis and philosophical contribution while being engaging and precise."""

        self.output_requirements = """
OUTPUT REQUIREMENTS:
1. Response must be valid JSON
2. Use simple ASCII characters only (no special quotes or unicode)
3. Keep all text fields clear and well-formed
4. Abstract should be 150-220 words (aim for this range)
5. Main thesis must be a single clear sentence
6. Key moves should be concrete and specific
7. Development notes should explain your choices"""

        self.output_format = """
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

    def construct_prompt(self, lit_synthesis: dict, final_selection: dict) -> str:
        """Generate prompt for initial abstract development"""
        return f"""
{self.analysis_context}

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

{self.output_requirements}

Literature Analysis:
```json
{json.dumps(lit_synthesis, indent=2)}
```

Selected Topic and Development:
```json
{json.dumps(final_selection, indent=2)}
```

Provide your output in the following JSON format:
{self.output_format}

The full paper readings and narrative synthesis are available if you need to check specific details. Provide a long abstract, at least 200 words"""
