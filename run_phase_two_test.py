import logging
import os
from pathlib import Path
import subprocess
from typing import Any, Dict
import json


from src.phases.phase_two.stages.stage_two.workflows.abstract.abstract_workflow import (
    create_abstract_workflow,
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

    # Prevent sleep during execution
    subprocess.Popen(["caffeinate", "-i", "-w", str(os.getpid())])

    # Load configuration and inputs
    config = load_config()
    final_selection = load_final_selection()
    literature = load_literature()

    # Setup output directory
    framework_dir = Path("./outputs/framework_development")
    framework_dir.mkdir(exist_ok=True)

    # Initial state
    state = {"final_selection": final_selection, "literature": literature}

    # Create and run workflows
    abstract_workflow = create_abstract_workflow(config, output_dir=framework_dir)
    abstract_state = abstract_workflow.execute(state)


if __name__ == "__main__":
    main()
