from typing import Dict, Any, Optional, List, Union


class MoveCriticPrompts:
    """Prompts for critiquing key move development in Phase II.3."""

    def __init__(self):
        self.system_prompt = """You are a rigorous philosophy journal reviewer evaluating key argumentative moves. Your role is to ensure content is publication-ready and can be directly inserted into the final paper. Do not be polite or deferential. Be constructive but skeptical. Your critique will guide refinement in an automated system."""

    def get_initial_critique_prompt(
        self,
        move: str,
        move_development: Union[Dict[str, Any], str],
        framework: Dict[str, Any],
        outline: Dict[str, Any],
        literature: Dict[str, Any],
        iteration: int,
    ) -> str:
        """
        Construct prompt for critiquing the initial development of a key move.

        This focuses on evaluating the argument structure and logical coherence.
        """
        # Extract the current development content
        if isinstance(move_development, dict):
            current_content = move_development.get("content", "")
        else:
            current_content = move_development

        # Get the main thesis and contribution from the framework
        main_thesis = framework.get("main_thesis", "")

        prompt = f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.3 (Key Moves Development).
Your role is crucial in ensuring that content developed is ready for direct inclusion in the final paper.
The goal is content requiring no further intellectual development - later phases only integrate and refine prose.
Your critique must be genuine and rigorous - the pipeline depends on honest criticism to succeed.
</context>

<task>
Critique the development of this philosophical key move.
Evaluate whether the content is written in publication-ready style for direct insertion into the final paper.
Identify any meta-commentary, incomplete arguments, or deferred intellectual decisions.
Consider the 4,000-word limit - each move should be approximately 500-600 words maximum.
</task>

<current_development>
{current_content}
</current_development>

<move_context>
Original move description: "{move}"
Main thesis: "{main_thesis}"
</move_context>

<requirements>
Evaluate whether the content is truly publication-ready:

1. CONTENT FORMAT: Is it written as actual paper content or as meta-commentary/analysis?
2. COMPLETENESS: Are all necessary arguments fully developed? (Note: not every move requires examples or literature citations)
3. PUBLICATION READINESS: Could this content be directly inserted into a published paper?
4. INTELLECTUAL DECISIONS: Have all intellectual decisions been made or are some deferred?
5. SCHOLARLY STYLE: Is it written in appropriate scholarly philosophical prose?
6. BREVITY: Does it stay within the target length (500-600 words)? Is it concise and focused?
7. APPROACH SUITABILITY: Is the chosen approach appropriate for this specific move?

RED FLAGS to identify:
- Phrases like "This move would..." or "This section demonstrates..." (planning language)
- Headings like "Move Analysis," "Argument Structure," or similar analytical frameworks
- Bullet points or outline format instead of prose paragraphs
- Unnecessary examples when the argument is already clear without them
- Excessive literature citations that don't directly advance the argument
- "This could be expanded..." or similar deferral language
- Content that significantly exceeds the target length
</requirements>

<output_format>
# Critique
[Provide a detailed critique of whether the content is truly publication-ready, addressing each requirement above. Be specific about issues that need fixing to make the content directly usable.]

# Summary Assessment
[MAJOR REVISION / MINOR REFINEMENT / MINIMAL CHANGES]
[Brief explanation of assessment]

Next steps: [List 2-5 specific, actionable recommendations for making the content publication-ready]
</output_format>

