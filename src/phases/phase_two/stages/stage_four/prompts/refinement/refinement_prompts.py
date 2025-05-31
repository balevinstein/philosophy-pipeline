from typing import Dict, Any, List, Optional
import json


class OutlineRefinementPrompts:
    """Prompts for refining detailed outline development in Phase II.4."""

    def __init__(self):
        self.system_prompt = """You are an expert philosophy editor refining paper outlines for publication. Your role is to transform outlines into comprehensive blueprints based on critique. You must produce polished, detailed outlines that guide subsequent paper development. Your refinements will be used in an automated pipeline."""

    def get_refinement_prompt(
        self,
        outline_development: str,
        critique: str,
        framework: Dict[str, Any],
        developed_key_moves: Any,
        development_phase: str = "framework_integration",
        previous_versions: List[str] = None,
        iteration: int = 0,
    ) -> str:
        """
        Get the appropriate refinement prompt based on the development phase.
        """
        # Initialize previous_versions if None
        if previous_versions is None:
            previous_versions = []
            
        # Extract assessment and recommendations from critique if not provided
        assessment = "NEEDS REFINEMENT"
        recommendations = []
        
        # Try to extract assessment from critique
        assessment_indicators = [
            "MAJOR REVISION NEEDED", 
            "MINOR REFINEMENT NEEDED", 
            "GOOD", 
            "VERY GOOD", 
            "EXCELLENT"
        ]
        
        for indicator in assessment_indicators:
            if indicator in critique:
                assessment = indicator
                break
                
        # Try to extract recommendations from critique
        if "Recommendations" in critique:
            recommendations_section = critique.split("Recommendations", 1)[1].split("##", 1)[0].strip()
            
            # Extract numbered or bulleted items
            import re
            pattern = r"(?:^|\n)[\s]*(?:[0-9]+\.|\-|\*)\s*(.+?)(?=(?:\n[\s]*(?:[0-9]+\.|\-|\*))|$)"
            matches = re.findall(pattern, recommendations_section, re.DOTALL)
            
            if matches:
                recommendations = [match.strip() for match in matches if match.strip()]
        
        if development_phase == "framework_integration":
            return self.get_framework_integration_refinement_prompt(
                outline_development, critique, assessment, recommendations, framework, developed_key_moves, previous_versions, iteration
            )
        elif development_phase == "literature_mapping":
            return self.get_literature_mapping_refinement_prompt(
                outline_development, critique, assessment, recommendations, framework, developed_key_moves, previous_versions, iteration
            )
        elif development_phase == "content_development":
            return self.get_content_development_refinement_prompt(
                outline_development, critique, framework, developed_key_moves, previous_versions
            )
        elif development_phase == "structural_validation":
            return self.get_structural_validation_refinement_prompt(
                outline_development, critique, assessment, recommendations, framework, developed_key_moves, previous_versions, iteration
            )
        else:
            # Default to framework integration if we don't recognize the phase
            return self.get_framework_integration_refinement_prompt(
                outline_development, critique, assessment, recommendations, framework, developed_key_moves, previous_versions, iteration
            )

    def get_framework_integration_refinement_prompt(
        self,
        outline_development: str,
        critique: str,
        assessment: str,
        recommendations: List[str],
        framework: Dict[str, Any],
        developed_key_moves: Any,
        previous_versions: List[str] = None,
        iteration: int = 0,
    ) -> str:
        """
        Construct prompt for refining the framework integration phase.
        
        This focuses on improving the foundational structure based on critique.
        """
        # Initialize previous_versions if None
        if previous_versions is None:
            previous_versions = []
            
        # Get the main thesis and contribution from the framework
        main_thesis = framework.get("main_thesis", "")
        core_contribution = framework.get("core_contribution", "")
        
        # Prepare key moves texts for inclusion in prompt
        key_moves_texts = []
        
        # Handle different formats of developed_key_moves
        if isinstance(developed_key_moves, dict) and "developed_moves" in developed_key_moves:
            moves_list = developed_key_moves.get("developed_moves", [])
            for move in moves_list:
                if isinstance(move, dict):
                    move_text = move.get("key_move_text", "")
                    if move_text:
                        key_moves_texts.append(move_text)
        elif isinstance(developed_key_moves, list):
            for move in developed_key_moves:
                if isinstance(move, dict):
                    move_text = move.get("key_move_text", move.get("name", ""))
                    if not move_text:
                        # Try finding any text field in the move
                        for key in ["text", "description", "content", "final_content"]:
                            if key in move:
                                move_text = move.get(key, "")
                                break
                    if move_text:
                        key_moves_texts.append(move_text)
                elif isinstance(move, str):
                    key_moves_texts.append(move)
        
        key_moves_list = "\n".join([f"- {move}" for move in key_moves_texts])
        
        # Format recommendations into a list
        recommendations_list = "\n".join([f"- {rec}" for rec in recommendations])
        
        # Add a section about previous versions if they exist
        previous_versions_text = ""
        if previous_versions and len(previous_versions) > 1 and iteration > 0:
            previous_versions_text = f"""
## Previous Version History
This is iteration {iteration+1} of the outline development process. Please consider the following context:

- There are {len(previous_versions)} versions in the history
- This refinement should build on improvements already made
- Focus on addressing the specific recommendations from the critique
"""
        
        prompt = f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.4 (Detailed Outline Development).
