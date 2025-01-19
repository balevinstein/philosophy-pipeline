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
        workflow_name="abstract",
        max_cycles=3,
        initial_step=WorkflowStep(
            worker=AbstractDevelopmentWorker(config),
            input_mapping={
                "literature": "literature",
                "final_selection": "final_selection",
            },
            output_mapping={
                "current_framework": "modifications",
                "output_versions": "modifications",
            },
            name="development",
            has_output_version=True,
        ),
        cycle_steps=[
            WorkflowStep(
                worker=AbstractCriticWorker(config),
                input_mapping={
                    "current_framework": "current_framework",
                    "literature": "literature",
                },
                output_mapping={"current_critique": "modifications"},
                name="critique",
                has_output_version=False,
            ),
            WorkflowStep(
                worker=AbstractRefinementWorker(config),
                input_mapping={
                    "current_critique": "current_critique",
                    "current_framework": "current_framework",
                    "literature": "literature",
                },
                output_mapping={
                    "current_refinment": "modifications",
                    "current_framework": "framework_data",
                    "output_versions": "framework_data",
                },
                name="refinment",
                has_output_version=True,
            ),
        ],
        output_dir=output_dir,
    )
