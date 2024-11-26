# src/prompts/development.py
from datetime import datetime
from typing import Dict, Any, Optional

class TopicAnalysisPrompt:
    """Initial topic analysis and selection"""
    
    def __init__(self):
        self.CONTEXT = """
CONTEXT:
You are part of an autonomous philosophical research pipeline where multiple LLMs collaborate to write a paper for Analysis journal. Your task is to select and begin developing AT MOST three topics from the provided list that are most promising for AI development.

Previous stages have generated topics and provided initial evaluation. However, you should make your own assessment, treating previous evaluations as input but not as binding."""

        self.SELECTION_CRITERIA = """
SELECTION CRITERIA:
1. AI Development Potential
   - Topic should leverage LLM strengths (logical analysis, argument evaluation, clear exposition)
   - Should avoid heavy reliance on areas of LLM weakness (empirical analysis, deep historical interpretation)
   - Must be developable through structured API calls with clear outputs
   
2. Philosophical Merit
   - Clear, novel contribution to existing literature
   - Well-defined scope suitable for 4,000-word paper
   - Tractable argument structure
   
3. Development Pathway
   - Clear steps for argument construction
   - Manageable literature engagement
   - Identifiable potential objections and responses
   
4. Risk Assessment
   - Likelihood of generating genuine insight
   - Potential pitfalls in development
   - Distinctness from existing work"""

        self.OUTPUT_FORMAT = """
Your response must be a JSON object with this structure:
{
    "selected_topics": [
        {
            "title": "string",
            "development_rationale": {
                "ai_suitability": "string",
                "pitfall_avoidance": "string",
                "strength_leverage": "string"
            },
            "core_analysis": {
                "central_thesis": "string",
                "key_claims": ["string"],
                "critical_assumptions": ["string"],
                "argument_sequence": ["string"],
                "section_breakdown": ["string"],
                "proof_strategy": "string"
            },
            "literature_strategy": {
                "key_papers": ["string"],
                "engagement_points": ["string"],
                "primary_tensions": ["string"],
                "resolution_strategy": "string",
                "literature_scope": "string",
                "advancement_claim": "string"
            },
            "development_guidance": {
                "key_definitions": ["string"],
                "formal_requirements": "string",
                "crucial_distinctions": ["string"],
                "scope_limitations": ["string"]
            },
            "development_risks": {
                "potential_failures": ["string"],
                "mitigation_strategies": ["string"],
                "success_criteria": ["string"]
            }
        }
    ],
    "selection_rationale": "string",
    "development_priority": "string",
    "cross_topic_synergies": "string"
}"""

    def get_prompt(self, topics_json: str, culling_json: str) -> str:
        """Construct the full evaluation prompt"""
        return f"""You are an expert in analytic philosophy participating in an autonomous philosophical research project where LLMs collaborate to write papers suitable for Analysis journal.

{self.CONTEXT}

{self.SELECTION_CRITERIA}

{self.OUTPUT_FORMAT}

Previously generated topics:
{topics_json}

Previous evaluation:
{culling_json}

Analyze the topics carefully and select AT MOST THREE that are most promising for AI development. Consider both the philosophical merit and the practical feasibility for AI development. Your selection may differ from previous evaluations if you identify stronger candidates."""

class DevelopmentMetadata:
    """Tracks the development state and history of each topic"""
    
    def __init__(self):
        self.metadata_template = {
            "pipeline_state": {
                "current_stage": "",
                "stages_completed": [],
                "next_stage": "",
                "timestamp": ""
            },
            "development_history": {
                "analysis_completion": "",
                "abstract_completion": "",
                "argument_completion": "",
                "outline_completion": ""
            },
            "quality_metrics": {
                "novelty_score": 0.0,
                "coherence_score": 0.0,
                "development_potential": 0.0
            },
            "revision_tracking": {
                "major_revisions": [],
                "current_version": 1,
                "last_modified": ""
            }
        }

class AbstractDevelopmentPrompt:
    """Develops detailed abstracts for selected topics"""
    
    def __init__(self):
        self.CONTEXT = """
CONTEXT:
You are developing detailed abstracts for philosophical papers as part of an AI research pipeline. Each abstract should clearly present the paper's thesis, approach, and contribution while setting up the argument structure."""

        self.REQUIREMENTS = """
ABSTRACT REQUIREMENTS:
1. Length: Approximately 300 words
2. Structure:
   - Problem/context statement
   - Gap in literature
   - Main thesis
   - Key moves/approach
   - Contribution/significance
3. Must integrate with provided development guidance
4. Should set up clear expectations for argument structure"""

        self.OUTPUT_FORMAT = """
Your response must be a JSON object with this structure:
{
    "topic_abstracts": [
        {
            "title": "string",
            "abstract": "string",
            "key_terms_defined": ["string"],
            "argument_preview": ["string"],
            "literature_engagement": ["string"],
            "development_notes": {
                "crucial_sections": ["string"],
                "potential_challenges": ["string"],
                "resolution_strategies": ["string"]
            }
        }
    ]
}"""

    def get_prompt(self, analysis_json: str) -> str:
        return f"""You are developing detailed abstracts for promising philosophical papers.

{self.CONTEXT}

{self.REQUIREMENTS}

{self.OUTPUT_FORMAT}

Previous analysis:
{analysis_json}

Develop detailed abstracts that build on the previous analysis while setting up clear paths for argument development."""




