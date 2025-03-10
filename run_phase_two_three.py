import logging
import os
from pathlib import Path
import subprocess
from typing import Any, Dict
import json
import datetime

from src.phases.phase_two.stages.stage_three.workflows.master_workflow import (
    process_all_key_moves,
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


def load_key_moves() -> Dict[str, Any]:
    """Load key moves"""
    try:
        with open("./outputs/framework_development/key_moves.json") as f:
            return json.load(f)["key_moves"]
    except FileNotFoundError:
        raise ValueError("Could not find key_moves.json.")


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
    """Main execution for Phase II.3: Key Moves Development"""
    print("Starting Phase II.3: Key Moves Development")
    setup_logging()

    # Prevent sleep during execution
    caffeinate()

    # Load configuration and inputs
    config = load_config()

    # Setup output directory
    key_moves_dev_dir = Path("./outputs/key_moves_development")
    key_moves_dev_dir.mkdir(exist_ok=True)

    # Load required data
    framework = load_framework()
    outline = load_outline()
    key_moves = load_key_moves()
    literature = load_literature()
    
    print(f"Processing {len(framework.get('key_moves', []))} key moves...")

    # Process all key moves
    developed_moves = process_all_key_moves(
        config=config,
        output_dir=key_moves_dev_dir,
        framework=framework,
        outline=outline,
        key_moves=key_moves,
        literature=literature,
    )

    print(f"Completed development of {len(developed_moves)} key moves")
    print(f"Output saved to {key_moves_dev_dir}/all_developed_moves.json")
    print(f"Human-readable version saved to {key_moves_dev_dir}/all_developed_moves.md")

    return


if __name__ == "__main__":
    main() 