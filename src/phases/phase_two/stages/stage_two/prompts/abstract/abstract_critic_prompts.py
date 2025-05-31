# src/stages/phase_two/stages/stage_two/prompts/abstract_critic_prompts.py

import json
from typing import Dict, Any


class AbstractCriticPrompts:
    """Prompts for abstract criticism and evaluation"""

    def __init__(self):
        self.system_prompt = """You are a rigorous philosophy journal reviewer evaluating a paper submission. Your role is to provide genuinely critical analysis - identifying real weaknesses, gaps, and areas for improvement. Do not be polite or deferential. Be constructive but skeptical. Your critique will be used by an automated system to improve the paper, so be specific and actionable."""

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

        self.output_format = """# Scratch Work
[Think through the entire framework's strengths, weaknesses, and opportunities]

# Abstract Analysis
[Evaluate the abstract text itself]
- Clarity and engagement
- Scope and focus
- Literature positioning
- Key claims and preview

# Framework Components Analysis
## Main Thesis
- Clarity
- Alignment with abstract
- Suggested refinements

## Core Contribution
- Clarity
- Distinctiveness
- Alignment with abstract
- Suggested refinements

## Key Moves
- Feasibility
- Logical progression
- Alignment with abstract
- Suggested refinements

## Development Notes
- Feasibility assessment
- Resource requirements
- Potential challenges
- Suggested refinements

# Validation Assessment
- Scope appropriate: [yes/no + rationale]
- Clearly articulated: [yes/no + rationale]
- Sufficiently original: [yes/no + rationale]
- Feasibly developable: [yes/no + rationale]

# Improvement Recommendations
[Specific suggestions for enhancing both abstract and framework components]

# Summary Assessment
MAJOR REVISION [if components need significant realignment]
MINOR REFINEMENT [if components need small adjustments]
MINIMAL CHANGES [if components are well-aligned and effective]"""

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
The system has already processed literature (Phase II.1) and will use your critique to improve the framework.
Your critique must be genuine and rigorous - the pipeline depends on honest criticism to succeed.
{self.context}
</context>

<task>
Critically evaluate this abstract and framework for a 4000-word philosophy paper targeting the journal Analysis.
Identify specific weaknesses, gaps, and areas for improvement.
Consider how well the framework utilizes our available literature.
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
Provide your evaluation following this format:
{self.output_format}

Remember: Focus on how components can be strengthened while maintaining coherence across the framework. Consider both individual elements and their integration.
</requirements>"""

    def get_system_prompt(self) -> str:
        """Return the system prompt for API calls"""
        return self.system_prompt
