import json
from typing import Dict, Any, List
from src.utils.prompt_utils import load_and_combine_style_guides

class QualityAuditPrompts:
    """Prompts for Phase II.5b Targeted Quality Audit - focused quality standards application"""

    def __init__(self):
        style_guide = load_and_combine_style_guides()
        self.system_prompt = f"""{style_guide}
        
You are a philosophy journal editor conducting a targeted quality audit. Based on a preliminary synthesis, you apply quality standards systematically to priority issues. You focus on actionable problems that refinement stages can fix."""

        # Streamlined quality standards - focus on most important
        self.key_quality_checks = """
<targeted_quality_standards>
Apply these selectively based on synthesis priorities:

1. HÁJEK SPOT CHECKS: Test priority arguments for:
   - Extreme case vulnerabilities
   - Self-undermining potential  
   - Hidden controversial assumptions

2. ANTI-RLHF AUDIT: Flag major instances of:
   - Hedging instead of position-taking
   - Survey style instead of argument
   - False balance undermining thesis

3. ANALYSIS STYLE CHECK: Verify compliance with:
   - Thesis statement clarity 
   - Concrete examples supporting abstract claims
   - Conversational directness
</targeted_quality_standards>"""

    def get_audit_prompt(
        self,
        synthesis_results: Dict[str, Any],
        abstract_framework: str,
        key_moves: str,
        outline_sections: str
    ) -> str:
        return f"""<task>
Conduct a targeted quality audit based on synthesis results. Focus on the priority issues identified and apply quality standards systematically to those areas. Provide specific, actionable remediation guidance for II.6-8.
</task>

<synthesis_results>
The preliminary synthesis identified these priorities:
{json.dumps(synthesis_results, indent=2)}
</synthesis_results>

{self.key_quality_checks}

<current_priorities>
Primary: Address the priority issues from synthesis
Secondary: Apply quality standards to those specific areas
Tertiary: Generate actionable fixes for II.6-8
Don't overextend: Focus on synthesis priorities, not comprehensive audit
</current_priorities>

<audit_framework>
## 1. PRIORITY ISSUE ANALYSIS
For each priority issue from synthesis:
- Apply relevant quality standards
- Identify specific violations
- Generate targeted fixes

## 2. TARGETED REMEDIATION PLANNING
- What should II.6 (Planning) focus on?
- What needs II.7 (Refinement) attention?
- What requires II.8 (Writing) optimization?

## 3. IMPLEMENTATION GUIDANCE
- Specific quotes/locations of problems
- Clear fix descriptions
- Priority ordering for refinement stages
</audit_framework>

<inputs>
ABSTRACT & FRAMEWORK:
{abstract_framework}

KEY MOVES (focus areas):
{key_moves}

OUTLINE SECTIONS (problem areas):
{outline_sections}
</inputs>

<output_format>
{{
    "priority_analysis": [
        {{
            "issue_from_synthesis": "Issue identified in synthesis",
            "quality_violations": [
                {{
                    "standard": "HAJEK/ANTI_RLHF/ANALYSIS_STYLE",
                    "specific_problem": "Exact quote or location",
                    "violation_type": "Description of what's wrong",
                    "severity": "critical/major/moderate"
                }}
            ],
            "targeted_fixes": [
                {{
                    "fix_description": "Specific action needed",
                    "implementation_stage": "II.6_planning/II.7_refinement/II.8_writing",
                    "priority": "urgent/important/helpful"
                }}
            ]
        }}
    ],
    "refinement_roadmap": {{
        "stage_6_planning_focus": ["What revision planning should prioritize"],
        "stage_7_refinement_targets": ["Specific moves/sections needing refinement"],
        "stage_8_writing_optimization": ["Writing issues to address"],
        "overall_difficulty": "easy/moderate/challenging"
    }},
    "implementation_details": {{
        "urgent_fixes": ["Must fix before proceeding"],
        "important_improvements": ["Should fix for quality"],
        "optional_enhancements": ["Nice to have but not essential"],
        "estimated_effort": "How much work this represents"
    }}
}}
</output_format>

<success_criteria>
Success = You've provided specific, actionable guidance for fixing the priority issues identified in synthesis. II.6-8 stages should know exactly what to work on and how to approach it.
</success_criteria>"""

    def get_system_prompt(self) -> str:
        return self.system_prompt 