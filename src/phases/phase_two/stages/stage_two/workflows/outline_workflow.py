from pathlib import Path
from typing import Dict, Any

from src.phases.core.workflow import Workflow, WorkflowStep
from src.phases.phase_two.stages.stage_two.workers.critic.outline_critic import (
    OutlineCriticWorker,
)
from src.phases.phase_two.stages.stage_two.workers.development.outline_development import (
    OutlineDevelopmentWorker,
)
from src.phases.phase_two.stages.stage_two.workers.refinement.outline_refinement import (
    OutlineRefinementWorker,
)


# Rules for writing workflow steps
# modifications is the output of a step, if you want the whole output to be copied, use modifications on the right side of mapping
# output_versions is a list that keeps track of the all the versions of an output,
# the output version will always be updated by the whole object you provide it, so mutate your object to match the final output
# refer to the code in core/workflow.py/_update_state


def create_outline_workflow(
    config: Dict[str, Any],
    output_dir: Path,
    workflow_name: str,
    max_cycles=3,
) -> Workflow:
    """Create workflows"""
    return Workflow(
        workflow_name=workflow_name,
        max_cycles=max_cycles,
        initial_step=WorkflowStep(
            worker=OutlineDevelopmentWorker(config),
            input_mapping={
                "literature": "literature",
                "framework": "framework",
            },
            output_mapping={
                "current_outline": "current_outline",
                "output_versions": "current_outline",
            },
            name="development",
        ),
        cycle_steps=[
            WorkflowStep(
                worker=OutlineCriticWorker(config),
                input_mapping={
                    "current_outline": "current_outline",
                    "framework": "framework",
                    "literature": "literature",
                },
                output_mapping={"current_critique": "modifications"},
                name="critique",
            ),
            WorkflowStep(
                worker=OutlineRefinementWorker(config),
                input_mapping={
                    "current_outline": "current_outline",
                    "current_critique": "current_critique",
                    "previous_versions": "current_outline",
                    "framework": "framework",
                    "literature": "literature",
                },
                output_mapping={
                    "current_refinement": "modifications",
                    "output_versions": "modifications",
                },
                name="refinement",
            ),
        ],
        output_dir=output_dir,
    )