You are refining the FRAMEWORK INTEGRATION phase based on critique.
Your task is to implement improvements while maintaining existing framework strengths.
The goal is a structure that properly accommodates all key moves with logical progression.
</context>

<task>
Refine the foundational structure for a philosophical paper based on critique.
Implement improvements while maintaining existing framework strengths.
Create a structure that properly accommodates all key moves.
Ensure appropriate word count allocations and logical progression.
</task>

<input_data>
CURRENT STRUCTURE:
```
{outline_development}
```

CRITIQUE:
```
{critique}
```

ASSESSMENT: {assessment}

RECOMMENDATIONS:
{recommendations_list}

MAIN THESIS:
{main_thesis}

CORE CONTRIBUTION:
{core_contribution}

KEY MOVES:
{key_moves_list}
{previous_versions_text}
</input_data>

<requirements>
1. Carefully implement critic's recommendations while preserving strengths
2. Ensure all key moves properly accommodated with explicit mapping
3. Maintain appropriate word count allocations
4. Preserve or enhance logical flow from introduction through conclusion
5. Keep same general format and style but improve organization/completeness
</requirements>

<output_format>
# Revised Structure
[Provide complete revised outline addressing critique while maintaining coherence]

Include:
- Updated section/subsection structure
- Explicit key move mappings
- Revised word count allocations
- Brief descriptions of each section

# Changes Made
[List specific refinements implemented as bullet points]
</output_format>"""

        return prompt

    def get_literature_mapping_refinement_prompt(
        self,
        outline_development: str,
        critique: str,
        assessment: str,
        recommendations: List[str],
        framework: Dict[str, Any],
        developed_key_moves: Any,
        previous_versions: List[str] = None,
        iteration: int = 0,
    ) -> str:
        """
        Construct prompt for refining the literature mapping phase.
        
        This focuses on improving how literature is mapped to sections based on critique.
        """
        # Initialize previous_versions if None
        if previous_versions is None:
            previous_versions = []
            
        # Get the main thesis and contribution from the framework
        main_thesis = framework.get("main_thesis", "")
        core_contribution = framework.get("core_contribution", "")
        
        # Format recommendations into a list
        recommendations_list = "\n".join([f"- {rec}" for rec in recommendations])
        
        # Add a section about previous versions if they exist
        previous_versions_text = ""
        if previous_versions and len(previous_versions) > 1 and iteration > 0:
            previous_versions_text = f"""
## Previous Version History
This is iteration {iteration+1} of the outline development process. Please consider the following context:

