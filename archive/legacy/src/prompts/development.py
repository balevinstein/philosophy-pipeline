# src/prompts/development.py
from datetime import datetime
from typing import Dict, Any, Optional

class TopicAnalysisPrompt:
    """Initial topic analysis and selection of topics for full development"""
    
    def __init__(self):
        self.CONTEXT = """
CONTEXT:
You are part of an autonomous philosophical research pipeline where multiple LLMs collaborate to write papers for Analysis journal. Your task is to identify AT MOST THREE topics that warrant full development and detailed comparison.

While only one paper will ultimately be chosen, at this stage we need multiple promising candidates for thorough development and comparison. Previous stages have generated topics and provided initial evaluation, but you should make your own assessment, treating previous evaluations as input but not as binding."""

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
   
4. Comparative Assessment Potential
   - Clear criteria for evaluation
   - Measurable progress indicators
   - Comparable development challenges
   - Features that will enable informed final selection"""

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
            },
            "selection_metrics": {
                "philosophical_novelty": "string",
                "technical_feasibility": "string",
                "development_clarity": "string"
            }
        }
    ],
    "selection_rationale": "string",
    "development_priority": "string",
    "comparative_assessment_criteria": ["string"]
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

Analyze the topics carefully and select AT MOST THREE that warrant full development. Consider both philosophical merit and practical feasibility, while ensuring selected topics can be meaningfully compared for final selection. Your selection may differ from previous evaluations if you identify stronger candidates."""

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
                "development_potential": 0.0,
                "implementation_clarity": 0.0
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
You are developing detailed abstracts for philosophical papers as part of an AI research pipeline. Each abstract should clearly present the paper's thesis, approach, and contribution while setting up the argument structure.

DEVELOPMENT PRINCIPLES:
1. Equal Depth
   - Develop each abstract to full potential
   - Maintain consistent quality across all abstracts
   - Each abstract deserves thorough treatment for fair comparison

2. Independent Development
   - Each abstract developed fully on its own merits
   - Clear documentation of unique strengths and challenges
   - Thorough exploration of argument potential

3. Selection Relevance
   - Note features that affect development viability
   - Track potential implementation challenges
   - Document special requirements or opportunities"""

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
4. Should set up clear expectations for argument structure
5. Must enable comparative assessment"""

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
                "resolution_strategies": ["string"],
                "development_features": {
                    "technical_requirements": "string",
                    "argument_complexity": "string",
                    "literature_demands": "string"
                }
            }
        }
    ],
    "development_assessment": {
        "relative_technical_demands": ["string"],
        "implementation_challenges": ["string"],
        "distinctive_features": ["string"]
    }
}"""

    def get_prompt(self, analysis_json: str) -> str:
        return f"""You are developing detailed abstracts for promising philosophical papers.

{self.CONTEXT}

{self.REQUIREMENTS}

{self.OUTPUT_FORMAT}

Previous analysis:
{analysis_json}

Develop detailed abstracts for each selected topic, ensuring thorough and equal development to enable informed comparison. Each abstract should stand on its own merits while providing clear indicators for comparative assessment."""

class StructurePlanningPrompt:
    """First stage: High-level outline planning"""
    
    def __init__(self):
        self.CONTEXT = """
CONTEXT:
You are part of an autonomous philosophical research pipeline where multiple LLMs collaborate to write papers for Analysis journal. Your task is to develop detailed structural plans for ALL topics that have reached this stage.

DEVELOPMENT PRINCIPLES:
1. Equal Depth
   - Develop structural plans for all topics to same level
   - Maintain consistent detail and scope
   - Enable fair comparison through parallel development

2. Independent Development
   - Each topic planned on its own merits
   - Full exploration of structural possibilities
   - Clear tracking of unique requirements

3. Selection Relevance
   - Note features affecting final viability
   - Track implementation challenges
   - Document development requirements

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
   - Manageable scope

4. Development Assessment
   - Track technical requirements
   - Note development challenges
   - Identify unique features"""

        self.OUTPUT_FORMAT = """
Your response must be a JSON object with this structure:
{
    "paper_structures": [
        {
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
            },
            "development_assessment": {
                "technical_complexity": "string",
                "argument_clarity": "string",
                "implementation_challenges": "string"
            }
        }
    ],
    "comparative_notes": {
        "relative_complexity": ["string"],
        "development_challenges": ["string"],
        "distinctive_features": ["string"]
    }
}"""

    def get_prompt(self, abstracts_json: str) -> str:
        return f"""You are developing detailed structural plans for Analysis journal papers.

{self.CONTEXT}

{self.REQUIREMENTS}

{self.OUTPUT_FORMAT}

Previously developed abstracts:
{abstracts_json}

Develop detailed structural plans for all topics, ensuring equal depth of development while maintaining focus on features relevant to final selection."""

class SectionDevelopmentPrompt:
    """Second stage: Detailed section development"""
    
    def __init__(self):
        self.CONTEXT = """
CONTEXT:
You are part of an autonomous philosophical research pipeline where multiple LLMs collaborate to write papers for Analysis journal. Your task is to develop detailed section content for ALL topics that have reached this stage.

Each topic deserves full development to enable informed final selection. While earlier stages appropriately culled less promising topics, remaining topics should be developed with equal thoroughness to reveal their full potential.

DEVELOPMENT PRINCIPLES:
1. Equal Depth
   - Develop all sections to full potential
   - Maintain consistent quality
   - Enable fair comparison

2. Independent Development
   - Each paper developed on its own merits
   - Clear tracking of progress
   - Full exploration of argument potential

