from typing import Dict, Any, List, Optional


class OutlineCriticPrompts:
    """Prompts for critiquing detailed outline development in Phase II.4."""

    def __init__(self):
        self.system_prompt = """You are a rigorous philosophy journal reviewer evaluating paper outlines. Your role is to ensure outlines provide comprehensive blueprints for paper development. Be constructive but skeptical. Your critiques will guide refinement in an automated system."""

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
        
        prompt = f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.4 (Detailed Outline Development).
You are critiquing the FRAMEWORK INTEGRATION phase, evaluating the foundational structure.
Your critique will guide refinement to ensure proper accommodation of all key moves.
The goal is an outline that serves as a comprehensive blueprint for Phase III writing.
</context>

<task>
Critique the structural framework to ensure it properly accommodates all key moves.
Evaluate word count allocations and logical progression.
Assess whether the structure will support the paper's thesis and core contribution.
Be rigorous but constructive in identifying weaknesses.
</task>

<input_data>
OUTLINE TO CRITIQUE:
```
{outline_development}
```

MAIN THESIS:
"{main_thesis}"

CORE CONTRIBUTION:
"{core_contribution}"

KEY ARGUMENTATIVE MOVES:
{key_moves_list}
{previous_versions_text}
</input_data>

<requirements>
Evaluate the structural framework based on these specific criteria:

1. **Key Move Accommodation**
   - Does structure properly accommodate all key moves?
   - Is there explicit mapping of sections to key moves?
   - Are key moves positioned in logical sequence?

2. **Structural Organization**
   - Is outline organized with clear sections/subsections?
   - Does numbering system make logical sense?
   - Is hierarchical structure appropriate for philosophy paper?

3. **Word Count Allocation**
   - Are word counts allocated appropriately across sections?
   - Is sufficient space allocated to most important arguments?
   - Is balance between intro, main arguments, conclusion appropriate?

4. **Logical Progression**
   - Does structure create logical progression of ideas?
   - Does organization support thesis and core contribution?
   - Will structure lead to coherent philosophical argument?

5. **Completeness**
   - Does outline include all necessary sections?
   - Is anything important missing from structure?
   - Is foundational framework sufficiently detailed?
</requirements>

<output_format>
# Detailed Feedback
[For each criterion above, provide specific observations identifying strengths and weaknesses. Point to specific sections needing improvement.]

# Summary Assessment
[Choose one category:]
- MAJOR REVISION NEEDED: Structure needs significant reorganization
- MINOR REFINEMENT NEEDED: Structure workable but needs important improvements
- GOOD: Structure mostly effective with minor adjustments needed
- VERY GOOD: Structure excellent with few improvements needed
- EXCELLENT: Structure outstanding and ready for next phase

# Recommendations
[Provide 3-5 specific, actionable recommendations for improvement]
</output_format>"""

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
        
        prompt = f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.4 (Detailed Outline Development).
You are critiquing the LITERATURE MAPPING phase, evaluating literature integration.
Your critique will ensure proper scholarly engagement and positioning of arguments.
The goal is clear guidance on how each source should be used in Phase III writing.
</context>

<task>
Critique how literature has been mapped to different sections.
Evaluate whether sources are relevant and properly positioned.
Assess the guidance on how each source should be engaged.
Be rigorous in identifying gaps or misalignments.
</task>

<input_data>
LITERATURE MAPPING TO CRITIQUE:
```
{outline_development}
```

MAIN THESIS:
"{main_thesis}"

CORE CONTRIBUTION:
"{core_contribution}"
{previous_versions_text}
</input_data>

<requirements>
Evaluate the literature mapping based on these specific criteria:

1. **Comprehensiveness**
   - Has literature been identified for all key sections?
   - Is there sufficient range of sources for philosophical arguments?
   - Are there sections lacking necessary literature support?

2. **Relevance**
   - Is identified literature relevant to its mapped sections?
   - Does literature directly support arguments being made?
   - Are connections between literature and arguments clear?

3. **Engagement Guidance**
   - Is there clear specification of how to engage each source?
   - Is guidance on supporting vs. contrasting sources clear?
   - Is there prioritization of primary vs. supporting sources?

4. **Scholarly Integration**
   - Does mapping create opportunities for scholarly dialogue?
   - Is there balance between using literature as support and critical engagement?
   - Does mapping help position paper within its field?

5. **Practical Usability**
   - Would Phase III writers find mapping clear and practical?
   - Is organization logical and easy to navigate?
   - Is there sufficient detail about how to use each source?
</requirements>

<output_format>
# Detailed Feedback
[For each criterion above, provide specific observations identifying strengths and weaknesses. Point to specific mapping elements needing improvement.]

# Summary Assessment
[Choose one category:]
- MAJOR REVISION NEEDED: Literature mapping needs significant reorganization/expansion
- MINOR REFINEMENT NEEDED: Mapping workable but needs important improvements
- GOOD: Mapping mostly effective with minor adjustments needed
- VERY GOOD: Mapping excellent with few improvements needed
- EXCELLENT: Literature mapping outstanding and ready for next phase

# Recommendations
[Provide 3-5 specific, actionable recommendations for improvement]
</output_format>"""

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
        
        prompt = f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.4 (Detailed Outline Development).
You are critiquing the CONTENT DEVELOPMENT phase, evaluating detailed content guidance.
Your critique will ensure Phase III writers have complete, specific direction for writing.
The goal is guidance so detailed that writers need not make significant content decisions.
</context>