- There are {len(previous_versions)} versions in the history
- This refinement should build on improvements already made
- Focus on addressing the specific recommendations from the critique
"""
        
        prompt = f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.4 (Detailed Outline Development).
You are refining the LITERATURE MAPPING phase based on critique.
Your task is to implement improvements while maintaining existing mapping approach.
The goal is comprehensive literature mapping with clear usage guidance.
</context>

<task>
Refine the literature mapping for a philosophical paper based on critique.
Implement improvements while maintaining existing mapping approach.
Create comprehensive mapping indicating which sources for each section.
Clarify how each source should be engaged.
</task>

<input_data>
CURRENT LITERATURE MAPPING:
```
{outline_development}
```

CRITIQUE:
```
{critique}
```

ASSESSMENT: {assessment}

RECOMMENDATIONS:
{recommendations_list}

MAIN THESIS:
{main_thesis}

CORE CONTRIBUTION:
{core_contribution}
{previous_versions_text}
</input_data>

<requirements>
1. Carefully implement critic's recommendations while preserving strengths
2. Ensure all key sections have appropriate literature identified
3. Clarify how each source should be engaged (supporting/contrasting/extending)
4. Prioritize sources for each section (primary vs supporting)
5. Maintain organization by section but improve quality/specificity of mappings
</requirements>

<output_format>
# Revised Literature Mapping
[Provide complete revised mapping addressing critique while maintaining coherence]

Include:
- Comprehensive literature mappings for all sections
- Clear guidance on how each source should be used
- Prioritization of sources
- Brief notes on why specific sources are relevant

# Changes Made
[List specific refinements implemented as bullet points]
</output_format>"""

        return prompt

    def get_content_development_refinement_prompt(
        self,
        outline_development: str,
        critique: str,
        framework: Dict[str, Any],
        developed_key_moves: List[Dict[str, Any]],
        previous_versions: List[str] = None,
    ) -> str:
        """
        Construct prompt for refining the content development phase based on critique.
        
        This focuses on improving the content guidance for each section.
        """
        # Initialize previous_versions if None
        if previous_versions is None:
            previous_versions = []
            
        # Get the main thesis and contribution from the framework
        main_thesis = framework.get("main_thesis", "")
        core_contribution = framework.get("core_contribution", "")
        
        # Add a section about previous versions if they exist
        previous_versions_text = ""
        if previous_versions and len(previous_versions) > 1:
            previous_versions_text = f"""
## Previous Version History
There are {len(previous_versions)} versions in the history. Use this information to avoid repeating problems that have already been addressed and build on improvements already made.
"""
        
        prompt = f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.4 (Detailed Outline Development).
You are refining the CONTENT DEVELOPMENT phase based on critique.
Your task is to create highly detailed, specific content guidance.
The goal is comprehensive direction for Phase III writers.
</context>

<task>
Refine the content guidance for a philosophical paper based on critique.
Implement critic's recommendations to create detailed, specific guidance.
Provide comprehensive direction that Phase III writers can follow directly.
Transform vague suggestions into concrete directives.
</task>

<input_data>
CURRENT CONTENT GUIDANCE:
```
{outline_development}
```

CRITIQUE TO ADDRESS:
```
{critique}
```

MAIN THESIS:
"{main_thesis}"

CORE CONTRIBUTION:
"{core_contribution}"
{previous_versions_text}
</input_data>

<requirements>
Implement critic's recommendations to substantially improve content guidance:

1. Make argument specifications more detailed:
   - Precise premises and conclusions for each argument
   - Clear logical structure and reasoning approaches
   - Explicit philosophical claims with supporting points
   - Specific explanations of how arguments advance thesis

2. Enhance concept definitions:
   - Explicitly identify key philosophical terms
   - Provide specific definitional guidance
   - Clarify technical terminology with explanations
   - Specify philosophical traditions or sources

3. Improve example integration:
   - Detailed descriptions of specific examples
   - Explicit guidance on presentation/development
   - Clear explanations of how examples support arguments
   - Step-by-step instructions for thought experiments

4. Strengthen literature connections:
   - Named references to specific scholars/sources
   - Explicit guidance on engaging each source
   - Clear identification of positions to support/critique
   - Specific quotes or ideas to highlight

5. Develop specific objection handling:
   - Articulate precise objections with logical structure
   - Provide detailed counter-arguments
   - Include step-by-step guidance on addressing objections
   - Identify strongest challenges and how to overcome

6. Increase overall specificity:
   - Convert vague suggestions into concrete directives
   - Provide actionable details for direct implementation
   - Include enough guidance to avoid significant content decisions
   - Use clear, directive language
</requirements>

<output_format>
# Refined Content Guidance

For each section, include structured categories:

- **Core Arguments**: Detailed descriptions with premises and conclusions
- **Key Concepts**: Important terms with suggested definitions
- **Example Development**: Specific examples with presentation guidance
- **Objections & Responses**: Specific counterarguments and responses
- **Philosophical Positions**: Named positions to address/defend/critique
- **Methodological Notes**: Approach for developing the section

Maintain original section structure but dramatically enhance content guidance.
Be extremely specific and detailed - provide comprehensive content blueprint.

