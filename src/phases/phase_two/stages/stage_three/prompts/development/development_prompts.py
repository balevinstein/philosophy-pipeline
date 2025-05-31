from typing import Dict, Any, Optional, List


class MoveDevelopmentPrompts:
    """Prompts for key move development in Phase II.3."""

    def __init__(self):
        self.system_prompt = """You are an expert philosophy researcher developing key argumentative moves. Your role is to create complete, publication-ready philosophical content that advances the paper's thesis. You must produce concrete arguments, examples, and literature integration - not meta-commentary. Your output will be used directly in an automated paper generation pipeline."""

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

        prompt = f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.3 (Key Moves Development).
- Phase I identified the paper topic and gathered literature
- Phase II.1 processed and analyzed the literature
- Phase II.2 created the paper framework (abstract, thesis, outline)
- We are now in Phase II.3, developing key argumentative moves
- After this, Phase II.4 will create a detailed outline integrating these key moves
- Phase III will focus only on prose crafting, not creating new arguments

Your task is to develop the intellectual content of this key move to completion.
</context>

<task>
Develop this philosophical key move in detail. Write the actual content as it would appear in the final paper.
Each key move is a critical argumentative step that advances the paper's thesis.
Make all intellectual decisions now - create complete arguments, not outlines or plans.
</task>

<input_data>
Key move to develop: "{move}"

Main thesis: "{main_thesis}"

Core contribution: "{core_contribution}"

This is move #{move_index + 1} in the paper's key argumentative structure.

Paper outline:
```
{outline_sections}
```
</input_data>

<requirements>
# Important Constraints
- Target Analysis journal's 4,000-word limit. Each key move should be approximately 500-600 words maximum.
- Be selective and concise. Remove redundant examples or peripheral discussions.

# Content Requirements
Write the actual content for this key move AS IT WOULD APPEAR IN THE FINAL PAPER:
1. Write in scholarly philosophical prose, not meta-commentary
2. Develop a complete, well-structured philosophical argument
3. Include necessary background, premises, and conclusions
4. Connect this move to the paper's overall thesis
5. Make all intellectual decisions now
6. Be bold, interesting, and creative - this is for a top philosophy journal

# Strategic Decisions
Determine what this specific move needs:
- Concrete examples? (Use if conceptually complex or counter-intuitive)
- Literature engagement? (Cite only most directly relevant works)
- Development approach? (Conceptual analysis, case-based reasoning, etc.)

Choose the approach that best serves this specific argument.
</requirements>

<output_format>
Write in clear, crisp, engaging scholarly philosophical prose.

IMPORTANT:
- DO NOT write "Move Analysis", "Argument Structure", or similar headings
- DO NOT use bullet points or outline format
- DO NOT include phrases like "This move would..." or "This section will..."
- DO NOT merely parrot other philosophers' arguments - be ORIGINAL
- DO write in complete paragraphs as they would appear in the final paper
- DO develop all arguments fully with proper premises and conclusions
- DO write in scholarly style appropriate for publication
- DO be concise and focused - remember the 500-600 word target
</output_format>