<guidelines>
- Be rigorous but constructive
- Focus on publication readiness, not just argument quality
- Provide specific, actionable recommendations
- Balance critique with recognition of strengths
- Evaluate whether examples and literature are necessary
- Remember: the goal is content that can be directly inserted into the final paper
</guidelines>"""

        return prompt

    def get_examples_critique_prompt(
        self,
        move: str,
        move_development: Union[Dict[str, Any], str],
        framework: Dict[str, Any],
        outline: Dict[str, Any],
        literature: Dict[str, Any],
        iteration: int,
    ) -> str:
        """
        Construct prompt for critiquing the examples in a key move development.

        This focuses on evaluating the effectiveness of examples and illustrations.
        """
        # Extract the current development content
        if isinstance(move_development, dict):
            current_content = move_development.get("content", "")
        else:
            current_content = move_development

        prompt = f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.3 (Key Moves Development).
You are evaluating whether examples are publication-ready for direct inclusion in the final paper.
The goal is examples requiring no further development - later phases only integrate and refine prose.
Your critique must determine if examples genuinely strengthen the argument or should be removed.
</context>

<task>
Critique the examples and illustrations in this philosophical key move.
Evaluate whether examples are written in publication-ready style for direct insertion.
Determine if examples are necessary or if the argument would be clearer without them.
Consider the 4,000-word limit - examples must be concise and essential.
</task>

<current_development>
{current_content}
</current_development>

<requirements>
Evaluate whether the examples are truly publication-ready:

1. NECESSITY: Are examples actually needed for this move? Would the argument be clear without them?
2. EXAMPLE FORMAT: Are examples written as they would appear in the final paper or just described/outlined?
3. COMPLETENESS: Are all examples fully detailed with necessary context and explanation?
4. INTEGRATION: Are examples naturally integrated into the philosophical argument?
5. DEVELOPMENT LEVEL: Are examples completely developed or do they need further elaboration?
6. BREVITY: Are examples concise and efficient? Do they use wordcount wisely?
7. SCHOLARLY STYLE: Are examples presented in appropriate scholarly philosophical prose?

RED FLAGS to identify:
- Phrases like "An example would be..." or "This could be illustrated by..." (planning language)
- Examples that are merely mentioned rather than fully developed
- Examples prefaced with "For example" without natural integration
- Bullet points or outline format instead of prose paragraphs
- Examples lacking necessary details or context
- "This example could be expanded..." or similar deferral language
- Unnecessarily lengthy examples that could be more concise
- Examples that don't genuinely strengthen or clarify the argument
</requirements>

<output_format>
# Critique
[Provide a detailed critique of whether examples are truly publication-ready. Be specific about issues. If examples are unnecessary, explicitly recommend removing them.]

# Summary Assessment
[MAJOR REVISION / MINOR REFINEMENT / MINIMAL CHANGES / EXAMPLES UNNECESSARY]
[Brief explanation of assessment]

Next steps: [List 2-5 specific, actionable recommendations for improving examples or removing unnecessary ones]
</output_format>

<guidelines>
- Be rigorous but constructive
- Focus on publication readiness and necessity
- Provide specific, actionable recommendations
- Consider whether examples truly add value
- Remember: quality over quantity - one perfect example beats several mediocre ones
</guidelines>"""

        return prompt

    def get_literature_critique_prompt(
        self,
        move: str,
        move_development: Union[Dict[str, Any], str],
        framework: Dict[str, Any],
        outline: Dict[str, Any],
        literature: Dict[str, Any],
        iteration: int,
    ) -> str:
        """
        Construct prompt for critiquing the literature integration in a key move development.

        This focuses on evaluating how effectively literature is integrated into the move.
        """
        # Extract the current development content
        if isinstance(move_development, dict):
            current_content = move_development.get("content", "")
        else:
            current_content = move_development

        # Extract some literature context
        lit_summary = ""
        lit_synthesis = literature.get("synthesis", {})
        if lit_synthesis:
            key_sources = lit_synthesis.get("key_sources", [])
            if key_sources:
                lit_summary = "Key sources in the literature:\n"
                for source in key_sources[:3]:  # Limit to first 3 sources
                    source_title = source.get("title", "")
                    source_author = source.get("author", "")
                    lit_summary += f"- {source_title} by {source_author}\n"

        prompt = f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.3 (Key Moves Development).
You are evaluating whether literature integration is publication-ready for direct inclusion.
The goal is literature engagement requiring no further development - later phases only refine prose.
Your critique must determine if citations genuinely advance the argument or should be reduced.
</context>

<task>
Critique how philosophical literature has been integrated into this key move.
Evaluate whether literature integration is written in publication-ready style.
Determine if citations are necessary and selective, or excessive and distracting.
Consider the 4,000-word limit - literature citations must be essential.
</task>

<current_development>
{current_content}
</current_development>

<literature_context>
{lit_summary}
</literature_context>

<requirements>
Evaluate whether the literature integration is truly publication-ready:

1. NECESSITY: Is literature engagement actually needed for this move? Would the argument stand alone?
2. INTEGRATION FORMAT: Is literature naturally incorporated as it would appear in a paper?
3. CITATION STYLE: Are works cited properly in scholarly format, not just mentioned?
4. ENGAGEMENT DEPTH: Is there substantive engagement with cited works, not just name-dropping?
5. SELECTIVITY: Are only the most directly relevant works cited? Are any citations unnecessary?
6. POSITIONING: Is the move properly positioned within philosophical debates?
7. SCHOLARLY TONE: Is literature discussed in appropriate scholarly philosophical prose?
8. BREVITY: Is the literature engagement concise and focused?
9. ACCURACY: Is the literature integration accurate? (Flag if unsure, but mention this explicitly)

RED FLAGS to identify:
- Phrases like "This move connects to..." or "The author should cite..." (planning language)
- Literature merely listed rather than substantively engaged
- Citations prefaced with "We should cite" or similar meta-commentary
- Bullet points or outline format instead of prose paragraphs
- Literature mentioned without proper scholarly citation format
- "This literature engagement could be expanded..." or deferral language
- "Survey" approaches listing multiple authors making similar points
- Excessive citations that don't directly advance the argument
</requirements>

<output_format>
# Critique
[Provide a detailed critique of whether literature integration is publication-ready. Be specific about issues. If engagement is excessive, explicitly recommend reducing it.]

# Summary Assessment
[MAJOR REVISION / MINOR REFINEMENT / MINIMAL CHANGES / REDUCE CITATIONS]
[Brief explanation of assessment]

Next steps: [List 2-5 specific, actionable recommendations for improving literature integration or reducing unnecessary citations]
</output_format>

<guidelines>
- Be rigorous but constructive
- Focus on publication readiness and selectivity
- Provide specific, actionable recommendations
- Consider whether each citation truly advances the argument
- Remember: quality of engagement over quantity of citations
</guidelines>"""

        return prompt

    def get_system_prompt(self) -> str:
        """Return the system prompt for API calls"""
        return self.system_prompt
