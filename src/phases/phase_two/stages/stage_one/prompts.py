# src/stages/phase_two/stages/stage_one/prompts.py

from typing import Dict, Any, List, Tuple
import json

class InitialReadPrompts:
    """Prompts for initial paper reading"""
    
    def __init__(self):
        self.OUTPUT_REQUIREMENTS = """
OUTPUT REQUIREMENTS:
1. Response must be valid JSON
2. Use simple ASCII characters only (no special quotes or unicode)
3. Keep all text fields as single-line strings (no line breaks)
4. Be explicit and specific in all assessments
5. Every string field must be a complete, well-formed sentence
6. Array items should be distinct and substantive
7. Maintain consistent detail level throughout
8. Include confidence levels where specified
9. Flag any uncertainties explicitly"""

        self.OUTPUT_FORMAT = """
{
    "paper_info": {
        "title": "exact paper title",
        "authors": ["list of authors"],
        "publication_info": {
            "year": "year of publication",
            "venue": "journal or conference name",
            "doi": "doi if available",
            "length": "number of pages"
        },
        "structure": {
            "sections": ["list of main section titles"],
            "organization": "description of paper's organizational strategy",
            "methodology": "description of paper's philosophical approach"
        }
    },
    "core_content": {
        "main_thesis": "central claim or argument of the paper",
        "background_context": "scholarly context and motivation",
        "key_arguments": [
            {
                "claim": "clear statement of argument",
                "support": ["key supporting points"],
                "development": "how the argument is developed",
                "significance": "why this argument matters",
                "confidence": "high|medium|low"
            }
        ],
        "important_definitions": [
            {
                "term": "term being defined",
                "definition": "clear statement of definition",
                "context": "how the definition is used",
                "confidence": "high|medium|low"
            }
        ],
        "examples": [
            {
                "description": "brief description of example",
                "purpose": "how example is used in paper",
                "effectiveness": "assessment of example's effectiveness"
            }
        ]
    },
    "scholarly_context": {
        "key_citations": [
            {
                "author": "author name",
                "year": "publication year",
                "work": "work being cited",
                "purpose": "how citation is used",
                "confidence": "high|medium|low"
            }
        ],
        "research_streams": ["major research areas this engages with"],
        "debates": ["key scholarly debates paper addresses"],
        "methodology_notes": "description of paper's philosophical approach and methods"
    },
    "potential_uses": {
        "key_quotes": [
            {
                "quote": "exact quote",
                "context": "surrounding context",
                "potential_uses": ["ways this might be useful"],
                "location": "page or section reference",
                "confidence": "high|medium|low"
            }
        ],
        "notable_points": [
            {
                "point": "important point that might be useful",
                "context": "how it arises in the paper",
                "potential_applications": ["ways this might be used"],
                "confidence": "high|medium|low"
            }
        ]
    },
    "analysis_notes": {
        "clarity_assessment": "assessment of paper's clarity and accessibility",
        "notable_features": ["distinctive features of the paper's approach"],
        "limitations": ["any notable limitations or gaps"],
        "confidence_summary": {
            "understanding": "high|medium|low",
            "quotes": "high|medium|low",
            "context": "high|medium|low"
        }
    }
}"""

    def get_prompt(self, paper_path: str) -> str:
        """Generate prompt for initial paper reading"""
        return f"""You are reading an academic philosophy paper to understand its content and identify potentially useful elements. This is an initial read focused on understanding the paper's contributions and context.

Read the paper carefully and extract key information, focusing on:
1. Clear understanding of main arguments and their development
2. Important definitions, distinctions, and examples
3. Scholarly context, debates, and methodology
4. Potentially useful quotes and points
5. Paper structure and organization
6. Areas that might be valuable for future work

{self.OUTPUT_REQUIREMENTS}

Be thorough but focus on accuracy over quantity. If you're uncertain about anything, note this explicitly in your confidence assessments. For quotes, only include those you're highly confident are exact.

Provide your analysis in the following format:
{self.OUTPUT_FORMAT}"""
    


