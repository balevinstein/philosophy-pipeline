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


# Rules for writing workflow steps
# modifications is the output of a step, if you want the whole output to be copied, use modifications on the right side of mapping
# output_versions is a list that keeps track of the all the versions of an output,
# the output version will always be updated by the whole object you provide it, so mutate your object to match the final output
# refer to the code in core/workflow.py/_update_state


def create_abstract_framework_workflow(
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
            ),
            WorkflowStep(
                worker=AbstractRefinementWorker(config),
                input_mapping={
                    "current_critique": "current_critique",
                    "current_framework": "current_framework",
                    "previous_versions": "current_framework",
                    "literature": "literature",
                },
                output_mapping={
                    "current_refinement": "modifications",
                    "current_framework": "framework_data",
                    "output_versions": "framework_data",
                },
                name="refinement",
            ),
        ],
        output_dir=output_dir,
    )
