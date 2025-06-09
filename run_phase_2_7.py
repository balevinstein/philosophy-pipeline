import json
import os
import sys
from pathlib import Path
from typing import Dict, Any
import time
import yaml

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.phases.phase_two.stages.stage_seven.workers.refinement_worker import RefinementWorker


def load_config():
    """Load configuration from config file"""
    config_path = Path("config/conceptual_config.yaml")
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def load_phase_outputs() -> Dict[str, Any]:
    """Load outputs from previous phases"""
    outputs = {}
    
    # Load consolidated context from II.5
    try:
        with open("./outputs/phase_2_5_consolidated_context.json", encoding='utf-8') as f:
            outputs["consolidated_context"] = json.load(f)
        print("   ✓ Loaded consolidated context from II.5")
    except FileNotFoundError:
        raise ValueError("Could not find phase_2_5_consolidated_context.json. Run Phase II.5 first.")
    
    # Load review results from II.6
    try:
        with open("./outputs/paper_vision_review/referee_report.json", encoding='utf-8') as f:
            outputs["referee_report"] = json.load(f)
        print("   ✓ Loaded referee report from II.6")
    except FileNotFoundError:
        raise ValueError("Could not find referee_report.json. Run Phase II.6 first.")
    
    try:
        with open("./outputs/paper_vision_review/final_writing_plan.json", encoding='utf-8') as f:
            outputs["final_writing_plan"] = json.load(f)
        print("   ✓ Loaded final writing plan from II.6")
    except FileNotFoundError:
        raise ValueError("Could not find final_writing_plan.json. Run Phase II.6 first.")
    
    # Load move examples
    try:
        with open("./outputs/curated_moves/injectable_examples.json", encoding='utf-8') as f:
            outputs["move_examples"] = json.load(f)
        print("   ✓ Loaded philosophical move examples")
    except FileNotFoundError:
        print("   ⚠ Warning: injectable_examples.json not found, using empty dict")
        outputs["move_examples"] = {}
    
    return outputs


def run_phase_2_7():
    """Run Phase II.7: Targeted Refinement"""
    
    start_time = time.time()
    
    print("\n" + "="*60)
    print("PHASE II.7: Targeted Refinement")
    print("="*60)
    print("\nImplementing targeted refinements based on review feedback...")
    
    try:
        print("\n1. Loading configuration...")
        config = load_config()
        
        print("\n2. Loading outputs from previous phases...")
        outputs = load_phase_outputs()
        
        # Extract original moves from consolidated context
        raw_outputs = outputs["consolidated_context"].get("raw_outputs", {})
        developed_moves = raw_outputs.get("developed_moves", {}).get("developed_moves", [])
        
        print(f"   ✓ Found {len(developed_moves)} original moves")
        
        # Count moves needing refinement
        writing_plan = outputs["final_writing_plan"]
        moves_to_refine = [m for m in writing_plan.get("final_key_moves", []) 
                          if m.get("status") == "Flagged for Redevelopment"]
        
        print(f"   ✓ {len(moves_to_refine)} moves flagged for redevelopment")
        
        print("\n3. Initializing refinement worker...")
        refinement_worker = RefinementWorker(config)
        
        # Prepare state for worker
        worker_state = {
            "original_moves": developed_moves,
            "final_writing_plan": writing_plan,
            "referee_report": outputs["referee_report"],
            "move_examples": outputs["move_examples"]
        }
        
        print("\n4. Running targeted refinements...")
        refinement_results = refinement_worker.run(worker_state)
        
        # Extract results
        refined_moves = refinement_results["refined_moves"]
        metadata = refinement_results["refinement_metadata"]
        
        print(f"\n   ✓ Refinement complete:")
        print(f"      - Original moves: {metadata['original_count']}")
        print(f"      - Refined moves: {metadata['refined_count']}")
        print(f"      - Redeveloped: {metadata['redeveloped_count']}")
        
        # Create final refined context
        refined_context = {
            "revised_paper_vision": {
                "thesis": metadata["revised_thesis"],
                "core_contribution": metadata["revised_contribution"],
                "revision_summary": writing_plan.get("revision_summary", "")
            },
            "refined_moves": refined_moves,
            "refinement_metadata": metadata,
            "structure": {
                "outline": writing_plan.get("final_outline", {}),
                "sections": extract_sections(writing_plan.get("final_outline", {}))
            },
            "review_addressed": {
                "referee_assessment": outputs["referee_report"]["review_summary"]["overall_assessment"],
                "most_damaging_flaw": outputs["referee_report"]["review_summary"]["most_damaging_flaw"],
                "issues_addressed": count_addressed_issues(refined_moves)
            },
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Save refined context
        output_file = "./outputs/phase_2_7_refined_context.json"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, "w", encoding='utf-8') as f:
            json.dump(refined_context, f, indent=2)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n✓ Phase II.7 complete! Refined context saved to: {output_file}")
        print(f"⏱️  Phase II.7 duration: {duration:.1f} seconds ({duration/60:.1f} minutes)")
        
        # Print summary
        print("\n" + "-"*60)
        print("REFINEMENT SUMMARY")
        print("-"*60)
        print(f"Revised thesis: {metadata['revised_thesis'][:150]}...")
        
        # Show redeveloped moves
        redeveloped = [m for m in refined_moves if m.get("status") == "Redeveloped"]
        if redeveloped:
            print(f"\nRedeveloped moves:")
            for move in redeveloped:
                print(f"  - Move {move['key_move_index']}: {move['key_move_text'][:80]}...")
                if move.get("addressed_issues"):
                    print(f"    Addressed: {', '.join(move['addressed_issues'])}")
        
        # Show quality checks if available
        quality_passed = 0
        quality_total = 0
        for move in redeveloped:
            if "quality_checks" in move:
                checks = move["quality_checks"]
                quality_total += len(checks)
                quality_passed += sum(1 for v in checks.values() if v)
                
        if quality_total > 0:
            print(f"\nQuality checks: {quality_passed}/{quality_total} passed ({quality_passed/quality_total*100:.0f}%)")
        
        return refined_context
        
    except Exception as e:
        print(f"\n❌ Error in Phase II.7: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def extract_sections(outline: Dict[str, Any]) -> list:
    """Extract section information from outline"""
    sections = []
    for key, value in outline.items():
        if isinstance(value, dict) and "word_target" in value:
            sections.append({
                "key": key,
                "title": value.get("title", key.replace("_", " ").title()),
                "word_target": value["word_target"],
                "guidance": value.get("content_guidance", "")[:200] + "..."
            })
    return sections


def count_addressed_issues(refined_moves: list) -> int:
    """Count total issues addressed across all refined moves"""
    total = 0
    for move in refined_moves:
        if move.get("addressed_issues"):
            total += len(move["addressed_issues"])
    return total


if __name__ == "__main__":
    run_phase_2_7() 