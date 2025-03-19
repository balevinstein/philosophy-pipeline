from typing import Dict, Any, List, Optional
import json


class OutlineRefinementPrompts:
    """Prompts for refining detailed outline development in Phase II.4."""

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
        
        prompt = f"""# Framework Integration Refinement

## Task Description
You are a philosophical writing expert refining the foundational structure for a philosophical paper. Your task is to implement improvements based on a critique while maintaining the existing framework. The goal is to create a structure that properly accommodates all key moves, provides appropriate word count allocations, and creates a logical progression.
{previous_versions_text}
## Current Structure
```
{outline_development}
```

## Critique
```
{critique}
```

## Assessment: {assessment}

## Recommendations
{recommendations_list}

## Paper Framework Information

### Main Thesis:
{main_thesis}

### Core Contribution:
{core_contribution}

### Key Moves:
{key_moves_list}

## Refinement Instructions
1. Carefully implement the critic's recommendations while preserving the strengths of the current structure
2. Ensure that all key moves are properly accommodated with explicit mapping
3. Maintain appropriate word count allocations
4. Preserve or enhance the logical flow from introduction through conclusion
5. Keep the same general format and style, but improve the structure's organization and completeness

## Expected Output
Provide a revised structure that addresses the critique while maintaining coherence. Your output should be a complete revised version, not just the changes. Include:
- Updated section/subsection structure
- Explicit key move mappings
- Revised word count allocations
- Brief descriptions of each section

## Change Documentation
At the end of your response, include a "Changes Made" section that lists the specific refinements you implemented, each as a bullet point.

Now, revise the structure to address the critique while maintaining a strong foundation for the philosophical paper.
"""

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
        
        prompt = f"""# Literature Mapping Refinement

## Task Description
You are a philosophical writing expert refining the literature mapping for a philosophical paper. Your task is to implement improvements based on a critique while maintaining the existing mapping approach. The goal is to create a comprehensive literature mapping that clearly indicates which sources should be used in each section and how.
{previous_versions_text}
## Current Literature Mapping
```
{outline_development}
```

## Critique
```
{critique}
```

## Assessment: {assessment}

## Recommendations
{recommendations_list}

## Paper Framework Information

### Main Thesis:
{main_thesis}

### Core Contribution:
{core_contribution}

## Refinement Instructions
1. Carefully implement the critic's recommendations while preserving the strengths of the current mapping
2. Ensure all key sections have appropriate literature identified
3. Clarify how each source should be engaged (supporting, contrasting, extending)
4. Prioritize sources for each section (primary vs supporting)
5. Maintain the organization by section but improve the quality and specificity of mappings

## Expected Output
Provide a revised literature mapping that addresses the critique while maintaining coherence. Your output should be a complete revised version, not just the changes. Include:
- Comprehensive literature mappings for all sections
- Clear guidance on how each source should be used
- Prioritization of sources
- Brief notes on why specific sources are relevant to specific sections

## Change Documentation
At the end of your response, include a "Changes Made" section that lists the specific refinements you implemented, each as a bullet point.

Now, revise the literature mapping to address the critique while maintaining a clear organization by section.
"""

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
        
        prompt = f"""# Content Development Refinement

## Task Description
You are a philosophical writing expert refining the content guidance for a philosophical paper. Your task is to implement the critic's recommendations to create highly detailed, specific content guidance that provides Phase III writers with comprehensive direction for each section.
{previous_versions_text}
## Current Content Guidance
```
{outline_development}
```

## Critique to Address
```
{critique}
```

## Context
This content guidance should support a paper with the following thesis:
"{main_thesis}"

The core contribution should be:
"{core_contribution}"

## Refinement Instructions
Implement the critic's recommendations to create substantially improved content guidance. Your refinements should:

1. Make argument specifications much more detailed with:
   - Precise premises and conclusions for each argument
   - Clear logical structure and reasoning approaches
   - Explicit philosophical claims with supporting points
   - Specific explanations of how arguments advance the main thesis

2. Enhance concept definitions by:
   - Explicitly identifying key philosophical terms
   - Providing specific definitional guidance for each term
   - Clarifying technical terminology with suggested explanations
   - Specifying philosophical traditions or sources for definitions

3. Improve example integration with:
   - Detailed descriptions of specific examples to use
   - Explicit guidance on how to present and develop examples
   - Clear explanations of how examples support specific arguments
   - Step-by-step instructions for constructing thought experiments

4. Strengthen literature connections through:
   - Named references to specific scholars and sources
   - Explicit guidance on how to engage with each source
   - Clear identification of positions to support or critique
   - Specific quotes or ideas to highlight from key sources

5. Develop more specific objection handling by:
   - Articulating precise objections with their logical structure
   - Providing detailed counter-arguments and responses
   - Including step-by-step guidance on addressing objections
   - Identifying the strongest challenges and how to overcome them

6. Increase overall specificity by:
   - Converting vague suggestions into concrete directives
   - Providing actionable details that a writer could implement directly
   - Including enough guidance that Phase III writers need not make significant content decisions
   - Using clear, directive language rather than open-ended suggestions

## Output Format
Present your refined content guidance in a structured format using Markdown. For each section, include:

- **Core Arguments**: Detailed descriptions of specific arguments with premises and conclusions
- **Key Concepts**: Important terms to define with suggested definitions
- **Example Development**: Specific examples/analogies with guidance on presentation
- **Objections & Responses**: Specific counterarguments and detailed responses
- **Philosophical Positions**: Named positions to address, defend, or critique
- **Methodological Notes**: Approach to use in developing the section

Maintain the original section structure but dramatically enhance the content guidance for each section and subsection. Be extremely specific and detailed in your guidance - your goal is to provide a comprehensive content blueprint that Phase III writers can follow directly.

## Implementation Approach
First identify the critic's most significant recommendations, then systematically enhance each section's content guidance to address these issues while maintaining the original structure. Focus particularly on adding specificity and actionable details where the critic noted deficiencies.
"""
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
        
        prompt = f"""# Structural Validation Refinement

## Task Description
You are a philosophical writing expert finalizing a comprehensive outline for a philosophical paper. Your task is to implement improvements based on a critique while maintaining the overall structure and content guidance. The goal is to create a final validated outline that will serve as the blueprint for Phase II.5 and ultimately Phase III writing.
{previous_versions_text}
## Current Validated Outline
```
{outline_development}
```

## Critique
```
{critique}
```

## Assessment: {assessment}

## Recommendations
{recommendations_list}

## Paper Framework Information

### Main Thesis:
{main_thesis}

### Core Contribution:
{core_contribution}

## Refinement Instructions
1. Carefully implement the critic's recommendations while preserving the strengths of the current outline
2. Ensure that the overall coherence of the outline is maintained or enhanced
3. Verify that all key moves are properly developed and sequenced
4. Check that word count allocations are appropriate for each section's complexity
5. Confirm that the introduction and conclusion effectively frame the paper
6. Maintain the structured format while making necessary adjustments

## Expected Output
Provide a final validated outline that addresses the critique while maintaining coherence. Your output should be a complete revised version, not just the changes. Include:
- Complete section/subsection structure with word counts
- Key move mappings
- Structured content guidance for each section
- Clear transitions between sections
- Any explanations needed for substantive changes

## Change Documentation
At the end of your response, include a "Changes Made" section that lists the specific refinements you implemented, each as a bullet point.

Now, finalize the outline to address the critique while ensuring it provides a comprehensive blueprint for the philosophical paper.
"""

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