class StructurePlanningPrompt:
    """First stage: High-level outline planning"""
    
    def __init__(self):
        self.CONTEXT = """
CONTEXT:
You are part of an autonomous philosophical research pipeline where multiple LLMs collaborate to write papers for Analysis journal. Your task is to develop a detailed structural plan that will guide section-by-section development.

Analysis is one of the most prestigious journals in analytic philosophy. Successful Analysis papers typically:
- Make a single, clear philosophical contribution
- Maintain precise argumentation
- Engage thoughtfully but efficiently with literature
- Complete their argument within 3,000-4,000 words
- Advance philosophical understanding through careful analysis

This outline phase must consider LLM capabilities:
STRENGTHS:
- Logical analysis and formal reasoning
- Identifying conceptual tensions
- Systematic evaluation of arguments
- Clear exposition of defined concepts
- Working with explicit premises and conclusions

WEAKNESSES:
- Heavy reliance on recent literature
- Complex historical interpretation
- Detailed empirical analysis
- Subtle linguistic intuitions
- Heavy context-dependent reasoning"""

        self.REQUIREMENTS = """
OUTLINE REQUIREMENTS:
1. Structure
   - Clear progression of ideas
   - Efficient use of word budget
   - Strategic literature placement
   - Precise argument development
   
2. Content Planning
   - Front-load key definitions
   - Build argument systematically
   - Anticipate objections
   - Maintain focus on core thesis

3. Analysis Standards
   - Rigorous but accessible argumentation
   - Clear advancement over existing work
   - Philosophical significance evident
   - Manageable scope"""

        self.OUTPUT_FORMAT = """
Your response must be a JSON object with this structure:
{
    "paper_structure": {
        "title": "string",
        "core_thesis": "string",
        "target_audience": "string",
        "sections": [
            {
                "section_title": "string",
                "target_length": "integer",
                "key_claims": ["string"],
                "required_setup": ["string"],
                "core_moves": ["string"],
                "dependencies": ["string"],
                "technical_requirements": ["string"],
                "literature_engagement": ["string"],
                "potential_pitfalls": ["string"]
            }
        ],
        "development_sequence": ["string"],
        "integration_points": {
            "literature": ["string"],
            "formal_elements": ["string"],
            "examples": ["string"]
        },
        "word_budget": {
            "introduction": "integer",
            "setup": "integer",
            "main_argument": "integer",
            "objections": "integer",
            "conclusion": "integer"
        }
    }
}"""

    def get_prompt(self, abstracts_json: str) -> str:
        return f"""You are developing a detailed structural plan for Analysis journal papers.

        {self.CONTEXT}

        {self.REQUIREMENTS}

        {self.OUTPUT_FORMAT}

        Previously developed abstracts:
        {abstracts_json}

        Develop a detailed structural plan for each abstract, ensuring clear progression and efficient word usage."""


class SectionDevelopmentPrompt:

    """Second stage: Detailed section development"""
    
    def __init__(self):
        self.CONTEXT = """
CONTEXT:
You are developing detailed content for specific sections of an Analysis paper as part of an autonomous LLM research pipeline. Your task is to transform the structural plan into detailed, publication-ready section content.

Key Considerations:
1. Analysis Style
   - Clear, direct prose
   - Precise argumentation
   - Efficient use of technical apparatus
   - Strategic example placement
   - Focused literature engagement

2. Development Guidelines
   - Build argument systematically
   - Maintain clear thread to thesis
   - Balance detail with word constraints
   - Ensure accessibility to philosophy audience
   - Support all key claims"""

        self.REQUIREMENTS = """
SECTION DEVELOPMENT REQUIREMENTS:
1. Format
   - Use academic markdown with LaTeX where needed
   - Clear subsection structure
   - Explicit argument markers
   - Literature integration points noted

2. Content
   - Clear connection to paper thesis
   - Explicit premise-conclusion structure
   - Anticipated objections
   - Key definitions where needed
   - Examples that illuminate rather than distract

3. Style
   - Professional academic tone
   - Precise philosophical language
   - Clear signposting
   - Efficient prose
   - Natural transitions"""

        self.FORMAT_GUIDE = """
Expected markdown structure:
# Section Title

## Motivation and Setup

[Clear introduction of section's role in overall argument]

## Core Development

### Key Argument
- Premise 1: [Clear statement]
- Premise 2: [Clear statement]
- Therefore: [Conclusion]

[Development and support...]

\\begin{align*}
[Formal notation as needed]
\\end{align*}

> **Literature Connection:** Engagement with [paper/argument]

### Potential Objection
[Anticipated counterargument and response]

## Section Conclusion
[Clear statement of progress made]"""

    def get_prompt(self, structure_json: str, section_focus: str, previous_sections: str = "") -> str:
        return f"""You are developing detailed content for a section of an Analysis paper as part of an autonomous LLM research project.

{self.CONTEXT}

{self.REQUIREMENTS}

{self.FORMAT_GUIDE}

Paper structure:
{structure_json}

Previously developed sections:
{previous_sections}

Focus section:
{section_focus}

Develop detailed markdown content for this section, ensuring it builds properly on previous sections and maintains focus on the paper's core thesis."""


class DevelopmentPrompts:
    """Manages prompts for the broad development phase"""
    
    def __init__(self):
        self.topic_analysis = TopicAnalysisPrompt()
        self.abstract_development = AbstractDevelopmentPrompt()
        self.structure_planning = StructurePlanningPrompt()
        self.section_development = SectionDevelopmentPrompt()
        self.metadata = DevelopmentMetadata()
    
    def update_metadata(self, topic_id: str, stage: str, metrics: Optional[Dict] = None) -> Dict:
        """Updates metadata for a given topic at a specific stage"""
        metadata = self.metadata.metadata_template.copy()
        metadata["pipeline_state"]["current_stage"] = stage
        metadata["pipeline_state"]["timestamp"] = datetime.now().isoformat()
        if metrics:
            metadata["quality_metrics"].update(metrics)
        return metadata