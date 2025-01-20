from typing import Dict

from src.phases.phase_two.stages.stage_two.prompts.outline.outline_critic_prompts import (
    OutlineCriticPrompts,
)
from src.phases.phase_two.stages.stage_two.prompts.outline.outline_development_prompts import (
    OutlineDevelopmentPrompts,
)
from src.phases.phase_two.stages.stage_two.prompts.outline.outline_refinement_prompts import (
    OutlineRefinementPrompts,
)


class OutlinePrompts:
    """Prompts for outline workflow"""

    def get_refinement_prompt(
        self,
        outline: str,
        critique: Dict,
        framework: Dict,
        lit_synthesis: Dict,
    ) -> str:

        refinement_prompts = OutlineRefinementPrompts()
        return refinement_prompts.construct_prompt(
            outline=outline,
            critique=critique,
            framework=framework,
            lit_synthesis=lit_synthesis,
        )

    def get_development_prompt(
        self, abstract: str, main_thesis: str, core_contribution: str, key_moves: list
    ) -> str:
        development_prompts = OutlineDevelopmentPrompts()
        return development_prompts.construct_prompt(
            abstract=abstract,
            main_thesis=main_thesis,
            core_contribution=core_contribution,
            key_moves=key_moves,
        )

    def get_critic_prompt(
        self,
        outline: str,
        framework: Dict,
        lit_readings: Dict,
        lit_synthesis: Dict,
        lit_narrative: str,
    ) -> str:
        critic_prompts = OutlineCriticPrompts()
        return critic_prompts.construct_prompt(
            outline=outline,
            framework=framework,
            lit_readings=lit_readings,
            lit_synthesis=lit_synthesis,
            lit_narrative=lit_narrative,
        )
