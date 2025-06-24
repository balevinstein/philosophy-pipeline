import json
from typing import Dict, Any
from src.utils.prompt_utils import load_and_combine_style_guides

class QuickSynthesisPrompts:
    """Prompts for Phase II.5a Quick Synthesis - lightweight coherence check"""

    def __init__(self):
        style_guide = load_and_combine_style_guides()
        self.system_prompt = f"""{style_guide}
        
You are a senior philosophy editor conducting a quick coherence check of paper materials. Your job is to synthesize outputs from previous phases and identify major issues that would prevent publication. You focus on big-picture problems, not detailed critique."""

    def get_synthesis_prompt(
        self,
        abstract_framework: str,
        developed_moves: str,
        detailed_outline: str
    ) -> str:
        return f"""<task>
You are conducting a quick synthesis of Phase II outputs to identify major coherence issues and set priorities for refinement phases. Focus on BIG PICTURE problems that would kill the paper, not detailed critique.
</task>

<current_priorities>
Your main focus: Does this paper hang together as a coherent philosophical project?
Secondary: What are the 3-5 most serious issues that need fixing?
Don't worry about: Detailed quality standards, specific citations, minor improvements
</current_priorities>

<coherence_check_framework>
## 1. BASIC COHERENCE
- Do thesis, moves, and outline work together toward the same goal?
- Are there major contradictions between components?
- Does the paper have a clear philosophical story?

## 2. MAJOR ISSUE IDENTIFICATION  
- What would make a hostile reviewer reject this immediately?
- Which problems are "paper killers" vs. fixable issues?
- What needs attention before detailed refinement?

## 3. REFINEMENT PRIORITIES
- What should II.6-8 focus on first?
- Which issues are most urgent vs. can wait?
- What's the overall state of the project?
</coherence_check_framework>

<inputs>
ABSTRACT & FRAMEWORK:
{abstract_framework}

DEVELOPED MOVES:
{developed_moves}

DETAILED OUTLINE:
{detailed_outline}
</inputs>

<output_format>
{{
    "coherence_assessment": {{
        "overall_coherence": "strong/acceptable/problematic/incoherent",
        "main_story": "What is this paper actually about in 2-3 sentences?",
        "thesis_move_alignment": "Do the key moves clearly support the thesis?",
        "major_contradictions": ["List any serious contradictions found"]
    }},
    "priority_issues": [
        {{
            "issue": "Brief description of major problem",
            "severity": "critical/major/moderate",
            "impact": "Why this matters for the paper",
            "urgency": "fix_first/address_soon/can_wait"
        }}
    ],
    "refinement_guidance": {{
        "immediate_priorities": ["Top 3 things to fix first"],
        "paper_readiness": "far_from_ready/needs_work/nearly_ready",
        "main_strengths": ["What's working well"],
        "next_steps": "High-level guidance for II.6-8 stages"
    }}
}}
</output_format>

<success_criteria>
Success = You've identified the 3-5 most important issues that would prevent publication and given clear direction for fixing them. You're NOT trying to catch every problem - just the big ones.
</success_criteria>"""

    def get_system_prompt(self) -> str:
        return self.system_prompt 