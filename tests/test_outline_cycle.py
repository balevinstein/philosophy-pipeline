# tests/test_outline_cycle.py

import json
import yaml
import os
from pathlib import Path
from src.stages.phase_two.stages.stage_two.workers.outline_worker import OutlineWorker
from src.stages.phase_two.stages.stage_two.workers.outline_critic import OutlineCritic
from src.stages.phase_two.stages.stage_two.workers.outline_refinement_worker import OutlineRefinementWorker

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

def test_outline_cycle():
    """Test complete outline development cycle"""
    config = load_yaml("tests/test_config.yaml")
   
    # Load final abstract framework
    # Before trying to load the final framework, let's get the correct cycle number
    refinements_dir = os.path.join("test_outputs", "framework_development", "refinements")
    cycles = [d for d in os.listdir(refinements_dir) if d.startswith("cycle_")]
    final_cycle = max(int(cycle.split("_")[1]) for cycle in cycles)

    # Then load the framework
    framework = load_json(os.path.join(refinements_dir, f"cycle_{final_cycle}", "framework.json"))["framework"]
    
    # Load literature context
    lit_readings = load_json("outputs/literature_readings.json")
    lit_synthesis = load_json("outputs/literature_synthesis.json")
    lit_synthesis_md = load_text("outputs/literature_synthesis.md")
    
    # Initialize workers
    outline_worker = OutlineWorker(config)
    critic = OutlineCritic(config)
    refinement_worker = OutlineRefinementWorker(config)
    
    # Create output directory
    outline_dir = os.path.join("test_outputs", "framework_development", "outline_development")
    os.makedirs(outline_dir, exist_ok=True)
   
    # Generate initial outline
    print("\nGenerating initial outline...")
    state = {
       "framework": framework,
       "literature": {
           "readings": lit_readings,
           "synthesis": lit_synthesis,
           "narrative": lit_synthesis_md
       }
    }
   
    outline = outline_worker.run(state)
    save_text(os.path.join(outline_dir, "initial_outline.md"), outline.modifications["outline"])
   
    print("\nInitial Outline Generated:")
    print(outline.modifications["outline"])
   
    # Track versions
    versions = [outline.modifications["outline"]]
    critiques = []
    refinements = []
   
    # Run critique/refinement cycles
    num_cycles = config["development_cycles"]["outline_num_cycles"]
   
    for cycle in range(num_cycles):
       print(f"\nStarting outline critique cycle {cycle + 1}/{num_cycles}")
       
       # Get critique
       critique_state = {
           "outline": versions[-1],
           "framework": framework,
           "literature": {
               "readings": lit_readings,
               "synthesis": lit_synthesis,
               "narrative": lit_synthesis_md
           }
       }
       
       critique = critic.run(critique_state)
       critiques.append(critique)
       
       # Save critique
       cycle_dir = os.path.join(outline_dir, f"cycle_{cycle}")
       os.makedirs(cycle_dir, exist_ok=True)
       
       save_json(os.path.join(cycle_dir, "critique.json"), 
                {"critique": critique.modifications})
       save_text(os.path.join(cycle_dir, "critique.md"),
                critique.modifications["content"])
       
       print("\nCritique Analysis:")
       print(f"Summary Assessment: {critique.modifications['summary']}")
       print("\nRed Flags:")
       for flag in critique.modifications["red_flags"]:
           print(f"- {flag}")
       
       print("\nSpecific Recommendations:")
       print(critique.modifications["sections"]["Specific Recommendations"])
       
       # Refine outline
       print(f"\nRefining outline...")
       refinement_state = {
           "outline": versions[-1],
           "critique": critique.modifications,
           "framework": framework,
           "literature": {
               "readings": lit_readings,
               "synthesis": lit_synthesis,
               "narrative": lit_synthesis_md
           }
       }
       
       refined = refinement_worker.run(refinement_state)
       refinements.append(refined)
       versions.append(refined.modifications["outline"])
       
       # Save refinement
       save_json(os.path.join(cycle_dir, "refinement.json"),
                {"refinement": refined.modifications})
       save_text(os.path.join(cycle_dir, "refinement.md"),
                refined.modifications["content"])
       
       print("\nRefinement Decisions:")
       print("\nWill Implement:")
       for change in refined.modifications["decisions"]["will_implement"]:
           print(f"- {change}")
       print("\nWon't Implement:")
       for change in refined.modifications["decisions"]["wont_implement"]:
           print(f"- {change}")
       
       print("\nUpdated Outline:")
       print(refined.modifications["outline"])
       
    # Save complete history
    save_json(os.path.join(outline_dir, "outline_history.json"),
            {"versions": versions,
             "critiques": [c.modifications for c in critiques],
             "refinements": [r.modifications for r in refinements]})

if __name__ == "__main__":
   test_outline_cycle()