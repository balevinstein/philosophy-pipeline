from typing import Dict, Any, List, Optional


class OutlineCriticPrompts:
    """Prompts for critiquing detailed outline development in Phase II.4."""

    def get_critique_prompt(
        self,
        outline_development: str,
        framework: Dict[str, Any],
        developed_key_moves: List[Dict[str, Any]],
        development_phase: str = "framework_integration",
        previous_versions: List[str] = None,
        iteration: int = 0,
    ) -> str:
        """
        Get the appropriate critique prompt based on the development phase.
        """
        # Initialize previous_versions if None
        if previous_versions is None:
            previous_versions = []
            
        if development_phase == "framework_integration":
            return self.get_framework_integration_critique_prompt(
                outline_development, framework, developed_key_moves, previous_versions, iteration
            )
        elif development_phase == "literature_mapping":
            return self.get_literature_mapping_critique_prompt(
                outline_development, framework, developed_key_moves, previous_versions, iteration
            )
        elif development_phase == "content_development":
            return self.get_content_development_critique_prompt(
                outline_development, framework, developed_key_moves, previous_versions, iteration
            )
        elif development_phase == "structural_validation":
            return self.get_structural_validation_critique_prompt(
                outline_development, framework, developed_key_moves, previous_versions, iteration
            )
        else:
            # Default to framework integration if we don't recognize the phase
            return self.get_framework_integration_critique_prompt(
                outline_development, framework, developed_key_moves, previous_versions, iteration
            )

    def get_framework_integration_critique_prompt(
        self,
        outline_development: str,
        framework: Dict[str, Any],
        developed_key_moves: List[Dict[str, Any]],
        previous_versions: List[str] = None,
        iteration: int = 0,
    ) -> str:
        """
        Construct prompt for critiquing the framework integration phase.
        
        This focuses on evaluating the foundational structure created to accommodate all key moves.
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
        
        # Add a section about previous versions if they exist
        previous_versions_text = ""
        if previous_versions and len(previous_versions) > 1 and iteration > 0:
            previous_versions_text = f"""
## Previous Version History
This is iteration {iteration+1} of the outline development process. Please consider the following context:

- There are {len(previous_versions)} versions in the history
- This critique should focus on comparing the current version to the previous ones
- Identify improvements already made and areas still needing attention
"""
        
        prompt = f"""# Framework Integration Critique

## Task Description
You are a philosophical writing expert evaluating the foundational structure for a philosophical paper. Your task is to critique the structural framework to ensure it properly accommodates all key moves, provides appropriate word count allocations, and creates a logical progression from introduction through conclusion.
{previous_versions_text}
## Outline to Critique
```
{outline_development}
```

## Context
This outline should support a paper with the following thesis:
"{main_thesis}"

The core contribution should be:
"{core_contribution}"

The outline should incorporate these key argumentative moves:
{key_moves_list}

## Critique Focus Areas
Evaluate the structural framework based on these specific criteria:

1. **Key Move Accommodation**
   - Does the structure properly accommodate all key moves?
   - Is there explicit mapping of which sections develop which key moves?
   - Are the key moves positioned in a logical sequence?

2. **Structural Organization**
   - Is the outline properly organized with clear sections and subsections?
   - Does the numbering system make logical sense?
   - Is the hierarchical structure appropriate for a philosophical paper?

3. **Word Count Allocation**
   - Are word counts allocated appropriately across sections?
   - Is sufficient space allocated to the most important arguments?
   - Is the balance between introduction, main arguments, and conclusion appropriate?

4. **Logical Progression**
   - Does the structure create a logical progression of ideas?
   - Does the organization support the thesis and core contribution?
   - Will this structure lead to a coherent philosophical argument?

5. **Completeness**
   - Does the outline include all necessary sections (introduction, main arguments, objections, conclusion)?
   - Is anything important missing from the structure?
   - Is the foundational framework sufficiently detailed?

## Provide Detailed Feedback
For each focus area, provide specific observations, identifying both strengths and weaknesses. Be precise in your critique - point to specific sections or structural elements that need improvement.

