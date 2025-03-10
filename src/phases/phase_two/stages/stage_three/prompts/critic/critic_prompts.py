from typing import Dict, Any, Optional, List, Union


class MoveCriticPrompts:
    """Prompts for critiquing key move development in Phase II.3."""

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
        
        prompt = f"""# Key Move Critique: Publication-Ready Content Evaluation

## Phase II.3 Context
You are participating in Phase II.3 (Key Moves Development) of a multi-phase philosophy paper generation process. Your role is crucial in ensuring that the content developed is ready for direct inclusion in the final paper.

The goal is to develop content that requires no further intellectual development in later phases. Later phases will focus only on integrating this content into the final paper structure and refining the prose, not developing new arguments or examples.

## Task Description
You are critiquing the development of a philosophical key move. Your task is to evaluate whether the content is written in a publication-ready style that can be directly inserted into the final paper, not just as meta-commentary or analysis.

## Important Constraints
- This paper targets Analysis journal's 4,000-word limit. Each key move should be approximately 500-600 words maximum.
- Not every move requires examples or extensive literature engagement. These elements should only be included when they genuinely strengthen the argument.
- Content should be concise, focused, and avoid unnecessary elaboration.

## Current Development
Here is the current development of the key move:

```
{current_content}
```

## Original Move Description
The key move being developed is:
"{move}"

This move is part of a philosophical paper with the following main thesis:
"{main_thesis}"

## Critique Requirements
Evaluate whether the content is truly publication-ready, focusing on:

1. CONTENT FORMAT: Is it written as actual paper content or as meta-commentary/analysis?
2. COMPLETENESS: Are all necessary arguments fully developed? (Note: not every move requires examples or literature citations)
3. PUBLICATION READINESS: Could this content be directly inserted into a published paper?
4. INTELLECTUAL DECISIONS: Have all intellectual decisions been made or are some deferred?
5. SCHOLARLY STYLE: Is it written in appropriate scholarly philosophical prose?
6. BREVITY: Does it stay within the target length (500-600 words)? Is it concise and focused?
7. APPROACH SUITABILITY: Is the chosen approach (conceptual analysis, case-based reasoning, etc.) appropriate for this specific move?

## RED FLAGS to identify:
- Phrases like "This move would..." or "This section demonstrates..." (planning language)
- Headings like "Move Analysis," "Argument Structure," or similar analytical frameworks
- Bullet points or outline format instead of prose paragraphs
- Unnecessary examples when the argument is already clear without them
- Excessive literature citations that don't directly advance the argument
- "This could be expanded..." or similar deferral language
- Content that significantly exceeds the target length (500-600 words)

## Output Format
Structure your critique as follows:

# Critique
[Provide a detailed critique of whether the content is truly publication-ready, addressing each of the requirements above. Be specific about any issues that need to be fixed to make the content directly usable in the final paper.]

# Summary Assessment
[Provide an overall assessment using one of these categories: MAJOR REVISION, MINOR REFINEMENT, or MINIMAL CHANGES. Include a brief explanation of your assessment.

Next steps: List 2-5 specific, actionable recommendations for making the content publication-ready.]

## Guidelines
- Be rigorous but constructive in your critique
- Focus on publication readiness, not just argument quality
- Provide specific, actionable recommendations
- Balance critique with recognition of strengths
- Evaluate whether examples and literature citations are necessary or if they could be reduced/eliminated
- Remember: the goal is content that can be directly inserted into the final paper
"""

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
        
        prompt = f"""# Key Move Critique: Publication-Ready Examples Evaluation

## Phase II.3 Context
You are participating in Phase II.3 (Key Moves Development) of a multi-phase philosophy paper generation process. Your role is crucial in ensuring that the examples developed are ready for direct inclusion in the final paper.

The goal is to develop examples that require no further intellectual development in later phases. Later phases will focus only on integrating this content into the final paper structure and refining the prose, not developing new examples.

## Task Description
You are critiquing the examples and illustrations used in the development of a philosophical key move. Your task is to evaluate whether the examples are written in a publication-ready style that can be directly inserted into the final paper, not just described or outlined.

## Important Constraints
- This paper targets Analysis journal's 4,000-word limit. Examples must be concise and essential.
- Not every move requires examples. Only include examples when they genuinely strengthen or clarify the argument.
- Each example should be as concise as possible while remaining effective.

## Current Development
Here is the current development of the key move, including examples:

```
{current_content}
```

## Critique Requirements
Evaluate whether the examples are truly publication-ready, focusing on:

1. NECESSITY: Are examples actually needed for this move? Would the argument be clear without them?
2. EXAMPLE FORMAT: Are examples written as they would appear in the final paper or just described/outlined?
3. COMPLETENESS: Are all examples fully detailed with necessary context and explanation?
4. INTEGRATION: Are examples naturally integrated into the philosophical argument?
5. DEVELOPMENT LEVEL: Are examples completely developed or do they need further elaboration?
6. BREVITY: Are examples concise and efficient? Do they use wordcount wisely?
7. SCHOLARLY STYLE: Are examples presented in appropriate scholarly philosophical prose?

## RED FLAGS to identify:
- Phrases like "An example would be..." or "This could be illustrated by..." (planning language)
- Examples that are merely mentioned rather than fully developed
- Examples prefaced with "For example" without natural integration into the text
- Bullet points or outline format instead of prose paragraphs
- Examples lacking necessary details or context
- "This example could be expanded..." or similar deferral language
- Unnecessarily lengthy examples that could be more concise
- Examples that don't genuinely strengthen or clarify the argument

## Output Format
Structure your critique as follows:

# Critique
[Provide a detailed critique of whether the examples are truly publication-ready, addressing each of the requirements above. Be specific about any issues that need to be fixed to make the examples directly usable in the final paper. If examples are unnecessary, explicitly recommend removing them.]

# Summary Assessment
[Provide an overall assessment using one of these categories: MAJOR REVISION, MINOR REFINEMENT, MINIMAL CHANGES, or EXAMPLES UNNECESSARY. Include a brief explanation of your assessment.

Next steps: List 2-5 specific, actionable recommendations for making the examples publication-ready or for removing unnecessary examples.]

## Guidelines
- Be rigorous but constructive in your critique
- Focus on publication readiness, not just example quality
- Provide specific, actionable recommendations for improving examples
- Balance critique with recognition of strengths
- Consider whether examples are truly necessary or could be reduced/eliminated
- Remember: the goal is examples that can be directly inserted into the final paper
"""

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
        
        prompt = f"""# Key Move Critique: Publication-Ready Literature Integration Evaluation

## Phase II.3 Context
You are participating in Phase II.3 (Key Moves Development) of a multi-phase philosophy paper generation process. Your role is crucial in ensuring that the literature integration is ready for direct inclusion in the final paper.

The goal is to develop literature integration that requires no further intellectual development in later phases. Later phases will focus only on integrating this content into the final paper structure and refining the prose, not developing new literature connections.

## Task Description
You are critiquing how philosophical literature has been integrated into the development of a key move. Your task is to evaluate whether the literature integration is written in a publication-ready style that can be directly inserted into the final paper, not just described or outlined.

## Important Constraints
- This paper targets Analysis journal's 4,000-word limit. Literature citations must be selective and essential.
- Not every move requires extensive literature engagement. Citations should only be included when they directly advance the argument.
- Literature engagement should focus on quality over quantity - cite only the most relevant works.

## Current Development
Here is the current development of the key move, including literature integration:

```
{current_content}
```

## Literature Context
{lit_summary}

## Critique Requirements
Evaluate whether the literature integration is truly publication-ready, focusing on:

1. NECESSITY: Is literature engagement actually needed for this move? Would the argument stand on its own?
2. INTEGRATION FORMAT: Is literature naturally incorporated into the text as it would appear in a paper?
3. CITATION STYLE: Are works cited properly in scholarly format, not just mentioned?
4. ENGAGEMENT DEPTH: Is there substantive engagement with cited works, not just name-dropping?
5. SELECTIVITY: Are only the most directly relevant works cited? Are any citations unnecessary?
6. POSITIONING: Is the move properly positioned within philosophical debates?
7. SCHOLARLY TONE: Is the literature discussed in appropriate scholarly philosophical prose?
8. BREVITY: Is the literature engagement concise and focused?
9. ACCURACY: Is the literature integration accurate and correct? (It's okay to flag that you yourself are unsure about the accuracy, but mention this explicitly if so!)

## RED FLAGS to identify:
- Phrases like "This move connects to..." or "The author should cite..." (planning language)
- Literature that is merely listed rather than substantively engaged with
- Citations prefaced with "We should cite" or similar meta-commentary
- Bullet points or outline format instead of prose paragraphs
- Literature mentioned without proper scholarly citation format
- "This literature engagement could be expanded..." or similar deferral language
- "Survey" approaches that list multiple authors making similar points
- Excessive citations that don't directly advance the argument

## Output Format
Structure your critique as follows:

# Critique
[Provide a detailed critique of whether the literature integration is truly publication-ready, addressing each of the requirements above. Be specific about any issues that need to be fixed to make the literature integration directly usable in the final paper. If literature engagement is excessive, explicitly recommend reducing it.]

# Summary Assessment
[Provide an overall assessment using one of these categories: MAJOR REVISION, MINOR REFINEMENT, MINIMAL CHANGES, or REDUCE CITATIONS. Include a brief explanation of your assessment.

Next steps: List 2-5 specific, actionable recommendations for making the literature integration publication-ready or for reducing unnecessary citations.]

## Guidelines
- Be rigorous but constructive in your critique
- Focus on publication readiness, not just depth of engagement
- Provide specific, actionable recommendations for improving literature integration
- Balance critique with recognition of strengths
- Consider whether literature engagement is truly necessary or could be reduced
- Remember: the goal is literature integration that can be directly inserted into the final paper
"""

        return prompt 