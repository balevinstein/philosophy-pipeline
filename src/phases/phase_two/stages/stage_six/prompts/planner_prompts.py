import json
from typing import Dict, Any
from src.utils.prompt_utils import load_and_combine_style_guides

class RevisionPlannerPrompts:
    """Prompts for the Revision Planner worker in Phase II.5."""

    def __init__(self):
        style_guide = load_and_combine_style_guides()
        self.system_prompt = f"""{style_guide}
        
You are a brilliant developmental editor for a philosophy press. You have a unique talent for seeing the "paper that could be" inside a messy and flawed draft plan. You are given a complete paper plan and a brutally harsh "hostile referee" report on it. Your task is to synthesize this information and create a new, coherent, and actionable writing plan that salvages the project. You are a constructive problem-solver, turning the referee's critique into a clear roadmap for revision."""

    def get_planning_prompt(
        self,
        detailed_outline: str,
        developed_moves: Dict[str, Any],
        referee_report: Dict[str, Any],
        move_examples: Dict[str, Any],
        diagnostic_analysis: Dict[str, Any] = None
    ) -> str:
        """Construct the prompt for the revision planning."""
        
        # Format diagnostic insights if available
        diagnostic_section = ""
        if diagnostic_analysis:
            diagnostic_section = f"""

<diagnostic_analysis>
The following diagnostic analysis was performed before the referee review, identifying specific issues with coherence, philosophical quality, and structure. Use this alongside the referee report to create a comprehensive revision plan.

<identified_issues>
{json.dumps(diagnostic_analysis.get('identified_issues', []), indent=2)}
</identified_issues>

<quality_standard_violations>
{json.dumps(diagnostic_analysis.get('quality_standard_violations', []), indent=2)}
</quality_standard_violations>

<priority_issues>
High Priority Issues:
{json.dumps(diagnostic_analysis.get('priority_issues', {}).get('high_priority', []), indent=2)}

Medium Priority Issues:  
{json.dumps(diagnostic_analysis.get('priority_issues', {}).get('medium_priority', []), indent=2)}
</priority_issues>
</diagnostic_analysis>"""
        
        return f"""<task>
You are the developmental editor tasked with saving this paper. You have the original paper plan and a hostile referee report. Your job is to create a new, revised, and coherent writing plan that addresses the referee's concerns and creates a clear path to a publishable, 4,000-word *Analysis*-style paper. The final plan should encourage the use of sophisticated philosophical moves like the examples provided.
</task>
{diagnostic_section}
<philosophical_move_examples>
Here are examples of high-quality philosophical moves that should be present in a top-tier philosophy paper. Your revised plan should create opportunities for these kinds of moves.

{json.dumps(move_examples, indent=2)}
</philosophical_move_examples>

<source_documents>
<original_paper_plan>
<detailed_outline>
{detailed_outline}
</detailed_outline>
<developed_key_moves>
{json.dumps(developed_moves, indent=2)}
</developed_key_moves>
</original_paper_plan>

<hostile_referee_report>
{json.dumps(referee_report, indent=2)}
</hostile_referee_report>
</source_documents>

<planning_instructions>
Your task is to produce a NEW, coherent `final_writing_plan`. Do not just summarize the referee's points; your job is to SOLVE the problems.

1.  **Triage the Issues:** Start by focusing on the `most_damaging_flaw` identified by the referee. Your plan must address this head-on.
2.  **Make Executive Decisions:** You have the authority to make major changes. This includes:
    *   **Revising the Thesis:** Propose a slightly modified main thesis or core contribution if it resolves a major contradiction.
    *   **Cutting/Merging Moves:** Explicitly state which key moves should be CUT or MERGED. If a move is cut, explain why.
    *   **Flagging for Redevelopment:** If a key move is promising but flawed, you can flag it for complete redevelopment (the pipeline will handle re-running the worker for that move).
    *   **Proposing New "Bridge" Arguments:** If there's a logical gap, specify the need for a new, small argument to connect two sections.
    *   **Restructuring the Outline:** Create a new, leaner outline that is realistic for a 4,000-word paper. Do not be afraid to cut or merge entire sections from the original outline.
3.  **Provide Clear Justifications:** For every major change you propose, briefly explain how it addresses a specific issue raised in the referee report.
4.  **Be Concrete:** Your output should be a complete and actionable plan that can be handed directly to the Phase III writing workers.
5.  **Ensure Analysis Style:** The revised plan should enable writing that follows Analysis journal conventions:
    *   **Hook → Thesis → Roadmap** structure for the introduction
    *   **Claim → Example → Analysis** pattern within sections
    *   **Conversational tone** with direct reader engagement
    *   **Philosophical moves** that match the sophistication of the provided examples
    *   **Word economy** - every sentence must advance the argument
6.  **Address Anti-RLHF Concerns:** The plan should encourage:
    *   **Taking clear positions** rather than hedging
    *   **Drawing controversial implications** when warranted
    *   **Making original arguments** rather than merely surveying literature
    *   **Engaging with the strongest** rather than weakest versions of objections
7.  **CRITICAL JSON FORMATTING:** 
    - Ensure all string values in the JSON output are single-line and do not contain any unescaped newline or tab characters
    - Do not use any control characters (like \\n, \\t, \\r) in string values - use spaces instead
    - Always use double quotes for strings, never single quotes
    - Do not include ANY text before or after the JSON object
    - The parsing of this output is automated and will fail on malformed JSON

</planning_instructions>

<output_format>
Your output must be a valid JSON object. Do not include any text outside the main JSON structure. The structure should be a new, complete writing plan.

{{
    "revised_thesis": "The (potentially) revised main thesis for the paper. If no change, state the original.",
    "revised_core_contribution": "The (potentially) revised core contribution. If no change, state the original.",
    "revision_summary": "A brief, high-level summary of the major changes made to the paper plan and the rationale behind them.",
    "final_key_moves": [
        {{
            "move_index": "The original index of the key move.",
            "status": "Retained | Merged | Flagged for Redevelopment | Cut",
            "revised_description": "The revised description of the key move (if applicable).",
            "justification": "A brief explanation of the decision (e.g., 'Cut due to contradiction with thesis,' 'Retained but reframed to support new thesis')."
        }}
    ],
    "final_outline": {{
        "introduction": {{
            "word_target": 400,
            "content_guidance": "Detailed guidance for writing the introduction, incorporating any necessary framing changes."
        }},
        "section_2": {{
            "title": "Title of the new Section 2",
            "word_target": 800,
            "content_guidance": "Detailed guidance for writing this section, specifying which (revised) key moves it should develop."
        }},
        "section_3": {{
            "title": "Title of the new Section 3",
            "word_target": 800,
            "content_guidance": "..."
        }},
        "conclusion": {{
            "word_target": 400,
            "content_guidance": "Detailed guidance for the conclusion."
        }}
    }}
}}
</output_format>

<analysis_writing_patterns>
When providing content_guidance, ensure it encourages these Analysis journal patterns:

**Introduction Pattern:**
- Start with a compelling hook (puzzle, striking example, or counterintuitive claim)
- State the thesis clearly by paragraph 2
- Provide a roadmap of the argument structure
- Use conversational tone: "I argue that..." not "This paper argues..."

**Section Patterns:**
- Begin each section with a clear claim
- Follow with a concrete example or case
- Provide sustained philosophical analysis of what the example shows
- Connect back to the main thesis

**Move Integration:**
- Reference the philosophical move examples when relevant
- Show how revised moves can achieve similar sophistication
- Create opportunities for elegant argumentative turns

**Tone Requirements:**
- Direct engagement with the reader
- Confident assertions rather than hedged claims
- Willingness to draw controversial implications
- No apologizing for taking positions
</analysis_writing_patterns>
"""

    def get_system_prompt(self) -> str:
        """Return the system prompt for API calls."""
        return self.system_prompt 