# tests/test_key_moves_cycle.py

import json
import yaml
import os
from pathlib import Path
from src.stages.phase_two.stages.stage_two.workers.key_moves_worker import KeyMovesWorker
from src.stages.phase_two.stages.stage_two.workers.key_moves_critic import KeyMovesCritic
from src.stages.phase_two.stages.stage_two.workers.key_moves_refinement_worker import KeyMovesRefinementWorker

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

def save_text(path: str, content: str):
    """Save text file"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

def test_key_moves_cycle():
    """Test complete key moves development cycle"""
    config = load_yaml("tests/test_config.yaml")
    
    # Load final refined framework
    refinements_dir = os.path.join("test_outputs", "framework_development", "refinements")
    cycles = [d for d in os.listdir(refinements_dir) if d.startswith("cycle_")]
    final_cycle = max(int(cycle.split("_")[1]) for cycle in cycles)
    framework = load_json(os.path.join(refinements_dir, f"cycle_{final_cycle}", "framework.json"))["framework"]

    # Load final refined outline
    outline_dir = os.path.join("test_outputs", "framework_development", "outline_development")
    cycles = [d for d in os.listdir(outline_dir) if d.startswith("cycle_")]
    final_cycle = max(int(cycle.split("_")[1]) for cycle in cycles)
    final_outline = load_json(os.path.join(outline_dir, f"cycle_{final_cycle}", "refinement.json"))["refinement"]["outline"]
    
    # Load literature context
    lit_readings = load_json("outputs/literature_readings.json")
    lit_synthesis = load_json("outputs/literature_synthesis.json")
    lit_synthesis_md = load_text("outputs/literature_synthesis.md")
    
    # Initialize workers
    moves_worker = KeyMovesWorker(config)
    critic = KeyMovesCritic(config)
    refinement_worker = KeyMovesRefinementWorker(config)
    
    # Create output directory
    moves_dir = os.path.join("test_outputs", "framework_development", "key_moves_development")
    os.makedirs(moves_dir, exist_ok=True)
    
    # Generate initial moves
    print("\nGenerating initial key moves analysis...")
    state = {
        "framework": framework,
        "outline": final_outline,
        "literature": {
            "readings": lit_readings,
            "synthesis": lit_synthesis,
            "narrative": lit_synthesis_md
        }
    }
    
    moves = moves_worker.run(state)
    save_text(os.path.join(moves_dir, "initial_moves.md"), moves.modifications["content"])
    
    print("\nInitial Key Moves Generated:")
    print(moves.modifications["content"])
    
    # Track versions
    versions = [moves.modifications["content"]]
    critiques = []
    refinements = []
    
    # Run critique/refinement cycles
    num_cycles = config["development_cycles"]["key_moves_num_cycles"]
    
    for cycle in range(num_cycles):
        print(f"\nStarting key moves critique cycle {cycle + 1}/{num_cycles}")
        
        # Get critique
        critique_state = {
            "key_moves_analysis": versions[-1],
            "framework": framework,
            "outline": final_outline,
            "literature": {
                "readings": lit_readings,
                "synthesis": lit_synthesis,
                "narrative": lit_synthesis_md
            }
        }
        
        critique = critic.run(critique_state)
        critiques.append(critique)
        
        # Save critique
        cycle_dir = os.path.join(moves_dir, f"cycle_{cycle}")
        os.makedirs(cycle_dir, exist_ok=True)
        
        save_json(os.path.join(cycle_dir, "critique.json"), 
                 {"critique": critique.modifications})
        save_text(os.path.join(cycle_dir, "critique.md"),
                 critique.modifications["content"])
        
        print("\nCritique Analysis:")
        print(f"Summary Assessment: {critique.modifications['summary']}")
        print("\nKey Recommendations:")
        print(critique.modifications["sections"]["Summary Assessment"])
        
        # Refine moves
        print(f"\nRefining key moves...")
        refinement_state = {
            "key_moves_analysis": versions[-1],
            "critique": critique.modifications,
            "framework": framework,
            "outline": final_outline,
            "literature": {
                "readings": lit_readings,
                "synthesis": lit_synthesis,
                "narrative": lit_synthesis_md
            }
        }
        
        refined = refinement_worker.run(refinement_state)
        refinements.append(refined)
        versions.append(refined.modifications["moves"])
        
        # Save refinement
        save_json(os.path.join(cycle_dir, "refinement.json"),
                 {"refinement": refined.modifications})
        save_text(os.path.join(cycle_dir, "refinement.md"),
                 refined.modifications["content"])
        
        print("\nRefinement Decisions:")
        decisions = refined.modifications["decisions"]
        print("\nWill Implement:")
        for change in decisions["will_implement"]:
            print(f"- {change['change']}: {change['rationale']}")
        print("\nWon't Implement:")
        for change in decisions["wont_implement"]:
            print(f"- {change['change']}: {change['rationale']}")
        
        print("\nUpdated Moves:")
        print(refined.modifications["moves"])
    
    # Save complete history and final version separately
    save_json(os.path.join(moves_dir, "moves_history.json"),
             {"versions": versions,
              "critiques": [c.modifications for c in critiques],
              "refinements": [r.modifications for r in refinements]})
    
    # Save final version for Phase II.3
    save_json(os.path.join("test_outputs", "framework_development", "final_key_moves.json"),
             {"key_moves": versions[-1]})

if __name__ == "__main__":
    test_key_moves_cycle()