import json
import yaml
import os
from pathlib import Path
from src.stages.phase_two.stages.stage_two.workers.abstract_critic import AbstractCritic

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

def test_abstract_critic():
    """Test abstract criticism"""
    config = load_yaml("tests/test_config.yaml")
    worker = AbstractCritic(config)
    
    # Load abstract and literature context
    abstract_result = load_json("test_outputs/framework_development/abstract_test.json")
    lit_readings = load_json("outputs/literature_readings.json")
    lit_synthesis = load_json("outputs/literature_synthesis.json")
    lit_synthesis_md = load_text("outputs/literature_synthesis.md")
    
    state = {
        "current_abstract": abstract_result,
        "literature": {
            "readings": lit_readings,
            "synthesis": lit_synthesis,
            "narrative": lit_synthesis_md
        }
    }
    
    result = worker.run(state)
    
    # Save JSON output
    save_json("test_outputs/framework_development/critique_test.json", 
             {"critique": result.modifications})
             
    # Save markdown content
    critique_md_path = os.path.join("test_outputs", "framework_development", "critique_test.md")
    os.makedirs(os.path.dirname(critique_md_path), exist_ok=True)
    with open(critique_md_path, "w") as f:
        f.write(result.modifications["content"])
    
    print("\nCritique Analysis:")
    print(result.modifications["content"])
    print("\nSummary Assessment:")
    print(result.notes["summary_assessment"])

if __name__ == "__main__":
    test_abstract_critic()