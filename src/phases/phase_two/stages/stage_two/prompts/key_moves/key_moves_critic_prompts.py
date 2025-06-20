from typing import Dict, List


class KeyMovesCriticPrompts:
    """Prompts for critiquing developed key moves"""

    def __init__(self):
        self.system_prompt = """You are a rigorous philosophy journal reviewer evaluating key argumentative moves. Your role is to provide genuinely critical analysis of the arguments' strength and feasibility. Do not be polite or deferential. Be constructive but skeptical. Your critique will guide refinement in an automated system."""

    def construct_prompt(
        self,
        key_moves: List[Dict],
        framework: Dict,
        outline: str,
        literature: Dict,
    ) -> str:
        context = f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.2 (Framework Development).
The system has developed initial versions of key argumentative moves.
Your critique will guide refinement before detailed paper development.

You are critiquing the developed key moves for our Analysis paper (4,000 word limit).
The paper will be written by AI models that have access to specific literature but cannot freely access additional sources.

Your task is to evaluate:
1. Each move's philosophical strength
2. Coherence with the framework  
3. Feasibility of development
4. Integration with other moves
5. Overall contribution to the thesis
</context>

<task>
Critically evaluate the developed key moves.
Identify specific weaknesses in arguments and examples.
Consider feasibility within the paper's constraints.
Assess how well moves work together to support the thesis.
</task>

<hájek_heuristics>
For EACH key move, apply these philosophical rigor tests:
- EXTREME CASE TEST: Does this move handle boundary cases?
- SELF-UNDERMINING CHECK: Does the move defeat itself when applied reflexively?
- COUNTEREXAMPLE GENERATION: What obvious objection would a grad student raise?
- HIDDEN ASSUMPTIONS: What controversial premises are smuggled in?
- DOMAIN TRANSFER: Would this reasoning work in parallel contexts?
</hájek_heuristics>

<framework>
Paper Framework:
{framework}

Paper Structure:
{outline}

Available Literature:
{literature}

Developed Key Moves:
{key_moves}
</framework>

<thinking>
Take time to think through the moves both individually and as a coherent whole.
Consider how effectively they advance the thesis and whether they can be developed within constraints.
</thinking>

<output_format>
# Scratch Work
[Think through the strengths and weaknesses of each move]
[Consider how moves work together]
[Evaluate feasibility and development challenges]

# Individual Move Analysis
[For each move, provide:]
## Move [Number]: [Brief description]
### Strengths
- [What works well about this move]

### Weaknesses  
- [Specific problems with the argument]
- [Issues with examples or development]
- [Integration concerns]

### Feasibility Issues
- [Challenges in developing this within word count]
- [Missing elements or dependencies]

### Recommendation
[Keep as is / Minor refinement needed / Major revision needed / Replace entirely]

# Overall Assessment
## Integration Analysis
- How well do the moves work together?
- Are there gaps in the argumentative progression?
- Do moves contradict or undermine each other?

## Framework Alignment
- Do the moves effectively support the thesis?
- Is the core contribution adequately developed?
- Are all abstract promises fulfilled?

## Critical Gaps
[List any major missing elements or underdeveloped areas]

# Summary Recommendation
ACCEPT AS IS [if moves are strong and well-integrated - rare]
MINOR REFINEMENTS [if moves need small improvements]
MAJOR REVISIONS [if significant changes needed]
FUNDAMENTAL REWORK [if moves fail to support framework]
</output_format>

<reminder>
Remember: Be genuinely critical. A paper gets rejected if its arguments are weak, its examples unconvincing, or its moves poorly integrated. Find these issues.
</reminder>"""

        return context

    def get_system_prompt(self) -> str:
        """Return the system prompt for API calls"""
        return self.system_prompt
