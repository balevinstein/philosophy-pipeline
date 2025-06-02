from typing import Any, Dict, Optional

from src.phases.phase_two.stages.stage_two.prompts.key_moves.key_moves_critic_prompts import (
    KeyMovesCriticPrompts,
)
from src.phases.phase_two.stages.stage_two.prompts.key_moves.key_moves_development_prompts import (
    KeyMovesDevelopmentPrompts,
)
from src.phases.phase_two.stages.stage_two.prompts.key_moves.key_moves_refinement_prompts import (
    KeyMovesRefinementPrompts,
)


class KeyMovesPrompts:
    """Prompts for key moves workflow"""

    def get_refinement_prompt(
        self,
        current_moves: Dict[str, Any],
        critique: Dict[str, Any],
        framework: Dict[str, Any],
        outline: str,
        lit_synthesis: Dict[str, Any],
    ) -> str:

        refinement_prompts = KeyMovesRefinementPrompts()
        return refinement_prompts.construct_prompt(
            current_moves=current_moves,
            critique=critique,
            framework=framework,
            outline=outline,
            lit_synthesis=lit_synthesis,
        )

    def get_development_argument_prompt(
        self, move: str, abstract: str, outline: str, prior_moves: Optional[Dict] = None
    ) -> str:
        development_prompts = KeyMovesDevelopmentPrompts()
        return development_prompts.construct_argument_prompt(
            move=move,
            abstract=abstract,
            outline=outline,
            prior_moves=prior_moves,
        )

    def get_development_challenges_prompt(
        self, move: str, argument_sketch: str, abstract: str, outline: str
    ) -> str:
        development_prompts = KeyMovesDevelopmentPrompts()
        return development_prompts.construct_challenges_prompt(
            move=move,
            argument_sketch=argument_sketch,
            abstract=abstract,
            outline=outline,
        )

    def get_critic_prompt(
        self,
        current_moves: Dict[str, Any],
        framework: Dict[str, Any],
        outline: str,
        lit_readings: Dict[str, Any],
        lit_synthesis: Dict[str, Any],
        lit_narrative: str,
    ) -> str:
        critic_prompts = KeyMovesCriticPrompts()
        return critic_prompts.construct_prompt(
            key_moves=current_moves,
            framework=framework,
            outline=outline,
            literature={
                "readings": lit_readings,
                "synthesis": lit_synthesis,
                "narrative": lit_narrative,
            },
        )
