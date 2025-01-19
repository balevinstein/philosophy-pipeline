from pathlib import Path
from typing import Dict, Any

from src.phases.core.workflow import Workflow, WorkflowStep

from src.phases.phase_two.stages.stage_two.workers.critic.abstract_critic import (
    AbstractCriticWorker,
)
from src.phases.phase_two.stages.stage_two.workers.development.abstract_development import (
    AbstractDevelopmentWorker,
)
from src.phases.phase_two.stages.stage_two.workers.refinement.abstract_refinement import (
    AbstractRefinementWorker,
)


def create_abstract_workflow(config: Dict[str, Any], output_dir: Path) -> Workflow:
    """Create workflows"""
    return Workflow(
        initial_step=WorkflowStep(
            worker=AbstractDevelopmentWorker(config),
            input_mapping={
                "literature": "literature",
                "final_selection": "final_selection",
            },
            output_mapping={
                "abstract": "result.abstract",
                "framework": "result.framework",
            },
            name="development",
        ),
        cycle_steps=[
            WorkflowStep(
                worker=AbstractCriticWorker(config),
                input_mapping={
                    "abstract": "abstract",
                    "framework": "framework",
                    "literature": "literature",
                },
                output_mapping={"critique": "result.critique"},
                name="critique",
            ),
            WorkflowStep(
                worker=AbstractRefinementWorker(config),
                input_mapping={
                    "current_version": "abstract",
                    "critique": "critique",
                    "framework": "framework",
                    "literature": "literature",
                },
                output_mapping={
                    "refined_abstract": "result.abstract",
                    "refined_framework": "result.framework",
                },
                name="refinment",
            ),
        ],
        output_dir=output_dir,
    )