# Implementation Approach
[Briefly describe how you addressed the critique's main recommendations]
</output_format>"""
        
        return prompt

    def get_structural_validation_refinement_prompt(
        self,
        outline_development: str,
        critique: str,
        assessment: str,
        recommendations: List[str],
        framework: Dict[str, Any],
        developed_key_moves: Any,
        previous_versions: List[str] = None,
        iteration: int = 0,
    ) -> str:
        """
        Construct prompt for refining the structural validation phase.
        
        This focuses on finalizing the complete outline based on critique.
        """
        # Initialize previous_versions if None
        if previous_versions is None:
            previous_versions = []
            
        # Get the main thesis and contribution from the framework
        main_thesis = framework.get("main_thesis", "")
        core_contribution = framework.get("core_contribution", "")
        
        # Format recommendations into a list
        recommendations_list = "\n".join([f"- {rec}" for rec in recommendations])
        
        # Add a section about previous versions if they exist
        previous_versions_text = ""
        if previous_versions and len(previous_versions) > 1 and iteration > 0:
            previous_versions_text = f"""
## Previous Version History
This is iteration {iteration+1} of the outline development process. Please consider the following context:

- There are {len(previous_versions)} versions in the history
- This refinement should build on improvements already made
- Focus on addressing the specific recommendations from the critique
"""
        
        prompt = f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.4 (Detailed Outline Development).
You are refining the STRUCTURAL VALIDATION phase based on critique.
Your task is to finalize the comprehensive outline.
The goal is a validated outline serving as blueprint for Phase II.5 and Phase III.
</context>

<task>
Finalize a comprehensive outline for a philosophical paper based on critique.
Implement improvements while maintaining overall structure and content guidance.
Create final validated outline as blueprint for subsequent phases.
Ensure coherence, completeness, and logical flow.
</task>

<input_data>
CURRENT VALIDATED OUTLINE:
```
{outline_development}
```

CRITIQUE:
```
{critique}
```

ASSESSMENT: {assessment}

RECOMMENDATIONS:
{recommendations_list}

MAIN THESIS:
{main_thesis}

CORE CONTRIBUTION:
{core_contribution}
{previous_versions_text}
</input_data>

<requirements>
1. Carefully implement critic's recommendations while preserving strengths
2. Ensure overall coherence of outline is maintained or enhanced
3. Verify all key moves properly developed and sequenced
4. Check word count allocations appropriate for section complexity
5. Confirm introduction/conclusion effectively frame paper
6. Maintain structured format while making necessary adjustments
</requirements>

<output_format>
# Final Validated Outline
[Provide complete revised outline addressing critique while maintaining coherence]

Include:
- Complete section/subsection structure with word counts
- Key move mappings
- Structured content guidance for each section
- Clear transitions between sections
- Any explanations needed for substantive changes

# Changes Made
[List specific refinements implemented as bullet points]
</output_format>"""

        return prompt

    # Keep the original methods for backwards compatibility
    def get_structure_refinement_prompt(
        self,
        outline_development: str,
        critique: str,
        assessment: str,
        recommendations: List[str],
        framework: Dict[str, Any],
        developed_key_moves: List[Dict[str, Any]],
        iteration: int = 0,
    ) -> str:
        """Legacy method - redirects to framework integration prompt"""
        return self.get_framework_integration_refinement_prompt(
            outline_development, critique, assessment, recommendations, framework, developed_key_moves, None, iteration
        )

    def get_content_refinement_prompt(
        self,
        outline_development: str,
        critique: str,
        assessment: str,
        recommendations: List[str],
        framework: Dict[str, Any],
        developed_key_moves: List[Dict[str, Any]],
        iteration: int = 0,
    ) -> str:
        """Legacy method - redirects to content development prompt"""
        return self.get_content_development_refinement_prompt(
            outline_development, critique, framework, developed_key_moves, None
        )

    def get_transitions_refinement_prompt(
        self,
        outline_development: str,
        critique: str,
        assessment: str,
        recommendations: List[str],
        framework: Dict[str, Any],
        developed_key_moves: List[Dict[str, Any]],
        iteration: int = 0,
    ) -> str:
        """Legacy method - redirects to structural validation prompt"""
        return self.get_structural_validation_refinement_prompt(
            outline_development, critique, assessment, recommendations, framework, developed_key_moves, None, iteration
        )

    def get_system_prompt(self) -> str:
        """Return the system prompt for API calls"""
        return self.system_prompt 