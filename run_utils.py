import json
import logging
import os
import subprocess
from typing import Any, Dict
from pathlib import Path
import yaml

import requests


def load_config() -> Dict[str, Any]:
    """Load configuration from config/conceptual_config.yaml"""
    config_path = Path("config/conceptual_config.yaml")
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def ensure_output_dir(dir_path: str) -> Path:
    """Ensure output directory exists and return Path object"""
    path = Path(dir_path)
    path.mkdir(parents=True, exist_ok=True)
    return path


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


def load_developed_key_moves() -> Dict[str, Any]:
    """Load Developed key moves"""
    try:
        with open(
            "./outputs/key_moves_development/key_moves_development/all_developed_moves.json"
        ) as f:
            return json.load(f)["developed_moves"]
    except FileNotFoundError:
        raise ValueError("Could not find all_developed_json.json.")


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


def load_developed_moves() -> Dict[str, Any]:
    """Load all developed key moves"""
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


def setup_logging():
    """Configure logging"""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def check_rivet_life() -> Dict[str, Any]:
    """Check if Rivet server is up"""
    try:
        result = requests.get("http://localhost:4040/life", timeout=5000)
        if result.ok:
            print("Rivet alive")
    except ConnectionError:
        raise ValueError(
            "Could not connect to the Rivet server. Please run `node ./rivet/app.js --watch` in another terminal process"
        )