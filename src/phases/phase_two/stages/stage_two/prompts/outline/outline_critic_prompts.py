from typing import Dict
import json


class OutlineCriticPrompts:
    """Prompts for critiquing outline and suggesting improvements"""

    def __init__(self):
        self.system_prompt = """You are a rigorous philosophy journal reviewer evaluating a paper outline. Your role is to provide genuinely critical analysis of the structural blueprint. Do not be polite or deferential. Be constructive but skeptical. Your critique will be used by an automated system to improve the outline, so be specific and actionable."""

        self.context = """You are critiquing an initial high-level outline for a paper to be published in Analysis (4,000 word limit).
This outline focuses on main sections and key structural elements - more detailed section development will occur in later stages.

The paper will be written by AI models that:
- Have access to the specific papers provided in our literature analysis
- Cannot freely access additional academic literature
- Must develop arguments without extensive citation requirements

Your task is to evaluate whether the outline's structure:
1. Provides appropriate scaffolding for developing the framework (abstract, thesis, key moves)
2. Creates a logical progression for argument development
3. Maintains feasibility within the 4,000-word constraint
4. Enables appropriate literature engagement

While detailed word allocation will come later, consider that a 4,000 word paper typically needs space for introduction, core argument development, and conclusion while maintaining appropriate balance across sections.

Take time to think through different aspects before providing your assessment."""

        self.output_format = """# Scratch Work
[Think through the outline's strengths, weaknesses, and opportunities]

# Framework Alignment Analysis
- How well sections support key moves
- Where thesis/abstract elements are developed
- Coverage of core concepts and arguments
- Space for methodology development
- Support for main claims

# Structural Analysis
- Section flow and progression
- Balance and proportions
- Development dependencies
- Argument building
- Introduction of concepts/tools
- Treatment of objections/counterexamples

# Feasibility Assessment
- Section scope evaluation
- Space allocation
- Development requirements
- Word count considerations
- Resource requirements

# Literature Integration
- Engagement opportunities
- Use of available sources
- Coverage balance
- Support for key claims

# Red Flags
- Sections that seem too ambitious for word count
- Places where literature support might be insufficient
- Dependencies that could cause development problems
- Structural issues that could impede argument flow
- Coverage gaps for key framework elements

# Specific Recommendations
[Concrete suggestions for improving the outline]

# Summary Assessment
MAJOR REVISION [if structure needs significant rework]
MINOR REFINEMENT [if structure needs small adjustments]
MINIMAL CHANGES [if structure is fundamentally sound]"""

    def construct_prompt(
        self,
        outline: str,
        framework: Dict,
        lit_readings: Dict,
        lit_synthesis: Dict,
        lit_narrative: str,
    ) -> str:
        """Generate prompt for outline critique"""
        return f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.2 (Framework Development).
The system has created an initial outline based on the abstract and framework.
Your critique will guide outline refinement before detailed development begins.
{self.context}
</context>

<task>
Critically evaluate this outline for structural soundness and framework alignment.
Identify specific weaknesses in the organizational structure.
Consider feasibility within the 4000-word constraint.
</task>

<current_framework>
Current Framework Development:
{json.dumps(framework, indent=2)}
</current_framework>

<current_outline>
Current Outline:
{outline}
</current_outline>

<literature_context>
Literature Context:
1. Paper Readings:
{json.dumps(lit_readings, indent=2)}

2. Literature Synthesis:
{json.dumps(lit_synthesis, indent=2)}

3. Synthesis Narrative:
{lit_narrative}
</literature_context>

<requirements>
Provide your evaluation following this format:
{self.output_format}

Remember to think carefully about how the outline can best support development of the framework while maintaining feasibility and coherence. Consider both high-level structure and essential development requirements.
</requirements>"""

    def get_system_prompt(self) -> str:
        """Return the system prompt for API calls"""
        return self.system_prompt
