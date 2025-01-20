import logging
import os
from pathlib import Path
import subprocess
from typing import Any, Dict
import json


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


def setup_logging():
    """Configure logging"""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def load_final_selection() -> Dict[str, Any]:
    """Load final selection from Phase I"""
    try:
        with open("./outputs/final_selection.json") as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValueError("Could not find final_selection.json. Run Phase I first.")


def load_framework() -> Dict[str, Any]:
    """Load framework"""
    try:
        with open("./outputs/framework_development/abstract_framework.json") as f:
            return json.load(f)["abstract_framework"]
    except FileNotFoundError:
        raise ValueError("Could not find abstract_framework.json.")


def load_outline() -> Dict[str, Any]:
    """Load outline"""
    try:
        with open("./outputs/framework_development/outline.json") as f:
            return json.load(f)["outline"]
    except FileNotFoundError:
        raise ValueError("Could not find outline.json.")


def load_literature() -> Dict[str, Any]:
    """Load literature analysis from Phase II.1"""
    try:
        lit_readings = json.load(open("./outputs/literature_readings.json"))
        lit_synthesis = json.load(open("./outputs/literature_synthesis.json"))
        with open("./outputs/literature_synthesis.md") as f:
            lit_narrative = f.read()
        return {
            "readings": lit_readings,
            "synthesis": lit_synthesis,
            "narrative": lit_narrative,
        }
    except FileNotFoundError as e:
        raise ValueError(f"Missing literature files. Run Phase II.1 first. Error: {e}")


def caffeinate():
    """Prevent system sleep during execution"""
    try:
        subprocess.Popen(["caffeinate", "-i", "-w", str(os.getpid())])
    except Exception as e:
        print(f"Warning: Could not caffeinate process: {e}")
        print(
            "You may want to manually prevent your system from sleeping during execution."
        )


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
