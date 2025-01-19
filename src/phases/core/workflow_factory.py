from typing import Dict, Any
from pathlib import Path
from .workflow import Workflow, WorkflowStep
from .worker_types import DevelopmentWorker, CriticWorker, RefinementWorker


def create_workflow(
    development_worker: DevelopmentWorker,
    critic_worker: CriticWorker,
    refinement_worker: RefinementWorker,
    output_dir: Path,
    config: Dict[str, Any],
) -> Workflow:
    """Creates a standard development workflow with development, critique, and refinement steps"""

    steps = [
        WorkflowStep(
            worker=development_worker,
            name="development",
            input_mapping={
                "literature": "literature",
                "framework": "framework",
                "outline": "outline",
            },
            output_mapping={
                "content": "result.content",
                "development": "result.development",
            },
        ),
        WorkflowStep(
            worker=critic_worker,
            name="critique",
            input_mapping={
                "content": "content",
                "development": "development",
                "framework": "framework",
                "literature": "literature",
            },
            output_mapping={
                "critique": "result.critique",
                "assessment": "result.assessment",
            },
        ),
        WorkflowStep(
            worker=refinement_worker,
            name="refinement",
            input_mapping={
                "content": "content",
                "critique": "critique",
                "framework": "framework",
                "literature": "literature",
            },
            output_mapping={
                "refined_content": "result.content",
                "refinements": "result.refinements",
            },
        ),
    ]

    return Workflow(
        steps=steps,
        output_dir=output_dir,
        max_cycles=config["parameters"]["development_cycles"]["num_cycles"],
    )