class ProjectSpecificPrompts:
    """Prompts for project-specific paper analysis"""
    
    def __init__(self):
        self.OUTPUT_REQUIREMENTS = """
OUTPUT REQUIREMENTS:
1. Response must be valid JSON
2. Use simple ASCII characters only (no special quotes or unicode)
3. Keep all text fields as single-line strings (no line breaks)
4. Be explicit and specific in all assessments
5. Array fields can be empty or contain a single 'none' entry if nothing relevant is found
6. Include confidence levels where specified"""

        self.OUTPUT_FORMAT = """{
    "paper_info": {
        "title": "exact paper title",
        "authors": ["list of authors"]
    },
    "engagement_assessment": {
        "type": "primary|supporting|background",
        "overall_relevance": "high|medium|low",
        "rationale": "explanation of assessed relevance level"
    },
    "key_connections": [
        {
            "type": "conceptual|methodological|framework",
            "description": "specific point of connection to our project",
            "strength": "how strong/direct the connection is",
            "development_needs": ["what we'd need to do to develop this"]
        }
    ],
    "critical_engagement": {
        "agreements": [
            {
                "point": "point of agreement",
                "usefulness": "how this helps our project",
                "development_needs": ["what we need to do to use this"]
            }
        ],
        "disagreements": [
            {
                "claim": "claim we might challenge",
                "our_position": "our view on this",
                "engagement_value": "how this advances our project"
            }
        ]
    }
}"""

    def get_prompt(self, initial_reading: Dict, final_selection: Dict) -> str:
        """Generate prompt for project-specific reading"""
        # Extract key information from final_selection
        chosen_topic = final_selection['selection']['selection_analysis']['selection']['chosen_topic']
        core_thesis = final_selection['phase_two_setup']['phase_two_setup']['thesis_development']['core_thesis']
        key_moves = final_selection['phase_two_setup']['phase_two_setup']['thesis_development']['key_moves']
        
        return f"""You are conducting a focused re-reading of a philosophy paper specifically for our project.

    Our project focus:
    Topic: {chosen_topic}
    Thesis: {core_thesis}
    Key Moves:
    {json.dumps(key_moves, indent=2)}

    Previous Reading:
    {json.dumps(initial_reading, indent=2)}

    Your task is to analyze how this paper specifically relates to our project. Consider:
    1. How directly relevant is this paper?
    2. What specific elements could we use?
    3. Where might we agree or disagree?
    4. How might this inform our development?

    {self.OUTPUT_REQUIREMENTS}

    Provide your analysis in the following format:
    {self.OUTPUT_FORMAT}"""    

class SynthesisPrompts:
    """Prompts for synthesizing literature analysis"""
    
    def __init__(self):
        self.JSON_REQUIREMENTS = """
JSON OUTPUT REQUIREMENTS:
1. Use simple ASCII characters only (no special quotes or unicode)
2. Keep all text fields as single-line strings (no line breaks)
3. Include confidence levels where specified
4. Flag any uncertainties explicitly"""

        self.MARKDOWN_REQUIREMENTS = """
MARKDOWN OUTPUT REQUIREMENTS:
1. Use clear section headers (##)
2. Include line breaks between sections
3. Use bullet points for lists
4. Use standard Markdown formatting (*italic*, **bold**)
5. Keep paragraphs focused and concise"""

        self.JSON_FORMAT = """
{
    "literature_overview": {
        "primary_papers": [
            {
                "title": "paper title",
                "engagement_level": "primary",
                "key_role": "how this paper will be central",
                "development_priority": "high|medium|low"
            }
        ],
        "supporting_papers": [
            {
                "title": "paper title",
                "engagement_level": "supporting",
                "key_role": "how this paper will support our work",
                "development_priority": "high|medium|low"
            }
        ],
        "background_papers": [
            {
                "title": "paper title",
                "engagement_level": "background",
                "key_role": "how this paper provides context",
                "citation_priority": "high|medium|low"
            }
        ]
    },
    "key_concepts": [
        {
            "concept": "important concept or distinction",
            "source": "where it comes from",
            "role": "how we'll use it",
            "development_needs": ["what we need to do to use this"]
        }
    ],
    "engagement_priorities": [
        {
            "focus": "specific engagement point",
            "papers": ["relevant papers"],
            "importance": "high|medium|low",
            "rationale": "why this is important"
        }
    ]
}"""

        self.MARKDOWN_SECTIONS = """
## Literature Synthesis

[Provide a narrative overview of how the papers fit together and relate to our project. Explain the scholarly context we're entering and how we'll position our work.]

## Key Arguments and Moves

[Analyze how arguments across papers relate to our planned moves. Identify tensions, support, and opportunities.]

## Development Strategy

[Explain how we should develop our contribution, what to emphasize, and how to manage engagement with different papers.]

## Critical Points

[Discuss key areas where we'll engage critically, explaining how different critiques work together.]

## Risks and Challenges

[Identify potential challenges and strategies for addressing them.]

## Additional Notes and Observations

[Include any important points, patterns, or considerations that don't fit elsewhere. This might include:
- Unexpected connections between papers
- Potential issues to watch for
- Suggestions about approach or methodology
- Other insights that could help project development]

## Next Stage Preparation

[Provide specific guidance for moving into argument development, including suggestions for abstract elements and outline structure.]"""

    def get_prompt(self, paper_readings: Dict, final_selection: Dict) -> str:
        return f"""You are synthesizing our analysis of multiple papers to prepare for developing our philosophical paper. Your task is to create both structured and narrative analysis that will guide our development.

Our project focus:
Thesis: {final_selection.get('current_thesis', '')}
Contribution: {final_selection.get('core_contribution', '')}
Key Moves: {final_selection.get('key_moves', [])}

You will provide two types of output:

1. Structured Data (JSON):
- Classification and organization of papers
- Key concepts and their roles
- Priority engagement points
{self.JSON_REQUIREMENTS}

2. Narrative Analysis (Markdown):
- How papers and arguments relate
- Development strategy
- Risks and opportunities
{self.MARKDOWN_REQUIREMENTS}

For the JSON output, use this format:
{self.JSON_FORMAT}

For the Markdown output, use these sections:
{self.MARKDOWN_SECTIONS}

Consider carefully:
1. How papers relate to each other
2. Which engagements are most important
3. How to maintain appropriate scope
4. What we need for next stages

Previous Readings:
{paper_readings}

Provide your synthesis starting with the JSON output, followed by the Markdown analysis."""