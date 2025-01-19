from typing import Any, Dict, List, Optional
from src.phases.phase_two.stages.stage_two.prompts.abstract.abstract_critic_prompts import (
    AbstractCriticPrompts,
)
from src.phases.phase_two.stages.stage_two.prompts.abstract.abstract_development_prompts import (
    AbstractDevelopmentPrompts,
)
from src.phases.phase_two.stages.stage_two.prompts.abstract.abstract_refinement_prompts import (
    AbstractRefinementPrompts,
)


class AbstractPrompts:
    """Prompts for abstract workflow"""

    def get_refinement_prompt(
        self,
        current_framework: Dict,
        critique: Dict,
        lit_synthesis: Dict,
        previous_versions: Optional[List[Dict]] = None,
    ) -> str:

        refinement_prompts = AbstractRefinementPrompts()
        return refinement_prompts.construct_prompt(
            current_framework=current_framework,
            critique=critique,
            lit_synthesis=lit_synthesis,
            previous_versions=previous_versions,
        )

    def get_development_prompt(self, lit_synthesis: dict, final_selection: dict) -> str:
        development_prompts = AbstractDevelopmentPrompts()
        return development_prompts.construct_prompt(lit_synthesis, final_selection)

    def get_critic_prompt(
        self,
        abstract_framework: Dict[str, Any],
        lit_readings: Dict[str, Any],
        lit_synthesis: Dict[str, Any],
        lit_narrative: str,
    ) -> str:
        critic_prompts = AbstractCriticPrompts()
        return critic_prompts.construct_prompt(
            abstract_framework=abstract_framework,
            lit_readings=lit_readings,
            lit_synthesis=lit_synthesis,
            lit_narrative=lit_narrative,
        )