## Summary Assessment
Conclude with an overall assessment of the structural framework and specific recommendations for improvement. Choose one of these assessment categories:

- MAJOR REVISION NEEDED: The structure needs significant reorganization
- MINOR REFINEMENT NEEDED: The structure is workable but needs important improvements
- GOOD: The structure is mostly effective with minor adjustments needed
- VERY GOOD: The structure is excellent with few improvements needed
- EXCELLENT: The structure is outstanding and ready for the next phase

Follow your assessment with specific, actionable recommendations for improvement.
"""

        return prompt

    def get_literature_mapping_critique_prompt(
        self,
        outline_development: str,
        framework: Dict[str, Any],
        developed_key_moves: List[Dict[str, Any]],
        previous_versions: List[str] = None,
        iteration: int = 0,
    ) -> str:
        """
        Construct prompt for critiquing the literature mapping phase.
        
        This focuses on evaluating how literature is mapped to sections and how sources should be engaged.
        """
        # Initialize previous_versions if None
        if previous_versions is None:
            previous_versions = []
            
        # Get the main thesis and contribution from the framework
        main_thesis = framework.get("main_thesis", "")
        core_contribution = framework.get("core_contribution", "")
        
        # Add a section about previous versions if they exist
        previous_versions_text = ""
        if previous_versions and len(previous_versions) > 1 and iteration > 0:
            previous_versions_text = f"""
## Previous Version History
This is iteration {iteration+1} of the outline development process. Please consider the following context:

- There are {len(previous_versions)} versions in the history
- This critique should focus on comparing the current version to the previous ones
- Identify improvements already made and areas still needing attention
"""
        
        prompt = f"""# Literature Mapping Critique

## Task Description
You are a philosophical writing expert evaluating the literature mapping for a philosophical paper. Your task is to critique how literature has been mapped to different sections and how each source should be engaged.
{previous_versions_text}
## Literature Mapping to Critique
```
{outline_development}
```

## Context
This mapping should support a paper with the following thesis:
"{main_thesis}"

The core contribution should be:
"{core_contribution}"

## Critique Focus Areas
Evaluate the literature mapping based on these specific criteria:

1. **Comprehensiveness**
   - Has literature been identified for all key sections of the outline?
   - Is there a sufficient range of sources to support the philosophical arguments?
   - Are there any sections that lack necessary literature support?

2. **Relevance**
   - Is the identified literature relevant to the sections it's mapped to?
   - Does the literature directly support the arguments being made?
   - Are the connections between literature and arguments clearly explained?

3. **Engagement Guidance**
   - Is there clear specification of how each source should be engaged?
   - Is there guidance on which sources are supporting vs. contrasting?
   - Is there prioritization of primary vs. supporting sources?

4. **Scholarly Integration**
   - Does the mapping create opportunities for meaningful scholarly dialogue?
   - Is there a balance between using literature as support and critically engaging with it?
   - Does the literature mapping help position the paper within its field?

5. **Practical Usability**
   - Would Phase III writers find this mapping clear and practical to follow?
   - Is the organization logical and easy to navigate?
   - Is there sufficient detail about how to use each source?

## Provide Detailed Feedback
For each focus area, provide specific observations, identifying both strengths and weaknesses. Be precise in your critique - point to specific mapping elements that need improvement.

## Summary Assessment
Conclude with an overall assessment of the literature mapping and specific recommendations for improvement. Choose one of these assessment categories:

- MAJOR REVISION NEEDED: The literature mapping needs significant reorganization or expansion
- MINOR REFINEMENT NEEDED: The mapping is workable but needs important improvements
- GOOD: The mapping is mostly effective with minor adjustments needed
- VERY GOOD: The mapping is excellent with few improvements needed
- EXCELLENT: The literature mapping is outstanding and ready for the next phase

