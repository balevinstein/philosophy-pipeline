import json
import yaml
import os
from pathlib import Path
from src.phases.phase_two.stages.stage_two.workers.abstract_worker import AbstractDevelopmentWorker


def load_yaml(path: str) -> dict:
    """Load YAML file"""
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def load_json(path: str) -> dict:
    """Load JSON file"""
    with open(path, 'r') as f:
        return json.load(f)

def load_text(path: str) -> str:
    """Load text file"""
    with open(path, 'r') as f:
        return f.read()

def save_json(path: str, data: dict):
    """Save JSON file"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def test_abstract_development():
    """Test abstract generation and validation"""
    # Load test config using yaml
    config = load_yaml("tests/test_config.yaml")
    worker = AbstractDevelopmentWorker(config)
    
    # Load outputs from previous stages
    lit_readings = load_json("outputs/literature_readings.json")
    lit_synthesis = load_json("outputs/literature_synthesis.json")
    lit_synthesis_md = load_text("outputs/literature_synthesis.md")
    final_selection = load_json("outputs/final_selection.json")
    
    state = {
        "literature": {
            "readings": lit_readings,
            "synthesis": lit_synthesis,
            "narrative": lit_synthesis_md
        },
        "final_selection": final_selection
    }
    
    result = worker.run(state)
    
    # Save for review
    save_json("test_outputs/framework_development/abstract_test.json", result.modifications)
    
    print("\nGenerated Abstract:")
    print(result.modifications['abstract'])
    print("\nMain Thesis:")
    print(result.modifications['main_thesis'])
    print("\nKey Moves:")
    for i, move in enumerate(result.modifications['key_moves'], 1):
        print(f"{i}. {move}")
    print("\nValidation Status:")
    print(json.dumps(result.modifications['validation_status'], indent=2))

if __name__ == "__main__":
    test_abstract_development()