from pathlib import Path
from typing import Dict, Any

from src.phases.core.workflow import Workflow, WorkflowStep
from src.phases.phase_two.stages.stage_two.workers.critic.key_moves_critic import (
    KeyMovesCriticWorker,
)
from src.phases.phase_two.stages.stage_two.workers.development.key_moves_development import (
    KeyMovesDevelopmentWorker,
)
from src.phases.phase_two.stages.stage_two.workers.refinement.key_moves_refinement import (
    KeyMovesRefinementWorker,
)


# Rules for writing workflow steps
# modifications is the output of a step, if you want the whole output to be copied, use modifications on the right side of mapping
# output_versions is a list that keeps track of the all the versions of an output,
# the output version will always be updated by the whole object you provide it, so mutate your object to match the final output
# refer to the code in core/workflow.py/_update_state


def create_key_moves_workflow(
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
            worker=KeyMovesDevelopmentWorker(config),
            input_mapping={
                "framework": "framework",
                "outline": "outline",
                "literature": "literature",
            },
            output_mapping={
                "current_moves": "content",
                "output_versions": "content",
            },
            name="development",
        ),
        cycle_steps=[
            WorkflowStep(
                worker=KeyMovesCriticWorker(config),
                input_mapping={
                    "current_moves": "current_moves",
                    "literature": "literature",
                    "outline": "outline",
                    "framework": "framework",
                },
                output_mapping={"current_critique": "modifications"},
                name="critique",
            ),
            WorkflowStep(
                worker=KeyMovesRefinementWorker(config),
                input_mapping={
                    "current_moves": "current_moves",
                    "current_critique": "current_critique",
                    "previous_versions": "current_moves",
                    "outline": "outline",
                    "framework": "framework",
                    "literature": "literature",
                },
                output_mapping={
                    "current_refinement": "modifications",
                    "current_moves": "modifications",
                    "output_versions": "modifications",
                },
                name="refinement",
            ),
        ],
        output_dir=output_dir,
    )