Follow your assessment with specific, actionable recommendations for improvement.
"""

        return prompt

    def get_content_development_critique_prompt(
        self,
        outline_development: str,
        framework: Dict[str, Any],
        developed_key_moves: List[Dict[str, Any]],
        previous_versions: List[str] = None,
        iteration: int = 0,
    ) -> str:
        """
        Construct prompt for critiquing the content development phase.
        
        This focuses on evaluating the specific content guidance for each section.
        """
        # Initialize previous_versions if None
        if previous_versions is None:
            previous_versions = []
            
        # Get the main thesis and contribution from the framework
        main_thesis = framework.get("main_thesis", "")
        core_contribution = framework.get("core_contribution", "")
        
        # Add a section about previous versions if they exist
        previous_versions_text = ""
        if previous_versions and len(previous_versions) > 1 and iteration > 0:
            previous_versions_text = f"""
## Previous Version History
This is iteration {iteration+1} of the outline development process. Please consider the following context:

- There are {len(previous_versions)} versions in the history
- This critique should focus on comparing the current version to the previous ones
- Identify improvements already made and areas still needing attention
"""
        
        prompt = f"""# Content Development Critique

## Task Description
You are a philosophical writing expert evaluating the content guidance for a philosophical paper. Your task is to critique the detailed content guidance provided for each section to ensure it gives Phase III writers complete and specific direction for writing.
{previous_versions_text}
## Content Guidance to Critique
```
{outline_development}
```

## Context
This content guidance should support a paper with the following thesis:
"{main_thesis}"

The core contribution should be:
"{core_contribution}"

## Critique Focus Areas
Evaluate the content guidance based on these specific criteria:

1. **Argument Specification**
   - Are the primary arguments for each section specified with clear premises and conclusions?
   - Is there sufficient detail about the logical structure of each argument?
   - Would a Phase III writer understand exactly which points to make and how to develop them?
   - Are the philosophical claims precise and well-articulated?
   - Is the reasoning approach clearly specified?

2. **Concept Definition**
   - Are key philosophical concepts explicitly identified?
   - Is guidance provided on how to define and explain these concepts?
   - Are technical terms clearly flagged with definitional guidance?
   - Is the philosophical terminology appropriate and precise?

3. **Example Integration**
   - Are specific examples clearly described with implementation details?
   - Is there context for how examples should be presented and developed?
   - Is it clear how examples support specific premises or conclusions?
   - Is sufficient detail provided about how to construct each example?

4. **Literature Connection**
   - Are specific literature sources identified by name?
   - Is there clear guidance on how to engage with each source?
   - Is the engagement approach specified (support, critique, extend, etc.)?
   - Are key scholarly positions named and addressed?

5. **Objection Handling**
   - Are specific objections clearly articulated with their logical structure?
   - Are detailed responses provided with clear counter-arguments?
   - Is guidance given on how to present and address each objection?
   - Are the strongest possible objections considered?

6. **Content Specificity**
   - Is the guidance concrete and specific rather than vague or general?
   - Are there actionable details that a writer could implement directly?
   - Is enough detail provided that a Phase III writer wouldn't need to make significant content decisions?
   - Are there clear directives rather than open-ended suggestions?

7. **Structure and Organization**
   - Is the content properly organized with clear categories?
   - Are the relationships between sections and subsections clear?
   - Are transitions between ideas explicitly addressed?
   - Is there a logical flow to the content guidance?

## Provide Detailed Feedback
For each focus area, provide specific observations, identifying both strengths and weaknesses. Be precise in your critique - point to specific content elements that need improvement, and suggest how they could be enhanced.

## Summary Assessment
Conclude with an overall assessment of the content guidance and specific recommendations for improvement. Choose one of these assessment categories:

- MAJOR REVISION NEEDED: The content guidance needs significant expansion or increased specificity
- MINOR REFINEMENT NEEDED: The guidance is workable but needs important details added
- GOOD: The guidance is mostly effective with minor additions needed
- VERY GOOD: The guidance is excellent with few improvements needed
- EXCELLENT: The content guidance is outstanding and ready for Phase III writers

