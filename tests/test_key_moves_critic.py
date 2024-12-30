# tests/test_key_moves_critic.py

import json
import yaml
import os
from pathlib import Path
from src.stages.phase_two.stages.stage_two.workers.key_moves_critic import KeyMovesCritic

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

def test_key_moves_critic():
    """Test key moves criticism"""
    config = load_yaml("tests/test_config.yaml")
    worker = KeyMovesCritic(config)
    
    # Load final framework from abstract refinement
    refinements_dir = os.path.join("test_outputs", "framework_development", "refinements")
    cycles = [d for d in os.listdir(refinements_dir) if d.startswith("cycle_")]
    final_cycle = max(int(cycle.split("_")[1]) for cycle in cycles)
    framework = load_json(os.path.join(refinements_dir, f"cycle_{final_cycle}", "framework.json"))["framework"]

    # Load final outline
    outline_dir = os.path.join("test_outputs", "framework_development", "outline_development")
    cycles = [d for d in os.listdir(outline_dir) if d.startswith("cycle_")]
    final_cycle = max(int(cycle.split("_")[1]) for cycle in cycles)
    final_outline = load_json(os.path.join(outline_dir, f"cycle_{final_cycle}", "refinement.json"))["refinement"]["outline"]

    # Load key moves analysis
    key_moves = load_json("test_outputs/framework_development/key_moves_test.json")["key_moves_analysis"]
    
    # Load literature context
    lit_readings = load_json("outputs/literature_readings.json")
    lit_synthesis = load_json("outputs/literature_synthesis.json")
    lit_synthesis_md = load_text("outputs/literature_synthesis.md")
    
    state = {
        "framework": framework,
        "outline": final_outline,
        "key_moves_analysis": key_moves,
        "literature": {
            "readings": lit_readings,
            "synthesis": lit_synthesis,
            "narrative": lit_synthesis_md
        }
    }
    
    # Run critique
    print("\nRunning key moves critique...")
    result = worker.run(state)
    
    # Save results
    output_path = "test_outputs/framework_development/key_moves_critique.json"
    save_json(output_path, {
        "critique": result.modifications
    })
    
    # Also save markdown for readability
    md_path = "test_outputs/framework_development/key_moves_critique.md"
    with open(md_path, "w") as f:
        f.write(result.modifications["content"])
    
    print("\nKey Moves Critique Summary:")
    print(f"Overall Assessment: {result.modifications['summary']}")
    
    print("\nKey Recommendations from Summary:")
    print(result.modifications["sections"]["Summary Assessment"])
    
    print("\nPer-Move Assessments:")
    move_analysis = result.modifications["sections"]["Move Analysis"]
    for line in move_analysis.split("\n"):
        if line.startswith("## Move") and "REFINEMENT" in line.upper():
            print(line.strip())
    
    print("\nFull critique saved to:")
    print(f"- {output_path}")
    print(f"- {md_path}")
    
if __name__ == "__main__":
    test_key_moves_critic()