<task>
Critique the detailed content guidance provided for each section.
Evaluate whether arguments are specified with clear premises and conclusions.
Assess whether examples, objections, and responses are sufficiently detailed.
Be rigorous in identifying vague or incomplete guidance.
</task>

<input_data>
CONTENT GUIDANCE TO CRITIQUE:
```
{outline_development}
```

MAIN THESIS:
"{main_thesis}"

CORE CONTRIBUTION:
"{core_contribution}"
{previous_versions_text}
</input_data>

<requirements>
Evaluate the content guidance based on these specific criteria:

1. **Argument Specification**
   - Are primary arguments specified with clear premises/conclusions?
   - Is there sufficient detail about logical structure?
   - Would Phase III writer understand exactly which points to make?
   - Are philosophical claims precise and well-articulated?
   - Is reasoning approach clearly specified?

2. **Concept Definition**
   - Are key philosophical concepts explicitly identified?
   - Is guidance provided on how to define/explain concepts?
   - Are technical terms flagged with definitional guidance?
   - Is philosophical terminology appropriate and precise?

3. **Example Integration**
   - Are specific examples clearly described with implementation details?
   - Is there context for how examples should be presented?
   - Is it clear how examples support specific premises/conclusions?
   - Is sufficient detail provided about constructing each example?

4. **Literature Connection**
   - Are specific literature sources identified by name?
   - Is there clear guidance on engaging each source?
   - Is engagement approach specified (support/critique/extend)?
   - Are key scholarly positions named and addressed?

5. **Objection Handling**
   - Are specific objections articulated with logical structure?
   - Are detailed responses provided with clear counter-arguments?
   - Is guidance given on presenting/addressing each objection?
   - Are strongest possible objections considered?

6. **Content Specificity**
   - Is guidance concrete and specific vs. vague/general?
   - Are there actionable details writers could implement directly?
   - Is enough detail provided to avoid significant content decisions?
   - Are there clear directives rather than open-ended suggestions?

7. **Structure and Organization**
   - Is content organized with clear categories?
   - Are relationships between sections/subsections clear?
   - Are transitions between ideas explicitly addressed?
   - Is there logical flow to content guidance?
</requirements>

<output_format>
# Detailed Feedback
[For each criterion above, provide specific observations identifying strengths and weaknesses. Point to specific content elements needing improvement and suggest enhancements.]

# Summary Assessment
[Choose one category:]
- MAJOR REVISION NEEDED: Content guidance needs significant expansion/increased specificity
- MINOR REFINEMENT NEEDED: Guidance workable but needs important details added
- GOOD: Guidance mostly effective with minor additions needed
- VERY GOOD: Guidance excellent with few improvements needed
- EXCELLENT: Content guidance outstanding and ready for Phase III writers

# Recommendations
[Provide 3-5 specific, actionable recommendations focusing on making guidance more specific, comprehensive, and directly implementable]
</output_format>"""

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
        
        prompt = f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.4 (Detailed Outline Development).
You are critiquing the STRUCTURAL VALIDATION phase, evaluating the final comprehensive outline.
Your critique will ensure the outline effectively delivers the paper's thesis through coherent structure.
The goal is a validated outline ready to serve as a complete blueprint for Phase III.
</context>

<task>
Critique the complete outline to ensure it creates a unified philosophical argument.
Evaluate whether all sections work together to support the main thesis.
Assess the balance, progression, and completeness of the final structure.
Be rigorous in identifying any remaining weaknesses.
</task>

<input_data>
VALIDATED OUTLINE TO CRITIQUE:
```
{outline_development}
```

MAIN THESIS:
"{main_thesis}"

CORE CONTRIBUTION:
"{core_contribution}"
</input_data>

<requirements>
Evaluate the validated outline based on these specific criteria:

1. **Overall Coherence**
   - Does outline create unified, coherent philosophical argument?
   - Do all sections work together to support main thesis?
   - Is there clear logical progression from beginning to end?

2. **Key Move Development**
   - Are all key moves properly developed and positioned?
   - Is there appropriate balance in how key moves are presented?
   - Do key moves build on each other effectively?

3. **Word Count Validation**
   - Are word count allocations appropriate for complexity of each section?
   - Is there sufficient space for all necessary arguments?
   - Is overall length appropriate for intended publication?

4. **Introduction and Conclusion**
   - Does introduction effectively set up paper's argument?
   - Does conclusion properly synthesize paper's contribution?
   - Do they work together to frame paper effectively?

5. **Final Structure Completeness**
   - Is outline structure complete with all necessary elements?
   - Is level of detail appropriate for Phase III writers?
   - Would this outline serve as comprehensive blueprint for writing?
</requirements>

<output_format>
# Detailed Feedback
[For each criterion above, provide specific observations identifying strengths and weaknesses. Point to specific elements needing improvement.]

# Summary Assessment
[Choose one category:]
- MAJOR REVISION NEEDED: Validated outline needs significant restructuring
- MINOR REFINEMENT NEEDED: Outline workable but needs important improvements
- GOOD: Outline mostly effective with minor adjustments needed
- VERY GOOD: Outline excellent with few improvements needed
- EXCELLENT: Validated outline outstanding and ready for next phase

# Recommendations
[Provide 3-5 specific, actionable recommendations for improvement]
</output_format>"""

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

    def get_system_prompt(self) -> str:
        """Return the system prompt for API calls"""
        return self.system_prompt 