<guidelines>
- Focus on philosophical depth and rigorous argument development
- Ensure logical coherence and theoretical soundness
- Keep the move realistic in scope while maintaining philosophical significance
- Consider both strengths and potential objections if applicable
- Prioritize philosophical precision and conciseness
- Remember: write the ACTUAL CONTENT, not commentary about it
</guidelines>"""

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

        prompt = f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.3 (Key Moves Development).
You are developing examples for a key move that has already been drafted.
Your examples must be fully developed and written as they would appear in the published paper.
Later phases will focus only on prose refinement, not creating new examples.
</context>

<task>
Develop examples for this key move AS THEY WOULD APPEAR IN THE FINAL PAPER.
Write fully developed examples in scholarly philosophical prose.
Only include examples if they genuinely clarify or strengthen the argument.
</task>

<current_development>
{current_content}
</current_development>

<requirements>
# Important Constraints
- Target Analysis journal's 4,000-word limit. Be extremely selective with examples.
- Each example should be concise yet effective - quality over quantity.
- Only include examples if they genuinely clarify or strengthen the argument.

# Content Requirements
1. Write fully developed examples in scholarly philosophical prose
2. Present examples as they would appear in the published paper
3. Integrate examples naturally within the philosophical argument
4. Include complete details and necessary context
5. Make all intellectual decisions now

# Strategic Considerations
Determine whether this move truly needs examples:
- If already clear without examples, state no additional examples needed
- If examples would strengthen, develop only the most essential ones
- Focus on quality over quantity - one perfect example beats several mediocre ones
</requirements>

<output_format>
Write examples in clear, concise scholarly philosophical prose.

IMPORTANT:
- DO NOT use phrases like "This example would..." or "This case could..."
- DO NOT write in bullet points or outline format
- DO NOT leave placeholder text or "future development" references
- DO write examples as complete, detailed, and publication-ready
- DO integrate examples naturally into the philosophical argument
- DO include all necessary context and details
- DO be concise - every word must earn its place
</output_format>

<guidelines>
- Choose philosophically illuminating examples, not just illustrative ones
- Ensure examples are clear while maintaining philosophical rigor
- Examples should genuinely strengthen the argument, not repeat it
- Consider both supporting examples and potential counterexamples
- Focus on quality over quantity
- Remember: write ACTUAL EXAMPLES as they would appear in the paper
</guidelines>"""

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
            for theme in themes[
                :3
            ]:  # Limit to first 3 themes to keep prompt size reasonable
                theme_name = theme.get("name", "")
                theme_desc = theme.get("description", "")
                lit_summary += f"- {theme_name}: {theme_desc}\n"

        prompt = f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.3 (Key Moves Development).
You are integrating relevant literature into a key move that has been developed.
The literature integration must be written as it would appear in the published paper.
Later phases will focus only on prose refinement, not creating new literature connections.
</context>

<task>
Integrate relevant literature into this key move AS IT WOULD APPEAR IN THE FINAL PAPER.
Write scholarly philosophical prose that naturally incorporates literature.
Position the move properly within the philosophical landscape.
Be highly selective - only cite what's truly necessary.
</task>

<current_development>
{current_content}
</current_development>

<literature_context>
{lit_summary}
</literature_context>

<requirements>
# Important Constraints
- Target Analysis journal's 4,000-word limit. Be extremely selective with citations.
- Cite only the most directly relevant works providing essential context.
- Avoid literature "surveys" listing multiple authors making similar points.
- Focus on how your argument extends beyond, challenges, or synthesizes existing views.

# Content Requirements
1. Write scholarly philosophical prose that naturally incorporates literature
2. Present literature engagement as it would appear in the published paper
3. Cite and discuss relevant works substantively, not superficially
4. Position the move properly within the philosophical landscape
5. Make all intellectual decisions now

# Strategic Considerations
Determine whether and how this move needs literature engagement:
- Novel argument? Focus on positioning within existing debates
- Responding to specific views? Engage directly with primary sources
- Extending existing work? Clarify your original contribution
- In all cases, be highly selective - only cite what's necessary
</requirements>

<output_format>
Write literature integration in clear scholarly philosophical prose.

IMPORTANT:
- DO NOT use phrases like "This would connect to..." or "The author could cite..."
- DO NOT write in bullet points or outline format
- DO NOT leave placeholder text or "future development" references
- DO write with proper scholarly citations as they would appear
- DO engage with philosophical content of cited works, not just name-drop
- DO position the move within relevant philosophical debates
- DO be selective and focused - every citation should advance the argument
</output_format>

<guidelines>
- Focus on quality of engagement rather than quantity of citations
- Literature should genuinely strengthen the argument
- Engage with both supporting and challenging perspectives when necessary
- Demonstrate how the move advances beyond existing work
- Remember: write ACTUAL LITERATURE INTEGRATION as it would appear
</guidelines>"""

        return prompt

    def get_system_prompt(self) -> str:
        """Return the system prompt for API calls"""
        return self.system_prompt
