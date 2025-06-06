from typing import Dict, Any, Optional, List, Union


class MoveRefinementPrompts:
    """Prompts for refining key move development in Phase II.3."""

    def __init__(self):
        self.system_prompt = """You are an expert philosophy editor refining key argumentative moves for publication. Your role is to transform content into publication-ready form based on critique. You must produce polished philosophical prose that can be directly inserted into the final paper. Your refinements will be used in an automated pipeline."""

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

        prompt = f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.3 (Key Moves Development).
You are refining content to ensure it's ready for direct inclusion in the final paper.
Later phases will only integrate content and refine prose, not develop new arguments.
Your task is to transform content into publication-ready form based on critical feedback.
</context>

<task>
Refine this philosophical key move based on the critique provided.
Transform the content into publication-ready form for direct insertion into a scholarly paper.
Address all critique recommendations while maintaining philosophical depth.
Ensure the move stays within 500-600 words (Analysis journal limit).
</task>

<current_development>
{current_content}
</current_development>

<critique_received>
Critique: {critique_content}
Assessment: {critique_assessment}
Key Recommendations:
{recommendations_text}
</critique_received>

<requirements>
# PRESERVE PHILOSOPHICAL TENSION (RLHF-Proofing)
Your training pushes you to:
- Smooth over productive disagreements
- Harmonize conflicting intuitions unnecessarily
- Remove "sharp edges" that make philosophy interesting
- Create false agreement where disagreement is valuable

RESIST. Good philosophy often:
- Maintains tension between competing intuitions
- Preserves paradoxes that motivate inquiry
- Keeps controversial implications explicit
- Shows where reasonable people disagree

If the original had philosophical bite, DON'T FILE DOWN THE TEETH.

Transform the content into publication-ready form by:

1. Converting ANY remaining meta-commentary into direct philosophical content
2. Restructuring content to flow as it would in a published paper
3. Writing in proper scholarly philosophical prose throughout
4. Ensuring all arguments are fully developed with premises and conclusions
5. Making all intellectual decisions now - nothing deferred to later phases
6. Keeping within the 500-600 word target
7. Including only essential examples and literature citations if needed
</requirements>

<output_format>
# Refined Development
[Provide the fully refined development as it would appear in the final published paper]

# Refinement Changes
[Briefly list specific changes made to address critique and transform to publication-ready form]

IMPORTANT:
- DO NOT use phrases like "This move demonstrates..." or "This section will..."
- DO NOT use planning headings like "Move Analysis" or "Argument Structure"
- DO NOT use bullet points or outline format
- DO write in complete scholarly paragraphs as in final paper
- DO incorporate all intellectual content from original
- DO make all arguments publication-ready
- DO be selective about examples and literature
- DO stay within 500-600 word target
</output_format>

<guidelines>
- Implement key recommendations from critique if you agree
- Maintain philosophical depth while improving readability
- Transform planning language into direct philosophical prose
- Ensure content could be directly inserted into published paper
- Make substantive improvements, not superficial edits
- Be ruthless about cutting non-essential content
- Prioritize clarity, conciseness, and philosophical depth
</guidelines>"""

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

        prompt = f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.3 (Key Moves Development).
You are refining examples to ensure they're ready for direct inclusion in the final paper.
Later phases will only integrate content and refine prose, not develop new examples.
Your task is to transform examples into publication-ready form or remove them if unnecessary.
</context>

<task>
Refine the examples in this philosophical key move based on the critique.
Transform examples into publication-ready form for direct insertion into a scholarly paper.
First determine if examples are truly necessary - if not, recommend removal.
Keep examples concise and essential (4,000-word limit constraint).
</task>

<current_development>
{current_content}
</current_development>

<critique_received>
Critique: {critique_content}
Assessment: {critique_assessment}
Key Recommendations:
{recommendations_text}
</critique_received>

<requirements>
Transform examples into publication-ready form by:

1. First determining if examples are truly necessary - if not, recommend removal
2. If necessary, converting descriptions into actual examples as they'd appear
3. Integrating examples naturally into philosophical prose
4. Providing only essential context and details
5. Ensuring examples are fully developed and clearly presented
6. Making examples as concise as possible while effective
7. Making all intellectual decisions now - nothing deferred
</requirements>

<output_format>
# Refined Development
[Provide fully refined development with examples as they'd appear in final paper. If examples should be removed, recommend explicitly and provide version without them.]

# Refinement Changes
[List specific changes made to address critique and transform to publication-ready form]

IMPORTANT:
- DO NOT use phrases like "An example would be..." or "This illustrates..."
- DO NOT just describe examples - write them as they'd appear
- DO NOT use bullet points or outline format
- DO consider whether examples are truly necessary
- DO write examples in complete scholarly paragraphs
- DO provide only essential context
- DO make examples flow naturally with argument
- DO make examples as concise as possible
</output_format>

<guidelines>
- Implement key recommendations from critique if you agree
- Maintain philosophical depth while improving clarity
- Transform meta-commentary into direct examples
- Ensure examples could be directly inserted into paper
- Make substantive improvements, not superficial edits
- Be ruthless about cutting unnecessary examples
- If critique suggests removal, seriously consider it
</guidelines>"""

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

        prompt = f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.3 (Key Moves Development).
You are refining literature integration for direct inclusion in the final paper.
Later phases will only integrate content and refine prose, not develop new literature connections.
Your task is to transform literature integration into publication-ready form or reduce if excessive.
</context>

<task>
Refine the literature integration in this philosophical key move based on critique.
Transform into publication-ready form for direct insertion into a scholarly paper.
First determine if current engagement is excessive - if so, reduce it.
Focus on quality over quantity - cite only most relevant works.
</task>

<current_development>
{current_content}
</current_development>

<critique_received>
Critique: {critique_content}
Assessment: {critique_assessment}
Key Recommendations:
{recommendations_text}
</critique_received>

<requirements>
Transform literature integration into publication-ready form by:

1. First determining if engagement is necessary or excessive - reduce if needed
2. Converting descriptions into actual scholarly engagement as it'd appear
3. Integrating literature naturally into philosophical prose
4. Citing only most directly relevant works providing essential context
5. Ensuring substantive engagement with cited works, not name-dropping
6. Making literature integration concise while effective
7. Making all intellectual decisions now - nothing deferred
</requirements>

<output_format>
# Refined Development
[Provide fully refined development with literature as it'd appear in final paper. If engagement should be reduced, provide more selective version.]

# Refinement Changes
[List specific changes made to address critique and transform to publication-ready form]

IMPORTANT:
- DO NOT use phrases like "This connects to..." or "The author should cite..."
- DO NOT just describe connections - write them as they'd appear
- DO NOT use bullet points or outline format
- DO consider whether engagement is excessive - reduce if so
- DO write integration in complete scholarly paragraphs
- DO provide proper citations in scholarly format
- DO engage with philosophical content, not just mention names
- DO make integration as concise as possible
</output_format>

<guidelines>
- Implement key recommendations from critique if you agree
- Maintain philosophical depth while improving clarity
- Transform meta-commentary into direct scholarly engagement
- Ensure integration could be directly inserted into paper
- Make substantive improvements, not superficial edits
- Be ruthless about cutting unnecessary citations
- Focus on how argument extends/challenges/synthesizes existing views
- If critique suggests reducing, seriously consider it
</guidelines>"""

        return prompt

    def get_system_prompt(self) -> str:
        """Return the system prompt for API calls"""
        return self.system_prompt