3. Selection Relevance
   - Note features affecting viability
   - Track development challenges
   - Document special requirements

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
   - Natural transitions

4. Assessment Preparation
   - Track development progress
   - Note implementation challenges
   - Document special features"""

        self.OUTPUT_FORMAT = """
Your response must be a JSON object with this structure:
{
    "paper_developments": [
        {
            "title": "string",
            "sections": [
                {
                    "section_title": "string",
                    "content": "string",
                    "key_moves": ["string"],
                    "technical_elements": ["string"],
                    "literature_connections": ["string"]
                }
            ],
            "development_notes": {
                "strengths": ["string"],
                "challenges": ["string"],
                "unique_features": ["string"],
                "implementation_requirements": ["string"]
            }
        }
    ],
    "development_assessment": {
        "relative_progress": ["string"],
        "implementation_challenges": ["string"],
        "distinctive_features": ["string"]
    }
}"""

        self.FORMAT_GUIDE = """
Expected markdown structure for each section:
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
        return f"""You are developing detailed content for selected sections of Analysis papers as part of an autonomous LLM research project.

{self.CONTEXT}

{self.REQUIREMENTS}

{self.FORMAT_GUIDE}

Paper structures:
{structure_json}

Previously developed sections:
{previous_sections}

Focus sections:
{section_focus}

Develop detailed section content for all papers, ensuring equal depth of development while maintaining focus on features relevant to final selection."""

class FinalSelectionPrompt:
    """Final selection of paper for full development"""
    
    def __init__(self):
        self.CONTEXT = """
CONTEXT:
You are part of an autonomous philosophical research pipeline where multiple LLMs collaborate to write papers for Analysis journal. Your task is to select the SINGLE most promising paper for full development, based on the parallel development work done so far.

This choice is crucial as the selected paper will be developed entirely through LLM interactions. The choice must therefore balance:
1. Philosophical merit and novelty
2. Feasibility for AI development
3. Demonstrated progress in initial development

Key LLM Capabilities to Consider:
STRENGTHS:
- Logical analysis and formal reasoning
- Systematic argument evaluation
- Clear exposition of defined concepts
- Working with explicit premises and conclusions
- Mathematical and formal manipulation

LIMITATIONS:
- Heavy reliance on recent or obscure literature
- Complex historical interpretation
- Detailed empirical analysis
- Subtle linguistic intuitions
- Heavy context-dependent reasoning"""

        self.EVALUATION_CRITERIA = """
EVALUATION CRITERIA:
1. Development Success
   - Quality of initial sections
   - Clarity of argument structure
   - Technical precision and control
   - Effective literature engagement
   
2. Implementation Feasibility
   - Alignment with LLM capabilities
   - Manageable technical requirements
   - Clear development pathway
   - Bounded scope
   
3. Philosophical Promise
   - Novelty of contribution
   - Significance of insights
   - Potential impact
   - Resilience to objections

4. Practical Considerations
   - Word limit manageability (4,000 words)
   - Literature engagement scope
   - Technical apparatus requirements
   - Clarity of success criteria"""

        self.OUTPUT_FORMAT = """
Your response must be a JSON object with this structure:
{
    "selected_paper": {
        "title": "string",
        "selection_rationale": {
            "development_quality": "string",
            "ai_feasibility": "string",
            "philosophical_merit": "string",
            "practical_advantages": "string"
        },
        "key_strengths": ["string"],
        "development_recommendations": ["string"],
        "success_criteria": ["string"]
    },
    "comparative_analysis": {
        "development_assessment": {
            "paper_title": "string",
            "section_quality": "string",
            "argument_clarity": "string",
            "technical_control": "string"
        },
        "feasibility_comparison": {
            "relative_strengths": ["string"],
            "implementation_challenges": ["string"],
            "risk_assessment": ["string"]
        }
    },
    "selection_confidence": "string",
    "development_guidance": {
        "key_focus_areas": ["string"],
        "potential_pitfalls": ["string"],
        "mitigation_strategies": ["string"]
    }
}"""

    def get_prompt(self, analysis_json: str, abstracts_json: str, outlines_json: str, developments_json: str) -> str:
        return f"""You are making the final selection of which paper to develop fully in an autonomous philosophical research pipeline.

{self.CONTEXT}

{self.EVALUATION_CRITERIA}

{self.OUTPUT_FORMAT}

Topic analysis:
{analysis_json}

Abstracts developed:
{abstracts_json}

Outlines created:
{outlines_json}

Section developments:
{developments_json}

Based on all parallel development so far, select the SINGLE most promising paper for full development. Consider both philosophical merit and practical feasibility for AI development. Provide detailed rationale for your selection and clear guidance for further development."""



class DevelopmentPrompts:
    """Manages prompts for the broad development phase"""
    
    def __init__(self):
        self.topic_analysis = TopicAnalysisPrompt()
        self.abstract_development = AbstractDevelopmentPrompt()
        self.structure_planning = StructurePlanningPrompt()
        self.section_development = SectionDevelopmentPrompt()
        self.final_selection = FinalSelectionPrompt()
        self.metadata = DevelopmentMetadata()
    
    def update_metadata(self, topic_id: str, stage: str, metrics: Optional[Dict] = None) -> Dict:
        """Updates metadata for a given topic at a specific stage"""
        metadata = self.metadata.metadata_template.copy()
        metadata["pipeline_state"]["current_stage"] = stage
        metadata["pipeline_state"]["timestamp"] = datetime.now().isoformat()
        if metrics:
            metadata["quality_metrics"].update(metrics)
        return metadata