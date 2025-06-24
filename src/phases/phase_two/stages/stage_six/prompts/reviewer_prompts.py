import json
from typing import Dict, Any
from src.utils.prompt_utils import load_and_combine_style_guides

class DialecticalReviewerPrompts:
    """Prompts for the Dialectical Reviewer worker in Phase II.5."""

    def __init__(self):
        style_guide = load_and_combine_style_guides()
        self.system_prompt = f"""{style_guide}

You are a senior editor at a top-tier philosophy journal (e.g., Analysis, Mind, Philosophical Review) and a notoriously sharp-witted philosopher known for your 'helpful asshole' reviews. Your task is to conduct a holistic review of a complete paper plan. Your goal is to identify every philosophical weakness, structural flaw, and internal contradiction that would lead to desk rejection or major revisions. You are brutally honest but your goal is constructive: to force the authors to produce a philosophically sound, coherent, and compelling paper. You are speaking to other AI agents, so be direct, blunt, and unfiltered."""

    def get_review_prompt(
        self,
        detailed_outline: str,
        developed_moves: Dict[str, Any],
        main_thesis: str,
        core_contribution: str,
        move_examples: Dict[str, Any],
        diagnostic_analysis: Dict[str, Any] = None
    ) -> str:
        """Construct the prompt for the dialectical review."""
        
        # Format diagnostic insights if available
        diagnostic_section = ""
        if diagnostic_analysis:
            diagnostic_section = f"""

<diagnostic_analysis>
The following diagnostic analysis has already been performed on this paper plan, identifying issues with coherence, philosophical quality, and structure. Use this as a starting point but feel free to identify additional issues.

<identified_issues>
{json.dumps(diagnostic_analysis.get('identified_issues', []), indent=2)}
</identified_issues>

<quality_standard_violations>
{json.dumps(diagnostic_analysis.get('quality_standard_violations', []), indent=2)}
</quality_standard_violations>

<paper_readiness>
{diagnostic_analysis.get('paper_readiness', 'Not assessed')}
</paper_readiness>

<priority_issues>
High Priority Issues:
{json.dumps(diagnostic_analysis.get('priority_issues', {}).get('high_priority', []), indent=2)}

Medium Priority Issues:
{json.dumps(diagnostic_analysis.get('priority_issues', {}).get('medium_priority', []), indent=2)}
</priority_issues>
</diagnostic_analysis>"""
        
        return f"""<task>
You must conduct a comprehensive and hostile review of the following paper plan. Your review will be used to significantly revise the paper's structure and arguments before the final writing phase. Identify every flaw that would prevent this paper from being published in a top journal.

Remember: You are the "helpful asshole" - brutally honest but ultimately constructive. Your harshness serves a purpose: to make the paper bulletproof against real reviewers. Be the skeptical friend who won't let bad arguments slide.
</task>
{diagnostic_section}
<philosophical_move_examples>
Here are examples of high-quality philosophical moves from published Analysis papers. Use these as your quality benchmark - does this paper plan enable moves of similar sophistication?

{json.dumps(move_examples, indent=2)}

Key patterns to look for:
- Do the planned moves have the same intellectual bite as these examples?
- Can the outlined structure support this level of philosophical sophistication?
- Are there opportunities for similarly elegant argumentative turns?
</philosophical_move_examples>

<paper_plan>
<main_thesis>
{main_thesis}
</main_thesis>

<core_contribution>
{core_contribution}
</core_contribution>

<developed_key_moves>
{json.dumps(developed_moves, indent=2)}
</developed_key_moves>

<detailed_outline>
{detailed_outline}
</detailed_outline>
</paper_plan>

<review_instructions>
Conduct your review in three phases.

### Phase 1: Global Coherence and Thesis Integrity
Your primary goal here is to check for internal contradictions and structural integrity.
1.  **Thesis-Move Contradiction:** Read the main thesis. Now read the development of EACH key move. Is there any move that, as developed, contradicts, undermines, or drifts away from the main thesis? Quote the exact text from the move that causes the problem.
2.  **Inter-Move Contradiction:** Do any of the developed key moves contradict each other? Identify any two or more moves that make claims that cannot both be true.
3.  **Outline-Move Mismatch:** Does the detailed outline accurately reflect the content of the developed moves? Or does it paper over problems, misrepresent the arguments, or create a structure that doesn't logically follow from the moves themselves?
4.  **Contribution Check:** Does the plan, as a whole, actually deliver the "core contribution" it promises? Or does it fall short?

### Phase 2: Philosophical Rigor and Argumentative Gaps (The 'Dumbass Claim' Check)
Your goal here is to apply philosophical pressure to the core arguments. For the paper as a whole and for each major section in the outline:
1.  **Identify Argumentative Gaps:** What are the most significant unstated assumptions or logical leaps? What crucial steps are missing?
2.  **Generate Strongest Objections:** What is the single most powerful objection to the paper's central thesis that is not adequately addressed in the plan?
3.  **Demand Clarification:** Where is the terminology most vague or ambiguous? What key terms need sharper definition?
4.  **Demand Elaboration:** Which arguments are too thin or underdeveloped? Where is more substance required to be convincing?
5.  **Check for Triviality:** Is the main thesis interesting and non-trivial? Is there a risk of it being a "merely verbal" dispute?

### Phase 2B: Apply Hájek's Philosophical Heuristics
Test the core arguments against these five diagnostic tests:
1.  **EXTREME CASE TEST:** What happens when you push the thesis to its limits? Do the arguments still hold for edge cases, or do they break down?
2.  **SELF-UNDERMINING TEST:** Does the thesis, if true, provide reasons to doubt itself? Are there self-referential problems?
3.  **COUNTEREXAMPLE GENERATION:** Can you think of clear cases that violate the proposed principles or criteria?
4.  **HIDDEN ASSUMPTIONS:** What unstated premises must be true for the arguments to work? Are these plausible?
5.  **DOMAIN TRANSFER:** If the reasoning were applied to analogous cases in other domains, would it yield absurd results?

### Phase 2C: Anti-RLHF Pattern Detection
Check for these indicators of philosophical cowardice:
1.  **HEDGING:** Does the paper excessively qualify claims to avoid taking clear positions?
2.  **BOTH-SIDESISM:** Does it present opposing views without adjudicating between them?
3.  **SURVEY MODE:** Does it merely catalog existing positions rather than advancing original arguments?
4.  **FALSE BALANCE:** Does it give undue weight to weak objections to appear fair?
5.  **CONCLUSION AVOIDANCE:** Does it fail to draw the obvious (but controversial) implications of its arguments?

### Phase 3: Structural and Editorial Review
Your goal here is to assess the paper's publishability as a piece of writing.
1.  **Word Count & Scope:** The detailed outline has a proposed word count. Is it realistic for a 4,000-word *Analysis*-style paper? Identify the sections that are most bloated or poorly justified in their length. Propose specific cuts or merges.
2.  **Narrative Flow:** Does the paper, as outlined, have a compelling narrative arc? Does it build momentum, or does it get bogged down?
3.  **Redundancy:** Are there arguments or points that are repeated unnecessarily across different sections?

</review_instructions>

<output_format>
Your output must be a valid JSON object. Do not include any text outside the main JSON structure.

{{
    "review_summary": {{
        "overall_assessment": "Desk Reject | Major Revision Required | Minor Revision Required",
        "most_damaging_flaw": "A concise, one-sentence summary of the single biggest problem with this paper plan.",
        "recommended_action": "A summary of the most critical change needed (e.g., 'Re-think and rewrite Key Move 2,' 'Cut Section IV and merge its key point into Section II')."
    }},
    "coherence_issues": [
        {{
            "issue_type": "Thesis-Move Contradiction | Inter-Move Contradiction | Outline-Move Mismatch",
            "description": "A detailed explanation of the problem, quoting the specific contradictory passages from the input.",
            "location": {{
                "move_index": "The index of the problematic key move (if applicable).",
                "outline_section": "The section of the outline where the problem appears (if applicable)."
            }}
        }}
    ],
    "argumentative_weaknesses": [
        {{
            "weakness_type": "Argumentative Gap | Unanswered Objection | Vague Terminology | Underdeveloped Argument | Triviality Concern",
            "description": "A detailed explanation of the philosophical weakness.",
            "location": "The specific key move or outline section where the weakness is most prominent."
        }}
    ],
    "hajek_test_failures": [
        {{
            "test_failed": "Extreme Case | Self-Undermining | Counterexample | Hidden Assumptions | Domain Transfer",
            "description": "Explain how the argument fails this specific test.",
            "location": "The specific claim or argument that fails the test.",
            "severity": "Fatal | Major | Minor"
        }}
    ],
    "anti_rlhf_violations": [
        {{
            "pattern": "Hedging | Both-Sidesism | Survey Mode | False Balance | Conclusion Avoidance",
            "description": "Specific instances of philosophical cowardice.",
            "location": "Where this pattern appears.",
            "fix_required": "How to make the argument more assertive."
        }}
    ],
    "structural_recommendations": [
        {{
            "recommendation_type": "Cut Section | Merge Sections | Reduce Word Count | Reorder Sections",
            "description": "A specific, actionable recommendation for improving the paper's structure and flow.",
            "target_section": "The outline section(s) to which this recommendation applies."
        }}
    ]
}}
</output_format>
"""

    def get_system_prompt(self) -> str:
        """Return the system prompt for API calls."""
        return self.system_prompt 