Follow your assessment with specific, actionable recommendations for improvement, focusing on how to make the content guidance more specific, comprehensive, and directly implementable by Phase III writers.
"""
        return prompt

    def get_structural_validation_critique_prompt(
        self,
        outline_development: str,
        framework: Dict[str, Any],
        developed_key_moves: List[Dict[str, Any]],
        previous_versions: List[str] = None,
        iteration: int = 0,
    ) -> str:
        """
        Construct prompt for critiquing the structural validation phase.
        
        This focuses on evaluating the final validated outline for coherence, completeness, and logical flow.
        """
        # Initialize previous_versions if None
        if previous_versions is None:
            previous_versions = []
            
        # Get the main thesis and contribution from the framework
        main_thesis = framework.get("main_thesis", "")
        core_contribution = framework.get("core_contribution", "")
        
        prompt = f"""# Structural Validation Critique

## Task Description
You are a philosophical writing expert evaluating the final validated outline for a philosophical paper. Your task is to critique the complete outline to ensure it effectively delivers the paper's thesis through a coherent, well-structured argument.

## Validated Outline to Critique
```
{outline_development}
```

## Context
This outline should support a paper with the following thesis:
"{main_thesis}"

The core contribution should be:
"{core_contribution}"

## Critique Focus Areas
Evaluate the validated outline based on these specific criteria:

1. **Overall Coherence**
   - Does the outline create a unified, coherent philosophical argument?
   - Do all sections work together to support the main thesis?
   - Is there a clear logical progression from beginning to end?

2. **Key Move Development**
   - Are all key moves properly developed and positioned?
   - Is there appropriate balance in how key moves are presented?
   - Do the key moves build on each other effectively?

3. **Word Count Validation**
   - Are the word count allocations appropriate for the complexity of each section?
   - Is there sufficient space for all necessary arguments?
   - Is the overall length appropriate for the intended publication?

4. **Introduction and Conclusion**
   - Does the introduction effectively set up the paper's argument?
   - Does the conclusion properly synthesize the paper's contribution?
   - Do they work together to frame the paper effectively?

5. **Final Structure Completeness**
   - Is the outline structure complete with all necessary elements?
   - Is the level of detail appropriate for Phase III writers?
   - Would this outline serve as a comprehensive blueprint for writing?

## Provide Detailed Feedback
For each focus area, provide specific observations, identifying both strengths and weaknesses. Be precise in your critique - point to specific elements of the validated outline that need improvement.

## Summary Assessment
Conclude with an overall assessment of the validated outline and specific recommendations for improvement. Choose one of these assessment categories:

- MAJOR REVISION NEEDED: The validated outline needs significant restructuring
- MINOR REFINEMENT NEEDED: The outline is workable but needs important improvements
- GOOD: The outline is mostly effective with minor adjustments needed
- VERY GOOD: The outline is excellent with few improvements needed
- EXCELLENT: The validated outline is outstanding and ready for the next phase

Follow your assessment with specific, actionable recommendations for improvement.
"""

        return prompt

    # Keep the original methods for backwards compatibility
    def get_structure_critique_prompt(
        self,
        outline_development: str,
        framework: Dict[str, Any],
        initial_outline: Dict[str, Any],
        developed_key_moves: List[Dict[str, Any]],
        iteration: int = 0,
    ) -> str:
        """Legacy method - redirects to framework integration prompt"""
        return self.get_framework_integration_critique_prompt(
            outline_development, framework, developed_key_moves, iteration
        )

    def get_content_critique_prompt(
        self,
        outline_development: str,
        framework: Dict[str, Any],
        initial_outline: Dict[str, Any],
        developed_key_moves: List[Dict[str, Any]],
        iteration: int = 0,
    ) -> str:
        """Legacy method - redirects to content development prompt"""
        return self.get_content_development_critique_prompt(
            outline_development, framework, developed_key_moves, iteration
        )

    def get_transitions_critique_prompt(
        self,
        outline_development: str,
        framework: Dict[str, Any],
        initial_outline: Dict[str, Any],
        developed_key_moves: List[Dict[str, Any]],
        iteration: int = 0,
    ) -> str:
        """Legacy method - redirects to structural validation prompt"""
        return self.get_structural_validation_critique_prompt(
            outline_development, framework, developed_key_moves, iteration
        ) 