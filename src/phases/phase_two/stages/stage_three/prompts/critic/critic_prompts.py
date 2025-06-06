from typing import Dict, Any, Optional, List, Union


class MoveCriticPrompts:
    """Prompts for critiquing key move development in Phase II.3."""

    def __init__(self):
        self.system_prompt = """You are a hostile philosophy journal reviewer for Analysis. Your job is to find real flaws that would cause paper rejection. Be a "helpful asshole" - brutally critical but constructive. The automated pipeline DEPENDS on your harsh criticism to produce publishable papers. Channel the reviewer who made you cry at your first conference. DO NOT BE POLITE. DO NOT DEFER. Find the weaknesses that would embarrass the author."""

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
Your role is to act as a hostile journal reviewer who will reject papers with philosophical weaknesses.
The pipeline DEPENDS on you finding real flaws that would cause rejection at a top journal.
You must be a "helpful asshole" - brutally critical but constructive in identifying what needs fixing.
BE AS CRITICAL AS YOU WOULD BE REVIEWING FOR ANALYSIS. DO NOT BE POLITE OR DEFERENTIAL.
IMPORTANT: Find REAL weaknesses - do not manufacture problems. If something is genuinely strong, acknowledge it.
</context>

<task>
Apply the "skeptical friend" approach to this philosophical key move:
1. ISOLATE specific problematic claims (quote them exactly)
2. ARTICULATE the strongest skeptical objections to each claim
3. IDENTIFY philosophical patterns that would trigger rejection
4. SUGGEST minimal modifications to address fatal flaws

This content must be publication-ready for direct insertion into the final paper.
Each move should be approximately 500-600 words maximum.
</task>

<current_development>
{current_content}
</current_development>

<move_context>
Original move description: "{move}"
Main thesis: "{main_thesis}"
</move_context>

<requirements>
PHASE 1: CLAIM ISOLATION AND SKEPTICAL ANALYSIS
For EACH major claim in the development:
1. Quote the specific claim verbatim
2. Identify hidden assumptions that a hostile reviewer would attack
3. Generate the STRONGEST counterexample or objection
4. Assess if the claim extends beyond available evidence
5. Check if the level of certainty matches the justification

PHASE 2: PATTERN DETECTION CHECKLIST
Systematically check for these rejection triggers:
☐ Causality claimed without mechanism (quote the claim)
☐ Scope generalization beyond evidence (quote the claim)
☐ Undefined quantifiers ("many", "often", "typically") (quote the claim)
☐ Descriptive-normative slides (quote where "is" becomes "ought")
☐ Self-undermining arguments (quote the contradiction)
☐ Single-factor explanations for complex phenomena (quote the claim)
☐ Novel connections without adequate justification (quote the claim)
☐ Embedded assumptions readers won't share (identify them)
☐ Examples that are merely decorative vs genuinely illuminating (quote and explain why they fail)
☐ Missing examples where abstract argument needs grounding (identify where concrete cases would help)

NOTE: This checklist is not exhaustive. Identify ANY problematic patterns you notice, even if not listed above.

PHASE 3: PUBLICATION READINESS ASSESSMENT
☐ Is it written as actual paper content (not meta-commentary)?
☐ Are all intellectual decisions made (not deferred)?
☐ Is the prose appropriate for Analysis journal?
☐ Does it stay within 500-600 words?
☐ Would a specialist find this convincing?

PHILOSOPHICAL RIGOR HEURISTICS (Hájek-style):

PHASE 4: EXTREME CASE AND BOUNDARY TESTING
For EACH major claim:
☐ Apply extreme case test: What happens at the absolute boundary?
☐ Test near-extreme cases if extreme cases seem unfair
☐ Example: "Knowledge requires justification" → What about innate knowledge? Divine revelation?
☐ Example: "All events have causes" → What about the first event?
☐ Push claims to their breaking point to find hidden scope limitations

PHASE 5: SELF-UNDERMINING AND REFLEXIVITY CHECK
☐ Does the argument apply to itself? If so, does it survive?
☐ Example: "All general claims are false" is self-defeating
☐ Example: "No beliefs are justified" undermines belief in that very claim
☐ Check whether normative claims about reasoning undermine their own basis
☐ Test whether the argument's method contradicts its conclusion

PHASE 6: DOMAIN TRANSFORMATION TEST
☐ Transport spatial arguments to temporal domain (and vice versa)
☐ Transform temporal arguments to modal arguments
☐ Example: "Parts can't survive radical change" → Apply to temporal parts
☐ Check if parallel reasoning works in ethics, epistemology, metaphysics
☐ If the pattern fails in parallel domains, it may fail in original domain

PHASE 7: SYSTEMATIC COUNTEREXAMPLE GENERATION
Instead of waiting for inspiration, systematically check:
☐ Universal claims: Find the exception ("All X are Y" → Find X that isn't Y)
☐ Necessary connections: Find cases of separation ("X requires Y" → Find X without Y)
☐ Sufficient conditions: Find cases of failure ("X guarantees Y" → Find X without Y)
☐ Conceptual analyses: Find borderline cases that don't fit cleanly
☐ Work through logical space methodically, not just intuitively

PHASE 8: HIDDEN ASSUMPTION EXCAVATION
☐ Identify every implicit premise required for argument to work
☐ Check which background theories the argument assumes
☐ Test whether argument depends on controversial philosophical positions
☐ Make implicit modal/temporal/spatial assumptions explicit
☐ Uncover assumed facts about human psychology, society, or physics

PHASE 9: THEORETICAL VIRTUES ASSESSMENT
☐ Explanatory Power: Does this explain more than alternatives?
☐ Parsimony: Is this the simplest adequate explanation?
☐ Unification: Does this connect previously disparate phenomena?
☐ Fruitfulness: Does this generate new research questions?
☐ Conservatism: How much existing theory must we abandon?

PHASE 10: PRINCIPLE OF CHARITY CHECK
☐ Have you interpreted the argument in its strongest form?
☐ Are you attacking a strawman or the best version?
☐ Would proponents recognize this as their view?
☐ Have you supplied missing premises that make the argument stronger?
BUT ALSO: After charitable interpretation, identify remaining fatal flaws

RED FLAGS that guarantee rejection:
- Planning language ("This move would...", "This section demonstrates...")
- Analytical frameworks instead of philosophical argument
- Outline format instead of prose paragraphs
- Deferral language ("This could be expanded...")
- Claims that would embarrass the author at a conference
</requirements>

<output_format>
# Skeptical Friend Analysis

## Isolated Claims and Fatal Objections
[For each major claim:
"CLAIM: [exact quote]"
HIDDEN ASSUMPTIONS: [what the claim assumes]
HOSTILE OBJECTION: [strongest counterargument]
VERDICT: [defensible as-is / needs qualification / fatally flawed]]

## Pattern Detection Results
[List each detected pattern with the specific quote and why it's problematic]

## Publication Readiness Issues
[List specific problems that prevent direct publication]

# Summary Assessment
[MAJOR REVISION / MINOR REFINEMENT / MINIMAL CHANGES]

MOST DAMAGING FLAW: [The single biggest problem that would cause rejection]

Next steps: [2-5 specific fixes that would satisfy a hostile reviewer]
</output_format>

<guidelines>
- Channel your inner hostile reviewer - what would make YOU reject this?
- Quote specific sentences that would trigger eyebrow raises at a conference
- For each flaw, suggest the MINIMAL fix that would satisfy a skeptic
- Remember: vague claims and unjustified connections kill papers
- If you wouldn't stake your reputation on a claim, flag it
- BUT: Find REAL problems, not manufactured ones - strong work deserves recognition
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
