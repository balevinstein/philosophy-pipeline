# src/prompts/conceptual_topic_development.py
import json


class TopicDevelopmentPrompt:
    """Manages prompts for developing promising philosophy paper topics"""

    def __init__(self):
        self.LITERATURE_ASSESSMENT = """
LITERATURE ASSESSMENT GUIDELINES:
For this topic, identify 2-3 papers that would be relevant for engagement. Be explicit about your confidence level for each paper and honest about any uncertainty.

Key Requirements:
1. Paper Identification
   - Suggest papers you believe exist in the literature
   - Be explicit about how confident you are in remembering each paper
   - Distinguish between specific memories and general sense
   - If uncertain about literature fit, say so

2. Engagement Analysis
   - For each paper, identify key arguments we'd engage with
   - Note specific points of departure
   - Flag any potential conflicts or overlaps
   - Highlight areas needing verification

3. Literature Positioning
   - Identify clear gaps we could fill
   - Note how our contribution differs
   - Flag any concerns about literature fit
   - Be explicit about areas of uncertainty"""

        self.DEVELOPMENT_TESTING = """
DEVELOPMENT TESTING GUIDELINES:
Using our literature context, test key aspects of the topic's development potential.

Key Requirements:
1. Argument Testing
   - Try out a key argumentative move in detail
   - Identify crucial assumptions
   - Look for potential weak points
   - Note where argument might need strengthening

2. Example Work
   - Generate a detailed example that illustrates the core idea
   - Test how well it works
   - Look for potential counterexamples
   - Note any limitations or concerns

3. Objection Mapping
   - Identify strongest potential objections
   - Develop possible responses
   - Note where responses might need work
   - Flag particularly concerning objections"""

        self.REFINEMENT_GUIDANCE = """
REFINEMENT GUIDELINES:
Based on our literature assessment and development testing, suggest improvements while maintaining the core contribution.

Key Requirements:
1. Thesis Development
   - Sharpen the central claim
   - Clarify key distinctions
   - Adjust scope as needed
   - Improve overall framing

2. Improvement Areas
   - Address identified weaknesses
   - Strengthen potential problem areas
   - Clarify ambiguous points
   - Polish presentation

3. Risk Assessment
   - Note remaining challenges
   - Identify areas needing work
   - Flag potential development issues
   - Assess overall viability"""

        self.OUTPUT_FORMATS = {
            "literature": """
{
    "key_papers": [
        {
            "title": "string",  # plausible paper title
            "confidence": "high|medium|low",  # confidence in memory
            "memory_type": "specific|general",  # specific vs general recollection
            "core_argument": "string",
            "engagement_points": ["string"],
            "potential_issues": ["string"]
        }
    ],
    "literature_confidence": {
        "overall_rating": "high|medium|low",
        "uncertainty_notes": ["string"],
        "verification_needs": ["string"]
    },
    "literature_gaps": ["string"],
    "engagement_strategy": "string"
}""",
            "development": """
{
    "sample_argument": {
        "key_move": "string",
        "assumptions": ["string"],
        "potential_weaknesses": ["string"],
        "strengthening_needs": ["string"]
    },
    "example_case": {
        "description": "string",
        "effectiveness": "string",
        "limitations": ["string"],
        "potential_counters": ["string"]
    },
    "potential_objections": ["string"],
    "responses": ["string"],
    "remaining_concerns": ["string"]
}""",
            "refinement": """
{
    "sharpened_thesis": "string",
    "scope_adjustments": ["string"],
    "polished_framing": "string",
    "remaining_challenges": {
        "conceptual_issues": ["string"],
        "development_needs": ["string"],
        "risk_assessment": "string"
    }
}""",
        }

    def get_literature_prompt(self, topic_info: dict) -> str:
        """Generate prompt for literature assessment phase"""
        return f"""You are assisting in developing a philosophy paper topic for Analysis journal. Assess the literature engagement potential for this topic:

{json.dumps(topic_info, indent=2)}

{self.LITERATURE_ASSESSMENT}

Important:
- Be explicit about your confidence in paper suggestions
- Note areas where memory is uncertain
- Flag any concerns about literature fit
- Don't make up or guess at paper details you're unsure about

Your response must be valid JSON matching this structure.
Be sure to:
-Avoid special characters (quotes, unicode) in text fields
-Use simple ASCII characters only
-Keep all text fields as single-line strings (no line breaks)
{self.OUTPUT_FORMATS['literature']}"""

    def get_development_prompt(self, topic_info: dict, lit_results: dict) -> str:
        """Generate prompt for development testing phase"""
        return f"""You are assisting in developing a philosophy paper topic for Analysis journal. Test the development potential of this topic:

Topic Information:
{json.dumps(topic_info, indent=2)}

Literature Assessment:
{json.dumps(lit_results, indent=2)}

{self.DEVELOPMENT_TESTING}

Your response must be valid JSON matching this structure:
Be sure to:
-Avoid special characters (quotes, unicode) in text fields
-Use simple ASCII characters only
-Keep all text fields as single-line strings (no line breaks)
{self.OUTPUT_FORMATS['development']}"""

    def get_refinement_prompt(
        self, topic_info: dict, lit_results: dict, dev_results: dict
    ) -> str:
        """Generate prompt for refinement phase"""
        return f"""You are assisting in developing a philosophy paper topic for Analysis journal. Based on our testing, propose refinements for this topic:

Topic Information:
{json.dumps(topic_info, indent=2)}

Literature Assessment:
{json.dumps(lit_results, indent=2)}

Development Testing:
{json.dumps(dev_results, indent=2)}

{self.REFINEMENT_GUIDANCE}

Your response must be valid JSON matching this structure:
Be sure to:
-Avoid special characters (quotes, unicode) in text fields
-Use simple ASCII characters only
-Keep all text fields as single-line strings (no line breaks)
{self.OUTPUT_FORMATS['refinement']}"""
