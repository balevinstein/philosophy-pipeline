# tests/test_key_moves_worker.py

import json
import yaml
import os
from pathlib import Path
from src.stages.phase_two.stages.stage_two.workers.key_moves_worker import KeyMovesWorker

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

def load_text(path: str) -> str:
   """Load text file"""
   with open(path, 'r') as f:
       return f.read()

def test_key_moves_analysis():
   """Test key moves analysis"""
   config = load_yaml("tests/test_config.yaml")
   worker = KeyMovesWorker(config)
   
   # Load final refined abstract framework
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

   # Set up state for worker
   state = {
       "framework": framework,
       "outline": final_outline,
       "literature": {
           "readings": lit_readings,
           "synthesis": lit_synthesis,
           "narrative": lit_synthesis_md
       }
   }

   # Run key moves analysis
   print("\nAnalyzing key moves...")
   
   results = {}
   for move in framework["key_moves"]:
       print(f"\nAnalyzing move: {move}")
       worker._state["current_move"] = move
       result = worker.run(state)
       results[move] = result.modifications

   # Save output
   save_json("test_outputs/framework_development/key_moves_test.json", 
            {"key_moves_analysis": results})

   # Print results
   print("\nKey Moves Analysis:")
   for move, analysis in results.items():
       print(f"\nMove: {move}")
       print(analysis["content"])

if __name__ == "__main__":
   test_key_moves_analysis()