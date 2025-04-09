import os
from pathlib import Path
import subprocess


from run_utils import (
    load_final_selection,
    load_framework,
    load_literature,
    load_outline,
    setup_logging,
)
from src.phases.phase_two.stages.stage_two.workflows.abstract_workflow import (
    create_abstract_framework_workflow,
)
from src.phases.phase_two.stages.stage_two.workflows.key_moves_workflow import (
    create_key_moves_workflow,
)
from src.phases.phase_two.stages.stage_two.workflows.outline_workflow import (
    create_outline_workflow,
)
from src.utils.api import load_config


def main():
    """Main execution for Phase 2"""
    print("Starting Phase II.2: Framework Development")
    setup_logging()

    # Prevent sleep during execution
    subprocess.Popen(["caffeinate", "-i", "-w", str(os.getpid())])

    # Load configuration and inputs
    config = load_config()

    # Setup output directory
    framework_dev_dir = Path("./outputs/framework_development")
    framework_dev_dir.mkdir(exist_ok=True)

    final_selection = load_final_selection()
    literature = load_literature()

    abstract_initial_state = {
        "final_selection": final_selection,
        "literature": literature,
    }

    # Create and run workflows

    # Abstract Workflow
    abstract_framework_workflow = create_abstract_framework_workflow(
        config,
        output_dir=framework_dev_dir,
        workflow_name="abstract_framework",
        max_cycles=3,
    )

    abstract_framework_workflow.execute(abstract_initial_state)

    framework = load_framework()

    # Outline Workflow
    outline_initial_state = {"framework": framework, "literature": literature}
    outline_workflow = create_outline_workflow(
        config, output_dir=framework_dev_dir, workflow_name="outline", max_cycles=3
    )

    outline = outline_workflow.execute(outline_initial_state)

    outline = load_outline()

    key_moves_initial_state = {
        "outline": outline,
        "framework": framework,
        "literature": literature,
    }

    # Key Moves Workflow
    key_moves_workflow = create_key_moves_workflow(
        config, output_dir=framework_dev_dir, workflow_name="key_moves", max_cycles=3
    )

    key_moves_workflow.execute(key_moves_initial_state)

    return


if __name__ == "__main__":
    main()
