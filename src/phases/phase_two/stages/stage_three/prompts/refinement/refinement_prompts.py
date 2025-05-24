from typing import Dict, Any, Optional, List, Union


class MoveRefinementPrompts:
    """Prompts for refining key move development in Phase II.3."""

    def get_initial_refinement_prompt(
        self,
        move: str,
        move_development: Union[Dict[str, Any], str],
        critique: Union[Dict[str, Any], str],
        framework: Dict[str, Any],
        outline: Dict[str, Any],
        literature: Dict[str, Any],
        iteration: int,
    ) -> str:
        """
        Construct prompt for refining the initial development of a key move.

        This focuses on improving the argument structure based on critique.
        """
        # Extract the current development content
        if isinstance(move_development, dict):
            current_content = move_development.get("content", "")
        else:
            current_content = move_development

        # Extract the critique content
        if isinstance(critique, dict):
            critique_content = critique.get("content", "")
            critique_assessment = critique.get("assessment", "UNKNOWN")
            critique_recommendations = critique.get("recommendations", [])
        else:
            critique_content = critique
            critique_assessment = "UNKNOWN"
            critique_recommendations = []

        # Format recommendations as a string
        recommendations_text = "\n".join(
            [f"- {rec}" for rec in critique_recommendations]
        )
        if not recommendations_text:
            recommendations_text = "- Review and refine the argument structure"

        prompt = f"""# Key Move Refinement: Creating Publication-Ready Content

## Phase II.3 Context
You are participating in Phase II.3 (Key Moves Development) of a multi-phase philosophy paper generation process.

Your task is to refine the content to ensure it's ready for direct inclusion in the final paper. This content must be written in the style it would appear in the published paper. Later phases will focus only on integrating this content into the paper structure and minor prose refinements, not developing new arguments or ideas.

## Task Description
You are refining the development of a philosophical key move based on critical feedback. Your task is to transform the content into publication-ready form that could be directly inserted into a scholarly philosophy paper.

## Important Constraints
- This paper targets Analysis journal's 4,000-word limit. Each key move should be approximately 500-600 words maximum.
- Not every move requires examples or extensive literature engagement. These elements should only be included when they genuinely strengthen the argument.
- Content should be concise, focused, and avoid unnecessary elaboration.

## Current Development
Here is the current development of the key move:

```
{current_content}
```

## Critique
The critique of this development was:

```
{critique_content}
```

## Assessment: {critique_assessment}

## Key Recommendations
{recommendations_text}

## Refinement Requirements
Transform the content into publication-ready form by:

1. Converting ANY remaining meta-commentary into direct philosophical content
2. Restructuring content to flow as it would in a published paper
3. Writing in proper scholarly philosophical prose throughout
4. Ensuring all arguments are fully developed with premises and conclusions
5. Making all intellectual decisions now - nothing should be deferred to later phases
6. Keeping within the 500-600 word target for the move
7. Including only essential examples and literature citations if they are needed

## Output Format
Your refined output must be ready for direct inclusion in a published paper:

IMPORTANT:
- DO NOT use phrases like "This move demonstrates..." or "This section will..."
- DO NOT use planning headings like "Move Analysis" or "Argument Structure"
- DO NOT use bullet points or outline format
- DO write in complete scholarly paragraphs as they would appear in the final paper
- DO incorporate all intellectual content from the original development
- DO make all arguments publication-ready
- DO be selective about including examples and literature - only include what's necessary
- DO stay within the 500-600 word target for the move

# Refined Development
[Provide the fully refined development as it would appear in the final published paper, incorporating all necessary transformations to make it publication-ready]

# Refinement Changes
[Briefly list the specific changes you made to address the critique recommendations and transform the content into publication-ready form]

## Guidelines
- For any key recommendation from the critique, decide whether you agree it should be implemented. If so, be sure to implement it.
- Maintain philosophical depth while improving readability
- Transform planning language into direct philosophical prose
- Ensure content could be directly inserted into a published paper
- Make substantive improvements, not just superficial edits
- Be ruthless about cutting anything that isn't absolutely necessary
- Prioritize clarity, conciseness, and philosophical depth
"""

        return prompt

    def get_examples_refinement_prompt(
        self,
        move: str,
        move_development: Union[Dict[str, Any], str],
        critique: Union[Dict[str, Any], str],
        framework: Dict[str, Any],
        outline: Dict[str, Any],
        literature: Dict[str, Any],
        iteration: int,
    ) -> str:
        """
        Construct prompt for refining the examples in a key move development.

        This focuses on improving examples and illustrations based on critique.
        """
        # Extract the current development content
        if isinstance(move_development, dict):
            current_content = move_development.get("content", "")
        else:
            current_content = move_development

        # Extract the critique content
        if isinstance(critique, dict):
            critique_content = critique.get("content", "")
            critique_assessment = critique.get("assessment", "UNKNOWN")
            critique_recommendations = critique.get("recommendations", [])
        else:
            critique_content = critique
            critique_assessment = "UNKNOWN"
            critique_recommendations = []

        # Format recommendations as a string
        recommendations_text = "\n".join(
            [f"- {rec}" for rec in critique_recommendations]
        )
        if not recommendations_text:
            recommendations_text = "- Improve examples to better support key premises"

        prompt = f"""# Key Move Refinement: Creating Publication-Ready Examples

## Phase II.3 Context
You are participating in Phase II.3 (Key Moves Development) of a multi-phase philosophy paper generation process.

Your task is to refine the examples to ensure they're ready for direct inclusion in the final paper. These examples must be written in the style they would appear in the published paper. Later phases will focus only on integrating this content into the paper structure and minor prose refinements, not developing new examples.

## Task Description
You are refining the examples in a philosophical key move based on critical feedback. Your task is to transform the examples into publication-ready form that could be directly inserted into a scholarly philosophy paper.

## Important Constraints
- This paper targets Analysis journal's 4,000-word limit. Examples must be concise and essential.
- Not every move requires examples. If the critique suggests examples are unnecessary, consider removing them.
- Each example should be as concise as possible while remaining effective.

## Current Development
Here is the current development of the key move, including examples:

```
{current_content}
```

## Critique
The critique of the examples was:

```
{critique_content}
```

## Assessment: {critique_assessment}

## Key Recommendations
{recommendations_text}

## Refinement Requirements
Transform the examples into publication-ready form by:

1. First determining if examples are truly necessary for this move - if not, recommend their removal
2. If examples are necessary, converting ANY descriptions of examples into actual examples as they would appear in the paper
3. Integrating examples naturally into the philosophical prose
4. Providing only the essential context and details for each example
5. Ensuring examples are fully developed and clearly presented
6. Making examples as concise as possible while maintaining their effectiveness
7. Making all intellectual decisions now - nothing should be deferred to later phases

## Output Format
Your refined examples must be ready for direct inclusion in a published paper:

IMPORTANT:
- DO NOT use phrases like "An example would be..." or "This illustrates..."
- DO NOT just describe examples - write them as they would appear in the paper
- DO NOT use bullet points or outline format
- DO consider whether examples are truly necessary - if not, recommend their removal
- DO write examples in complete scholarly paragraphs as they would appear in the final paper
- DO provide only essential context for each example
- DO make examples flow naturally with the philosophical argument
- DO make examples as concise as possible

# Refined Development
[Provide the fully refined development with examples as they would appear in the final published paper, incorporating all necessary transformations to make them publication-ready. If examples should be removed, recommend this explicitly and provide a version without them.]

# Refinement Changes
[Briefly list the specific changes you made to address the critique recommendations and transform the examples into publication-ready form]

## Guidelines
- For any key recommendation from the critique, decide whether you agree it should be implemented. If so, be sure to implement it.
- Maintain philosophical depth while improving clarity
- Transform meta-commentary into direct examples
- Ensure examples could be directly inserted into a published paper
- Make substantive improvements, not just superficial edits
- Be ruthless about cutting unnecessary examples or making them more concise
- If the critique suggests examples are unnecessary, seriously consider removing them
"""

        return prompt

    def get_literature_refinement_prompt(
        self,
        move: str,
        move_development: Union[Dict[str, Any], str],
        critique: Union[Dict[str, Any], str],
        framework: Dict[str, Any],
        outline: Dict[str, Any],
        literature: Dict[str, Any],
        iteration: int,
    ) -> str:
        """
        Construct prompt for refining the literature integration in a key move development.

        This focuses on improving literature engagement based on critique.
        """
        # Extract the current development content
        if isinstance(move_development, dict):
            current_content = move_development.get("content", "")
        else:
            current_content = move_development

        # Extract the critique content
        if isinstance(critique, dict):
            critique_content = critique.get("content", "")
            critique_assessment = critique.get("assessment", "UNKNOWN")
            critique_recommendations = critique.get("recommendations", [])
        else:
            critique_content = critique
            critique_assessment = "UNKNOWN"
            critique_recommendations = []

        # Format recommendations as a string
        recommendations_text = "\n".join(
            [f"- {rec}" for rec in critique_recommendations]
        )
        if not recommendations_text:
            recommendations_text = (
                "- Improve integration of literature with the key move"
            )

        prompt = f"""# Key Move Refinement: Creating Publication-Ready Literature Integration

## Phase II.3 Context
You are participating in Phase II.3 (Key Moves Development) of a multi-phase philosophy paper generation process.

Your task is to refine the literature integration to ensure it's ready for direct inclusion in the final paper. The literature integration must be written in the style it would appear in the published paper. Later phases will focus only on integrating this content into the paper structure and minor prose refinements, not developing new literature connections.

## Task Description
You are refining the literature integration in a philosophical key move based on critical feedback. Your task is to transform the literature integration into publication-ready form that could be directly inserted into a scholarly philosophy paper.

## Important Constraints
- This paper targets Analysis journal's 4,000-word limit. Literature citations must be selective and essential.
- Not every move requires extensive literature engagement. If the critique suggests reducing citations, seriously consider this.
- Literature engagement should focus on quality over quantity - cite only the most relevant works.

## Current Development
Here is the current development of the key move, including literature integration:

```
{current_content}
```

## Critique
The critique of the literature integration was:

```
{critique_content}
```

## Assessment: {critique_assessment}

## Key Recommendations
{recommendations_text}

## Refinement Requirements
Transform the literature integration into publication-ready form by:

1. First determining if literature engagement is truly necessary for this move - if excessive, reduce it
2. Converting ANY descriptions of literature connections into actual scholarly engagement as it would appear in the paper
3. Integrating literature naturally into the philosophical prose
4. Citing only the most directly relevant works that provide essential context or support
5. Ensuring substantive engagement with cited works, not just name-dropping
6. Making literature integration as concise as possible while maintaining its effectiveness
7. Making all intellectual decisions now - nothing should be deferred to later phases

## Output Format
Your refined literature integration must be ready for direct inclusion in a published paper:

IMPORTANT:
- DO NOT use phrases like "This connects to X's work..." or "The author should cite..."
- DO NOT just describe literature connections - write them as they would appear in the paper
- DO NOT use bullet points or outline format
- DO consider whether literature engagement is truly necessary - if excessive, reduce it
- DO write literature integration in complete scholarly paragraphs as they would appear in the final paper
- DO provide proper citations in scholarly format
- DO engage with the philosophical content of cited works, not just mention names
- DO make literature integration as concise as possible

# Refined Development
[Provide the fully refined development with literature integration as it would appear in the final published paper, incorporating all necessary transformations to make it publication-ready. If literature engagement should be reduced, recommend this explicitly and provide a more selective version.]

# Refinement Changes
[Briefly list the specific changes you made to address the critique recommendations and transform the literature integration into publication-ready form]

## Guidelines
- For any key recommendation from the critique, decide whether you agree it should be implemented. If so, be sure to implement it.
- Maintain philosophical depth while improving clarity
- Transform meta-commentary into direct scholarly engagement
- Ensure literature integration could be directly inserted into a published paper
- Make substantive improvements, not just superficial edits
- Be ruthless about cutting unnecessary citations or making engagement more concise
- If the critique suggests reducing literature engagement, seriously consider doing so
- Focus on how your argument extends beyond, challenges, or synthesizes existing views
"""

        return prompt
