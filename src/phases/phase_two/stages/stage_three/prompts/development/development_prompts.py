from typing import Dict, Any, Optional, List


class MoveDevelopmentPrompts:
    """Prompts for key move development in Phase II.3."""

    def get_initial_development_prompt(
        self,
        move: str,
        framework: Dict[str, Any],
        outline: Dict[str, Any],
        literature: Dict[str, Any],
        move_index: int,
    ) -> str:
        """
        Construct prompt for initial development of a key move.
        
        This focuses on developing the core argument structure.
        """
        # Get the main thesis and contribution from the framework
        main_thesis = framework.get("main_thesis", "")
        core_contribution = framework.get("core_contribution", "")
        
        # Get the outline sections that might be relevant
        outline_sections = outline.get("outline", "")
        
        # Get literature synthesis
        lit_synthesis = literature.get("synthesis", {})
        lit_narrative = literature.get("narrative", "")
        
        prompt = f"""# Key Move Development: Initial Argument Structure

## Phase II.3 Context
You are participating in Phase II.3 (Key Moves Development) of a multi-phase philosophy paper generation process.

- Phase I identified the paper topic and gathered literature
- Phase II.1 processed and analyzed the literature
- Phase II.2 created the paper framework (abstract, thesis, outline)
- We are now in Phase II.3, developing key argumentative moves
- After this, Phase II.4 will create a detailed outline integrating these key moves
- Phase II.5 may perform final integration and smoothing if needed
- Only then will Phase III focus on prose crafting

Your task is to develop the intellectual content of this key move to completion. You must produce FINAL CONTENT that can be directly inserted into the paper. All intellectual decisions should be made now. The models in Phase III will focus only on prose refinement and will not create new arguments, examples, or structure.

## Task Description
You are developing a philosophical key move in detail. Each key move is a critical argumentative step in a philosophical paper. Your task is to write the actual content for this move as it would appear in the final paper, not just analyze it.

## Input
The key move you need to develop is:

"{move}"

This move is part of a philosophical paper with the following main thesis:
"{main_thesis}"

The core contribution of the paper is:
"{core_contribution}"

## Context
This is move #{move_index + 1} in the paper's key argumentative structure.

The paper's outline is:
```
{outline_sections}
```

## Important Constraints
- This paper targets Analysis journal's 4,000-word limit. Each key move should be approximately 500-600 words maximum.
- Be selective and concise in your development. Remove redundant examples, unnecessary literature citations, or peripheral discussions.

## Requirements
Write the actual content for this key move AS IT WOULD APPEAR IN THE FINAL PAPER. This means:

1. Write in scholarly philosophical prose, not in meta-commentary about the move. It should be written in the style seen in top journals in Analytic Philosophy, such as Analysis. 
2. Develop a complete, well-structured philosophical argument
3. Include necessary background, premises, and conclusions
4. Connect this move to the paper's overall thesis
5. Make all intellectual decisions now - don't defer any for "later phases"
6. Be bold, interesting, and creative. These moves play a central role in a paper that will be submitted for publication to a top philosophy journal.

## Strategic Decisions
Not every move requires the same elements. Determine what this specific move needs:

1. Does this move require concrete examples?
   - Use examples if the move is conceptually complex or counter-intuitive
   - Omit examples if the theoretical argument is clear without them
   
2. Does this move require literature engagement?
   - Cite only the most directly relevant works that provide essential context, represent positions you're directly responding to, or offer crucial support
   - Avoid literature "survey" approaches that list multiple authors making similar points
   - Ensure your engagement clearly highlights how your argument extends beyond, challenges, or synthesizes existing views

3. What development approach best serves this move?
   - Pure conceptual analysis
   - Case-based reasoning
   - Methodological argument
   - Novel theoretical contribution
   
Choose the approach that best serves this specific argument. Not all moves require all elements.

## Output Format
Write your content in clear, crisp, and engaging scholarly philosophical prose. Do NOT use meta-commentary like "This move accomplishes..." or "This section demonstrates..." Instead, write the actual content directly:

IMPORTANT:
- DO NOT write "Move Analysis", "Argument Structure", or similar analytical headings
- DO NOT use bullet points or outline format
- DO NOT include phrases like "This move would..." or "This section will..."
- DO NOT merely parrot other philosophers' arguments. Make the argument your own. Be ORIGINAL AND CREATIVE. 
- DO write in complete paragraphs as they would appear in the final paper
- DO develop all arguments fully with proper premises and conclusions
- DO write in a scholarly philosophical style appropriate for publication
- DO be concise and focused - remember the 500-600 word target for this move

## Guidelines
- Focus on philosophical depth and rigorous argument development
- Ensure logical coherence and theoretical soundness
- Keep the move realistic in scope while maintaining philosophical significance
- Consider both strengths and potential objections to the move if applicable 
- Prioritize philosophical precision and conciseness
- Remember: write the ACTUAL CONTENT, not commentary about it
"""

        return prompt

    def get_examples_development_prompt(
        self,
        move: str,
        current_development: Any,
        framework: Dict[str, Any],
        outline: Dict[str, Any],
        literature: Dict[str, Any],
    ) -> str:
        """
        Construct prompt for developing examples for a key move.
        
        This focuses on creating effective examples and illustrations to support the argument.
        """
        # Extract the current development content, handling various inputs
        if current_development is None:
            # If no current development provided, extract info from framework
            main_thesis = framework.get("main_thesis", "")
            moves_list = framework.get("key_moves", [])
            move_index = moves_list.index(move) if move in moves_list else -1
            
            current_content = f"""
# Key Move Context
This key move is: "{move}"

It supports the main thesis: "{main_thesis}"

Please develop examples that illustrate and support this move.
"""
        elif isinstance(current_development, dict):
            current_content = current_development.get("content", "")
        else:
            current_content = str(current_development)
        
        prompt = f"""# Key Move Development: Examples and Illustrations

## Phase II.3 Context
You are participating in Phase II.3 (Key Moves Development) of a multi-phase philosophy paper generation process.

Your task is to develop examples for this key move that are ready for direct inclusion in the final paper. These examples must be fully developed and written in the style they would appear in the published paper. Later phases will focus only on prose refinement and will not create new examples or arguments.

## Current Development
Here is the current development of the key move:

```
{current_content}
```

## Important Constraints
- This paper targets Analysis journal's 4,000-word limit. Be extremely selective with examples.
- Each example should be concise yet effective - focus on quality over quantity.
- Only include examples if they genuinely clarify or strengthen the philosophical argument.

## Requirements
Develop examples for this key move AS THEY WOULD APPEAR IN THE FINAL PAPER. This means:

1. Write fully developed examples in scholarly philosophical prose
2. Present examples as they would appear in the published paper, not as notes or outlines
3. Integrate examples naturally within the philosophical argument
4. Include complete details and necessary context
5. Make all intellectual decisions now - don't defer any for "later phases"

## Strategic Considerations
Determine whether this move truly needs examples:
- If the move is already clear and persuasive without examples, state that no additional examples are necessary
- If examples would strengthen the argument, develop only the most essential ones
- Focus on quality over quantity - one perfect example is better than several mediocre ones

## Output Format
Write your examples in clear, concise scholarly philosophical prose as they would appear in the final paper. Do NOT use meta-commentary like "This example demonstrates..." Instead, write the actual examples directly:

IMPORTANT:
- DO NOT use phrases like "This example would..." or "This case could..."
- DO NOT write in bullet points or outline format
- DO NOT leave placeholder text or references to "future development"
- DO write examples as complete, detailed, and ready for publication
- DO integrate the examples naturally into the philosophical argument
- DO include all necessary context and details for each example
- DO be concise - every word must earn its place

## Guidelines
- Choose examples that are philosophically illuminating, not just illustrative
- Ensure examples are clear and accessible while maintaining philosophical rigor
- Examples should genuinely strengthen the argument, not merely repeat it
- Consider both supporting examples and potential counterexamples
- Focus on quality over quantity - a few well-developed examples are better than many superficial ones
- Remember: write the ACTUAL EXAMPLES as they would appear in the final paper
"""

        return prompt

    def get_literature_integration_prompt(
        self,
        move: str,
        current_development: Any,
        framework: Dict[str, Any],
        outline: Dict[str, Any],
        literature: Dict[str, Any],
    ) -> str:
        """
        Construct prompt for integrating literature into a key move.
        
        This focuses on connecting the move to relevant philosophical literature.
        """
        # Extract the current development content, handling various inputs
        if current_development is None:
            # If no current development provided, extract info from framework
            main_thesis = framework.get("main_thesis", "")
            moves_list = framework.get("key_moves", [])
            move_index = moves_list.index(move) if move in moves_list else -1
            
            current_content = f"""
# Key Move Context
This key move is: "{move}"

It supports the main thesis: "{main_thesis}"

Please integrate relevant literature with this move.
"""
        elif isinstance(current_development, dict):
            current_content = current_development.get("content", "")
        else:
            current_content = str(current_development)
        
        # Extract literature information
        lit_readings = literature.get("readings", {})
        lit_synthesis = literature.get("synthesis", {})
        lit_narrative = literature.get("narrative", "")
        
        # Extract some key literature info to include in the prompt
        lit_summary = ""
        if lit_synthesis:
            themes = lit_synthesis.get("themes", [])
            lit_summary = "Key themes in the literature:\n"
            for theme in themes[:3]:  # Limit to first 3 themes to keep prompt size reasonable
                theme_name = theme.get("name", "")
                theme_desc = theme.get("description", "")
                lit_summary += f"- {theme_name}: {theme_desc}\n"
        
        prompt = f"""# Key Move Development: Literature Integration

## Phase II.3 Context
You are participating in Phase II.3 (Key Moves Development) of a multi-phase philosophy paper generation process.

Your task is to integrate relevant literature into this key move in a way that's ready for direct inclusion in the final paper. The literature integration must be written in the style it would appear in the published paper. Later phases will focus only on prose refinement and will not create new literature connections or arguments.

## Current Development
Here is the current development of the key move:

```
{current_content}
```

## Literature Context
{lit_summary}

## Important Constraints
- This paper targets Analysis journal's 4,000-word limit. Be extremely selective with citations.
- Cite only the most directly relevant works that provide essential context for your argument.
- Avoid literature "surveys" that list multiple authors making similar points.
- Focus on how your argument extends beyond, challenges, or synthesizes existing views.

## Requirements
Integrate literature into this key move AS IT WOULD APPEAR IN THE FINAL PAPER. This means:

1. Write scholarly philosophical prose that naturally incorporates literature
2. Present literature engagement as it would appear in the published paper
3. Cite and discuss relevant works in a substantive, not superficial, way
4. Position the move properly within the philosophical landscape
5. Make all intellectual decisions now - don't defer any for "later phases"

## Strategic Considerations
Determine whether and how this move needs literature engagement:
- If the move presents a novel argument, focus on positioning it within existing debates
- If responding to specific views, engage directly with those primary sources
- If extending existing work, clarify your original contribution
- In all cases, be highly selective - only cite what's truly necessary

## Output Format
Write your literature integration in clear scholarly philosophical prose as it would appear in the final paper. Do NOT use meta-commentary like "This move connects to X's work..." Instead, integrate the literature directly:

IMPORTANT:
- DO NOT use phrases like "This would connect to..." or "The author could cite..."
- DO NOT write in bullet points or outline format
- DO NOT leave placeholder text or references to "future development"
- DO write with proper scholarly citations as they would appear in the paper
- DO engage with the philosophical content of cited works, not just mention names
- DO position the move within relevant philosophical debates and traditions
- DO be selective and focused - every citation should directly advance the argument

## Guidelines
- Focus on quality of engagement rather than quantity of citations
- Literature should genuinely strengthen the argument, not merely name-drop
- Engage with both supporting and challenging perspectives when necessary
- Demonstrate how the move advances beyond existing work
- Remember: write the ACTUAL LITERATURE INTEGRATION as it would appear in the paper
"""

        return prompt 