# tests/test_abstract_refinement.py

import json
import yaml
import os
from pathlib import Path
from src.stages.phase_two.stages.stage_two.workers.abstract_refinement_worker import AbstractRefinementWorker
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

def save_text(path: str, content: str):
   """Save text file"""
   os.makedirs(os.path.dirname(path), exist_ok=True)
   with open(path, 'w') as f:
       f.write(content)

def test_abstract_refinement():
   """Test abstract and framework refinement through multiple cycles"""
   config = load_yaml("tests/test_config.yaml")
   critic = AbstractCritic(config)
   refinement_worker = AbstractRefinementWorker(config)
   
   # Load initial framework and literature context
   framework_result = load_json("test_outputs/framework_development/abstract_test.json")
   lit_readings = load_json("outputs/literature_readings.json")
   lit_synthesis = load_json("outputs/literature_synthesis.json")
   lit_synthesis_md = load_text("outputs/literature_synthesis.md")
   
   # Track versions
   versions = [framework_result]
   critiques = []
   
   # Create output directories
   refinements_dir = os.path.join("test_outputs", "framework_development", "refinements")
   os.makedirs(refinements_dir, exist_ok=True)
   
   # Run refinement cycles
   num_cycles = config["development_cycles"]["abstract_num_cycles"]
   
   for cycle in range(num_cycles):
        print(f"\nStarting refinement cycle {cycle + 1}/{num_cycles}")
       
        # Get critique of current version
        state = {
           "abstract_framework": versions[-1],
           "literature": {
               "readings": lit_readings,
               "synthesis": lit_synthesis,
               "narrative": lit_synthesis_md
           }
        }
       
        critique = critic.run(state)
        critiques.append(critique)
       
        # Save critique with all components
        cycle_dir = os.path.join(refinements_dir, f"cycle_{cycle}")
        os.makedirs(cycle_dir, exist_ok=True)
       
        save_json(os.path.join(cycle_dir, "critique.json"),
                {"critique": critique.modifications})
        save_text(os.path.join(cycle_dir, "critique.md"),
                critique.modifications["content"])
       
        # Refine framework
        refinement_state = {
           "current_framework": versions[-1],
           "current_critique": critique.modifications,
           "literature": {
               "readings": lit_readings,
               "synthesis": lit_synthesis,
               "narrative": lit_synthesis_md
           },
           "previous_versions": versions
        }
       
        refined = refinement_worker.run(refinement_state)
        versions.append(refined.modifications["framework_data"])
       
        # Save refined version with all components
        save_json(os.path.join(cycle_dir, "framework.json"),
                {"framework": refined.modifications["framework_data"]})
       
        # Save a more readable version with scratch work and decisions
        save_text(os.path.join(cycle_dir, "refinement_process.md"),
                f"# Scratch Work\n{refined.modifications['scratch_work']}\n\n" +
                f"# Refinement Decisions\n{refined.modifications['refinement_decisions']}\n\n" +
                f"# Framework Components\n\n" +
                f"## Abstract\n{refined.modifications['framework_data']['abstract']}\n\n" +
                f"## Main Thesis\n{refined.modifications['framework_data']['main_thesis']}\n\n" +
                f"## Core Contribution\n{refined.modifications['framework_data']['core_contribution']}\n\n" +
                f"## Key Moves\n" + "\n".join(f"- {move}" for move in refined.modifications['framework_data']['key_moves']) + "\n\n" +
                f"## Development Notes\n{refined.modifications['framework_data']['development_notes']}\n\n" +
                f"## Validation Status\n" + "\n".join(f"- {k}: {v}" for k,v in refined.modifications['framework_data']['validation_status'].items()) + "\n\n" +
                f"## Changes Made\n" + "\n".join(f"- {change}" for change in refined.modifications['framework_data']['changes_made']))
       
        print(f"\nCompleted cycle {cycle + 1}")
        print("\nRefinement Decisions:")
        print(refined.modifications["refinement_decisions"])
        print("\nUpdated Framework:")
        print(f"Abstract:\n{refined.modifications['framework_data']['abstract']}\n")
        print(f"Main Thesis:\n{refined.modifications['framework_data']['main_thesis']}\n")
        print(f"Core Contribution:\n{refined.modifications['framework_data']['core_contribution']}\n")
        print("Key Moves:")
        for move in refined.modifications["framework_data"]["key_moves"]:
            print(f"- {move}")
        print("\nChanges Made:")
        if refined.modifications["framework_data"].get("changes_made"):
            for change in refined.modifications["framework_data"]["changes_made"]:
                print(f"- {change}")
        else:
            print("No changes recorded")
        print("\nValidation Status:")
        print(json.dumps(refined.modifications["framework_data"]["validation_status"], indent=2))
   # Save complete refinement history
   save_json(os.path.join(refinements_dir, "refinement_history.json"),
            {"versions": versions, 
             "critiques": [c.modifications for c in critiques]})

if __name__ == "__main__":
   test_abstract_refinement()