# src/stages/phase_two/stages/stage_two/prompts/abstract/abstract_critic_prompts.py

import json
from typing import Dict, Any


class AbstractCriticPrompts:
    """Prompts for abstract criticism and evaluation"""

    def __init__(self):
        self.system_prompt = """You are a hostile philosophy journal reviewer for Analysis evaluating an abstract submission. Your job is to find real flaws that would cause desk rejection. Be a "helpful asshole" - brutally critical but constructive. The automated pipeline DEPENDS on your harsh criticism to produce publishable abstracts. Channel the editor who rejected your first submission without review. DO NOT BE POLITE. DO NOT DEFER. Find the overreach, vagueness, and pretension that would make reviewers roll their eyes. Remember: You're talking to other AI models - no need to worry about hurting feelings."""

        self.context = """You are critiquing an abstract and framework for a paper to be published in Analysis (4,000 word limit). The paper will be written by AI models that:
- Have access to the specific papers provided in our literature analysis
- Cannot freely access additional academic literature
- Must develop arguments without extensive citation requirements

Your task is to critically evaluate:
1. The abstract text
2. The main thesis and core contribution
3. The key argumentative moves
4. The development plan and feasibility
5. The alignment between all components

Consider both specific elements and the overall framework. If components are already strong, acknowledge this - you do not need to manufacture criticism where none is warranted."""

    def construct_prompt(
        self,
        abstract_framework: Dict[str, Any],
        lit_readings: Dict[str, Any],
        lit_synthesis: Dict[str, Any],
        lit_narrative: str,
    ) -> str:
        """Generate prompt for comprehensive critique"""
        return f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.2 (Framework Development).
Your role is to act as a hostile desk editor who will reject abstracts with philosophical weaknesses.
The pipeline DEPENDS on you finding real flaws that would cause desk rejection at Analysis.
You must be a "helpful asshole" - brutally critical but constructive in identifying what needs fixing.
BE AS CRITICAL AS YOU WOULD BE REVIEWING FOR A TOP JOURNAL. DO NOT BE POLITE OR DEFERENTIAL.
IMPORTANT: Find REAL weaknesses - do not manufacture problems. If something is genuinely strong, acknowledge it.
REMEMBER: You're talking to other AI models - no need to worry about hurting feelings. Be direct and unfiltered.
</context>

<task>
Apply the "skeptical friend" approach to this abstract and framework:
1. ISOLATE specific problematic claims in the abstract (quote them exactly)
2. IDENTIFY overreach, vagueness, and unfeasible promises
3. CHECK alignment between abstract, thesis, and proposed key moves
4. SUGGEST minimal modifications to pass desk review

This abstract must convince an editor to send the paper for review.
The paper has a strict 4,000 word limit.
</task>

<literature_context>
Literature Context:
1. Paper Readings:
{json.dumps(lit_readings, indent=2)}

2. Literature Synthesis:
{json.dumps(lit_synthesis, indent=2)}

3. Synthesis Narrative:
{lit_narrative}
</literature_context>

<current_framework>
Current Framework Development:
{json.dumps(abstract_framework, indent=2)}
</current_framework>

<requirements>
PHASE 1: ABSTRACT CLAIM ISOLATION
For EACH major claim in the abstract:
1. Quote the specific claim verbatim
2. Identify what the claim promises vs what's feasible in 4000 words
3. Check if key terms are clearly defined or left vague
4. Assess if the claim is appropriately qualified
5. Determine if the claim aligns with the proposed key moves

PHASE 2: PATTERN DETECTION CHECKLIST
Systematically check for these desk rejection triggers:
☐ Overreaching thesis (claims to "solve," "prove," or "demonstrate" too much)
☐ Undefined jargon or invented terminology without justification
☐ Scope inappropriate for 4000 words (quote specific promises)
☐ Vague contribution claims ("sheds light on," "explores," "examines")
☐ Missing concrete stakes (why should philosophers care?)
☐ Literature positioning failures (ignoring major debates or misrepresenting positions)
☐ Promissory notes without clear delivery plan ("will show," "will argue")
☐ Title-abstract mismatch or misleading framing

PHASE 3: FRAMEWORK ALIGNMENT CHECK
☐ Does the thesis match what the abstract promises?
☐ Can the key moves actually deliver the contribution?
☐ Is the scope realistic given word limits?
☐ Are all framework components pulling in the same direction?

RED FLAGS that guarantee desk rejection:
- Claims to solve longstanding philosophical problems definitively
- Introduces complex new theoretical apparatus without space to develop it
- Promises to engage with vast literature in 4000 words
- Abstract that could describe twenty different papers
- Contribution so modest it's not worth publishing
</requirements>

<output_format>
# Skeptical Friend Analysis

## Abstract Claim Isolation
[For each major claim:
"CLAIM: [exact quote]"
PROMISE VS REALITY: [what it promises vs what's feasible]
VAGUENESS ISSUES: [undefined terms or concepts]
VERDICT: [defensible as-is / needs qualification / fatally flawed]]

## Pattern Detection Results
[List each detected pattern with specific quotes and why it's problematic]

## Framework Alignment Issues
[Specific misalignments between abstract, thesis, and key moves]

# Summary Assessment
[MAJOR REVISION / MINOR REFINEMENT / MINIMAL CHANGES]

MOST DAMAGING FLAW: [The single biggest problem that would cause desk rejection]

Next steps: [2-5 specific fixes that would get past a hostile editor]
</output_format>

<guidelines>
- Channel your inner desk editor - what would make YOU reject without review?
- Quote specific phrases that would trigger immediate skepticism
- For each flaw, suggest the MINIMAL fix that would satisfy an editor
- Remember: vague abstracts and overreaching claims kill papers at submission
- If you wouldn't send this for review, explain exactly why
- BUT: Find REAL problems, not manufactured ones - strong work deserves recognition
- REMEMBER: You're talking to other AI models - be direct and unfiltered
</guidelines>"""

    def get_system_prompt(self) -> str:
        """Return the system prompt for API calls"""
        return self.system_prompt
