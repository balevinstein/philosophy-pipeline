# src/prompts/outline_development.py
from .json_format import JSONFormattingRequirements

class OutlineDevelopmentPrompts:
    """Manages prompts for outline development stage"""
    
    def __init__(self):
        self.DEVELOPMENT_CONTEXT = """
CONTEXT:
You are helping develop a detailed philosophical paper outline for publication in Analysis, one of the most prestigious journals in analytic philosophy. 

ANALYSIS REQUIREMENTS:
- Papers must be 3,000-4,000 words
- Must make a single, clear philosophical contribution
- Requires precise argumentation
- Must engage thoughtfully but efficiently with literature
- Should advance philosophical understanding through careful analysis

While Analysis papers can succeed through different combinations of elements, all successful papers share:
- Clear, focused argumentation
- Precise development of key ideas
- Efficient use of space
- Convincing defense against objections
- Sharp and precise prose
- Novel and original contribution to the field

Optional elements that may strengthen the paper when appropriate:
- Formal logical apparatus
- Technical innovations
- Carefully chosen examples
- Mathematical modeling
- Detailed case studies

The development process should strengthen core argumentative elements while thoughtfully developing optional elements where they serve the paper's goals."""

        self.JSON_FORMATTING_REQUIREMENTS = JSONFormattingRequirements

        self.ASPECT_GUIDELINES = {
            "argument_structure": """
ARGUMENT STRUCTURE FOCUS:
- Ensure each premise is clearly stated and justified
- Map logical connections explicitly
- Identify and fill any gaps in reasoning
- Maintain focus on core thesis
- Ensure each section contributes to main argument
- Balance detail with concision""",

            "example_development": """
TASK:
Write the actual examples that will appear in the paper. Do not discuss example requirements or characteristics. Generate the specific text that will be used.

Given the current state of the paper, write:
1. The complete text of the primary example exactly as it will appear in the introduction
2. The expanded version of this example that will appear in the main analysis, including any technical notation required
3. Any supporting examples needed to demonstrate scope or address objections

Your response must contain publication-ready prose that could be directly inserted into the paper. Include precise wording and any necessary technical notation.

RESPONSE REQUIREMENTS:
1. Provide ONLY concrete example text
2. Include exact wording as it would appear in the paper
3. No meta-discussion about what examples should do
4. No placeholders - all content must be fully developed""",

            "formal_framework": """
TASK:
Write the actual formal content needed for this paper. Do not discuss what formalism might be useful - provide the precise technical content exactly as it would appear in the paper.

Given this paper's specific needs, write:
1. Any formal notation that needs to be introduced
2. Any technical definitions required
3. Any mathematical results (theorems, lemmas, etc.) if needed
4. Any formal arguments or proofs required

Your response must contain publication-ready technical content that could be directly inserted into the paper. The formalism should serve the paper's specific argumentative needs - include only what is necessary and justified.

RESPONSE REQUIREMENTS:
1. Provide ONLY concrete technical content
2. Include exact wording and notation where needed
3. No meta-discussion about what formalism should do
4. No placeholders - all included content must be fully specified""",

            "objection_mapping": """
TASK:
Write the actual objections and responses that will appear in the paper. Do not discuss what objections might arise - provide the precise text of objections and their responses exactly as they would appear in the paper.

Given the paper's current state, write:
1. The exact text of potential objections
2. Complete responses to these objections
3. Any necessary technical details supporting the responses

Your response must contain publication-ready objection/response text that could be directly inserted into the paper.

RESPONSE REQUIREMENTS:
1. Provide ONLY concrete objection and response text
2. Include exact wording and any needed technical content
3. No meta-discussion about what objections might need addressing
4. No placeholders - all objections and responses must be fully developed""",

            "integration": """
INTEGRATION FOCUS:
- Ensure sections flow logically
- Verify consistent terminology
- Check argument thread remains clear
- Balance section lengths appropriately
- Verify word budget allocation
- Ensure coherent narrative arc"""
        }

        self.FOCUSED_DEVELOPMENT = """
DEVELOPMENT FOCUS:
When improving the outline, concentrate specifically on {aspect} while maintaining:
- Compatibility with existing outline elements
- Clear documentation of changes and rationale
- Explicit consideration of potential issues

{aspect_specific_guidelines}

Think carefully through each proposed change:
1. What specific improvement does it make?
2. How does it strengthen the paper?
3. What potential issues might it raise?
4. How does it fit within word constraints?"""

        
    


    def get_development_prompt(self, current_state: str, focus_aspect: str) -> str:
        """Get prompt for outline development with specific focus"""
        base_prompt = f"""
    {self.DEVELOPMENT_CONTEXT}
    {self.JSON_FORMATTING_REQUIREMENTS}

    {self.FOCUSED_DEVELOPMENT.format(
        aspect=focus_aspect,
        aspect_specific_guidelines=self.ASPECT_GUIDELINES[focus_aspect]
    )}

    Current outline state:
    {current_state}
    """

        if focus_aspect == "argument_structure":
            return base_prompt + """
    Your response must be a complete JSON object with this structure:
    {
        "analysis": {
            "current_treatment": "string describing current argument structure",
            "required_elements": ["logical elements needed"],
            "target_sections": ["sections where structure will appear"]
        },
        "proposed_content": {
            "premises": [
                {
                    "text": "string containing complete premise statement",
                    "support": "string containing supporting argument",
                    "connections": ["connections to other premises"]
                }
            ],
            "conclusions": [
                {
                    "text": "string containing conclusion statement",
                    "derivation": "string showing how conclusion follows from premises"
                }
            ]
        }
    }"""

        elif focus_aspect == "example_development":
            return f"""
    {self.DEVELOPMENT_CONTEXT}

    {self.FOCUSED_DEVELOPMENT.format(
        aspect=focus_aspect,
        aspect_specific_guidelines=self.ASPECT_GUIDELINES[focus_aspect]
    )}

    Current outline state:
    {current_state}

    Your response must be a complete JSON object with this structure:
    {{
        "analysis": {{
            "current_treatment": "string describing current example use",
            "required_features": ["features example must demonstrate"],
            "target_sections": ["sections where example will appear"]
        }},
        "proposed_content": {{
            "primary_example": {{
                "introduction_text": "string containing complete example text for introduction",
                "main_analysis_text": "string containing expanded example text for main analysis",
                "technical_elements": ["any required technical notation or formal elements"]
            }},
            "supporting_examples": [
                {{
                    "purpose": "string explaining why this example is needed",
                    "example_text": "string containing complete supporting example text"
                }}
            ]
        }},
        "overall_impact": {{
            "argument_strengthening": "string explaining how examples strengthen argument",
            "clarity_improvement": "string explaining how examples improve clarity",
            "potential_risks": "string identifying any concerns"
        }}
    }}"""
        elif focus_aspect == "formal_framework":
            return f"""
    {self.DEVELOPMENT_CONTEXT}

    {self.FOCUSED_DEVELOPMENT.format(
        aspect=focus_aspect,
        aspect_specific_guidelines=self.ASPECT_GUIDELINES[focus_aspect]
    )}

    Current outline state:
    {current_state}

    Your response must be a complete JSON object with this structure:
    {{
        "analysis": {{
            "current_treatment": "string describing current formal treatment",
            "required_elements": ["formal elements needed"],
            "target_sections": ["sections where formalism will appear"]
        }},
        "proposed_content": {{
            "technical_foundations": {{
                "notation": "string containing any required notation (or 'None needed')",
                "definitions": "string containing any required formal definitions (or 'None needed')",
                "formal_framework": "string containing any required technical framework (or 'None needed')"
            }},
            "formal_development": [
                {{
                    "element_type": "string (e.g., 'theorem', 'argument', 'proof', etc.)",
                    "content": "string containing the complete formal content"
                }}
            ]
        }},
        "overall_impact": {{
            "argument_strengthening": "string",
            "clarity_improvement": "string",
            "potential_risks": "string"
        }}
    }}"""
        elif focus_aspect == "objection_mapping":
            return f"""
            {self.DEVELOPMENT_CONTEXT}

            {self.FOCUSED_DEVELOPMENT.format(
                aspect=focus_aspect,
                aspect_specific_guidelines=self.ASPECT_GUIDELINES[focus_aspect]
            )}

            Current outline state:
            {current_state}

            Your response must be a complete JSON object with this structure:
            {{
                "analysis": {{
                    "current_treatment": "string describing current objection handling",
                    "required_elements": ["objections that must be addressed"],
                    "target_sections": ["sections where objections will appear"]
                }},
                "proposed_content": {{
                    "major_objections": [
                        {{
                            "objection_text": "string containing complete objection",
                            "response_text": "string containing complete response",
                            "technical_support": "string containing any required technical details (or 'None needed')"
                        }}
                    ],
                    "anticipated_concerns": [
                        {{
                            "concern_text": "string containing specific concern",
                            "resolution_text": "string containing complete resolution"
                        }}
                    ]
                }},
                "overall_impact": {{
                    "argument_strengthening": "string",
                    "clarity_improvement": "string",
                    "potential_risks": "string"
                }}
            }}"""

        elif focus_aspect == "integration":
            return base_prompt + """
    Your response must be a complete JSON object with this structure:
    {
        "analysis": {
            "current_treatment": "string describing current integration",
            "required_elements": ["integration points needed"],
            "target_sections": ["sections requiring integration"]
        },
        "proposed_content": {
            "transitions": [
                {
                    "from_section": "string",
                    "to_section": "string",
                    "transition_text": "string containing complete transition paragraph",
                    "connection_type": "string describing connection type"
                }
            ],
            "cross_references": [
                {
                    "source": "string identifying source content",
                    "target": "string identifying target content",
                    "reference_text": "string containing complete cross-reference text"
                }
            ]
        }
    }"""
    
    

    def get_example_development_prompt(self, current_state: str) -> str:
        """Get prompt for example development"""
        return f"""
    {self.DEVELOPMENT_CONTEXT}

    {self.JSON_FORMATTING_REQUIREMENTS}
    You are writing the actual examples that will appear in the paper. Do not describe what examples should be like - write the complete text of the examples themselves.

    Current paper state:
    {current_state}

    Your response must be a valid JSON object with this structure:
    {{
        "analysis": {{
            "target_sections": ["string"]
        }},
        "content": {{
            "primary_example": {{
                "text": "string - THE COMPLETE EXAMPLE TEXT",
                "formal_elements": "string - ANY FORMAL NOTATION NEEDED",
                "elaboration": "string - THE ACTUAL ELABORATION TEXT"
            }},
            "supporting_examples": [
                {{
                    "text": "string - THE COMPLETE EXAMPLE TEXT",
                    "connection": "string - THE ACTUAL TEXT CONNECTING TO MAIN EXAMPLE",
                    "technical_elements": "string - ANY TECHNICAL CONTENT NEEDED"
                }}
            ]
        }}
    }}

    IMPORTANT:
    - Write the complete, final text of each example
    - Include all necessary context and explanation
    - Make examples concrete and specific
    - Examples should be publication-ready
    - Do not use placeholders or describe what examples should contain"""

    def get_example_enhancement_prompt(self, initial_examples: str, current_state: str) -> str:
        """Get prompt for enhancing examples with technical precision"""
        return f"""
    {self.DEVELOPMENT_CONTEXT}
    {self.JSON_FORMATTING_REQUIREMENTS}
    You are enhancing philosophical examples to maximize their clarity and technical precision while maintaining accessibility.

    Initial examples:
    {initial_examples}

    Current paper state:
    {current_state}

    Your task is to enhance these examples by:
    1. Adding precise formal notation where helpful
    2. Clarifying logical structure
    3. Making technical connections explicit
    4. Ensuring philosophical significance remains clear

    Your response must be a complete JSON object with this structure:
    {{
        "analysis": {{
            "enhancement_goals": ["string"],
            "technical_requirements": ["string"],
            "target_sections": ["string"]
        }},
        "enhanced_examples": [
            {{
                "content_type": "example",
                "target_section": "string",
                "original_version": "string",
                "enhanced_version": "string",
                "formal_elements": {{
                    "notation": "string",
                    "structure": "string"
                }},
                "technical_notes": "string",
                "philosophical_connections": "string"
            }}
        ],
        "integration_guidance": {{
            "sequence": ["string"],
            "technical_prerequisites": ["string"],
            "connection_points": ["string"]
        }}
    }}

    Ensure all formal enhancements serve to illuminate rather than obscure the philosophical points."""

    def get_formal_development_prompt(self, current_state: str, focus_aspect: str) -> str:
        return f"""
    {self.DEVELOPMENT_CONTEXT}

    {self.JSON_FORMATTING_REQUIREMENTS}
    Write concrete text, definitions and formal content that will appear DIRECTLY in the paper. DO NOT provide commentary about what should be written.

    Current paper state:
    {current_state}

    Your response must contain only publication-ready content in this exact JSON structure. Be sure not to violate any JSON formatting requirements listed by using, e.g., too many quotation marks that might mess things up:
    {{
        "content": {{
            "text": [
                {{
                    "section": "string - SECTION NAME",
                    "content": "string - ACTUAL PAPER TEXT",
                    "formal_notation": "string - ACTUAL FORMAL NOTATION IF ANY"
                }}
            ],
            "definitions": [
                {{
                    "term": "string - THE TERM BEING DEFINED",
                    "definition": "string - THE ACTUAL COMPLETE DEFINITION",
                    "formal": "string - THE ACTUAL FORMAL EXPRESSION"
                }}
            ],
            "proofs": [
                {{
                    "title": "string - PROOF TITLE",
                    "content": "string - THE ACTUAL COMPLETE PROOF"
                }}
            ]
        }}
    }}

    IMPORTANT:
    - Provide ONLY the actual text/content that will appear in the paper
    - Write complete, publication-ready prose and formal content
    - Do not include any metacommentary or descriptions
    - Use proper formal notation where needed


    IMPORTANT:
    - Every array must end with a properly placed comma if another element follows
    - Every object must end with a properly placed comma if another key-value pair follows
    - All strings must be properly enclosed in double quotes
    - Ensure all brackets and braces are properly matched
    - Do not include any explanatory text outside the JSON structure"""

    def get_clarity_critique_prompt(self, proposed_changes: str, focus_aspect: str) -> str:
        """Get prompt for clarity/accessibility verification"""
        return f"""
    {self.DEVELOPMENT_CONTEXT}

    {self.JSON_FORMATTING_REQUIREMENTS}
    You are evaluating formal/technical content for clarity and accessibility while maintaining philosophical precision.

    Content to evaluate:
    {proposed_changes}

    Assess:
    1. Balance of technical precision and readability
    2. Clarity of formal definitions and notation
    3. Effective integration with philosophical content
    4. Accessibility to the Analysis journal audience

    Your response must be a complete JSON object with this structure:
    {{
        "clarity_assessment": {{
            "overall_accessibility": "string",
            "technical_necessity": "string",
            "audience_considerations": "string"
        }},
        "specific_critiques": [
            {{
                "element": "string",
                "clarity_issues": ["string"],
                "suggested_improvements": "string",
                "rationale": "string"
            }}
        ],
        "integration_feedback": {{
            "exposition_flow": "string",
            "prerequisite_clarity": "string",
            "connection_to_argument": "string"
        }},
        "revision_recommendations": {{
            "priority_changes": ["string"],
            "exposition_suggestions": ["string"],
            "balance_adjustments": ["string"]
        }}
    }}"""

    def get_formal_refinement_prompt(self, original_development: str, clarity_feedback: str, focus_aspect: str) -> str:
        """Get prompt for refining formal content based on clarity feedback"""
        return f"""
    {self.DEVELOPMENT_CONTEXT}

    {self.JSON_FORMATTING_REQUIREMENTS}
    You are refining formal philosophical content to optimize both technical precision and clarity.

    Original development:
    {original_development}

    Clarity feedback received:
    {clarity_feedback}

    Your task is to refine the formal content while:
    1. Maintaining technical precision
    2. Improving accessibility
    3. Strengthening philosophical connections
    4. Ensuring efficient exposition

    Your response must be a complete JSON object with this structure:
    {{
        "refinement_process": {{
            "technical_preservation": "string",
            "clarity_improvements": "string",
            "integration_strategy": "string"
        }},
        "refined_content": {{
            "formal_definitions": [
                {{
                    "term": "string",
                    "refined_definition": "string",
                    "refined_notation": "string",
                    "exposition_notes": "string"
                }}
            ],
            "technical_framework": {{
                "refined_elements": ["string"],
                "refined_axioms": ["string"],
                "clarity_enhancements": ["string"]
            }},
            "formal_development": [
                {{
                    "element_type": "string",
                    "refined_content": "string",
                    "accessibility_notes": "string",
                    "technical_notes": "string"
                }}
            ]
        }},
        "verification": {{
            "technical_accuracy": "string",
            "clarity_achieved": "string",
            "philosophical_connection": "string",
            "exposition_efficiency": "string"
        }}
    }}

    Ensure all refined content maintains technical precision while improving clarity."""
    
  

    def get_critique_prompt(self, proposed_changes: str, focus_aspect: str) -> str:
        """Get prompt for critiquing concrete content"""
        base_critique = f"""
    {self.DEVELOPMENT_CONTEXT}

    {self.JSON_FORMATTING_REQUIREMENTS}
    You are acting as a critic evaluating concrete content for the paper. Assess both technical accuracy and philosophical effectiveness.

    Content to evaluate:
    {proposed_changes}

    Your response must be a complete JSON object with this structure:
    {{
        "analysis_process": {{
            "technical_assessment": ["specific technical strengths or issues"],
            "philosophical_assessment": ["specific philosophical strengths or issues"],
            "practical_assessment": ["specific practical strengths or issues"],
            "word_budget_impact": "string"
        }},
        "content_evaluation": {{
            "strengths": ["specific content elements that work well"],
            "weaknesses": ["specific content elements needing improvement"],
            "accuracy_concerns": ["specific technical or philosophical inaccuracies"]
        }},
        "specific_critiques": [
            {{
                "content_element": "string identifying specific content",
                "technical_assessment": "string evaluating technical aspects",
                "philosophical_assessment": "string evaluating philosophical contribution",
                "suggested_revisions": "string containing specific textual improvements"
            }}
        ],
        "recommendations": {{
            "content_to_keep": ["specific content to retain"],
            "content_to_modify": {{
                "original": "string containing original content",
                "suggested_revision": "string containing specific revisions",
                "rationale": "string explaining necessity of changes"
            }},
            "content_to_remove": {{
                "content": "string identifying content to remove",
                "reason": "string explaining basis for removal",
                "alternative": "string suggesting replacement content"
            }}
        }}
    }}"""

        return base_critique

    def get_refinement_prompt(self, original_changes: str, critique: str, focus_aspect: str) -> str:
        """Get prompt for refining concrete content"""
        base_refinement = f"""
    {self.DEVELOPMENT_CONTEXT}

    {self.JSON_FORMATTING_REQUIREMENTS}

    You are refining concrete content based on critical feedback. Produce improved content that addresses the critiques while maintaining technical precision and philosophical insight.

    Original content:
    {original_changes}

    Critique received:
    {critique}

    Your response must be a complete JSON object with this structure. ENSURE THE JSON IS PROPERLY FORMATTED AND ALL COMMAS ARE CORRECTLY PLACED:
    {{
        "refinement_process": {{
            "technical_resolution": "string explaining how technical issues were addressed",
            "philosophical_resolution": "string explaining how philosophical issues were addressed",
            "integration_strategy": "string explaining how content fits paper development"
        }},
        "refined_content": [
            {{
                "content_type": "string (e.g., 'example', 'formal_definition', 'objection')",
                "original_version": "string containing original content",
                "refined_version": "string containing improved content",
                "technical_notes": "string explaining technical improvements",
                "philosophical_notes": "string explaining philosophical improvements"
            }}
        ],
        "verification": {{
            "technical_accuracy": "string confirming technical correctness",
            "philosophical_contribution": "string confirming philosophical value",
            "integration_check": "string confirming fit with paper"
        }}
    }}"""

        return base_refinement