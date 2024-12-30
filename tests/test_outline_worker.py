import json
import yaml
import os
from pathlib import Path
from src.stages.phase_two.stages.stage_two.workers.outline_worker import OutlineWorker

def load_yaml(path: str) -> dict:
    """Load YAML file"""
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def load_json(path: str) -> dict:
    """Load JSON file"""
    with open(path, 'r') as f:
        return json.load(f)

def save_json(path: str, data: dict):
    """Save JSON file"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def test_outline_development():
    """Test outline generation and validation"""
    config = load_yaml("tests/test_config.yaml")
    worker = OutlineWorker(config)
    
    # Load abstract output
    abstract_result = load_json("test_outputs/framework_development/abstract_test.json")
    
    state = {
        "abstract_info": abstract_result
    }
    
    result = worker.run(state)
    
    # Save for review
    save_json("test_outputs/framework_development/outline_test.json", 
             {"outline": result.modifications["outline_content"],
              "development_notes": result.modifications["development_notes"],
              "scratch_work": result.modifications["scratch_work"]})
    
    print("\nGenerated Outline:")
    print(result.modifications["outline_content"])
    print("\nDevelopment Notes:")
    print(result.modifications["development_notes"])

if __name__ == "__main__":
    test_outline_development()