import json
import os
import sys
from pathlib import Path
from typing import Dict, Any
import time
from datetime import datetime

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.phases.phase_two.stages.stage_five.workers.synthesis_worker import SynthesisWorker
from src.phases.phase_two.stages.stage_five.workers.quality_audit_worker import QualityAuditWorker
from run_utils import load_config


def load_phase_outputs() -> Dict[str, Any]:
    """Load all outputs from Phase II.1-4"""
    outputs = {}
    
    # Load II.1 Literature Synthesis
    try:
        with open("./outputs/literature_synthesis.json", encoding='utf-8') as f:
            outputs["literature_synthesis"] = json.load(f)
        print("   ✓ Loaded literature synthesis from II.1")
    except FileNotFoundError:
        print("   ⚠ Warning: literature_synthesis.json not found")
        outputs["literature_synthesis"] = {}
    
    # Load II.2 Framework
    try:
        with open("./outputs/framework_development/abstract_framework.json", encoding='utf-8') as f:
            outputs["abstract_framework"] = json.load(f)
        print("   ✓ Loaded abstract framework from II.2")
    except FileNotFoundError:
        raise ValueError("Could not find abstract_framework.json. Run Phase II.2 first.")
    
    # Load II.3 Developed Moves
    try:
        with open("./outputs/key_moves_development/key_moves_development/all_developed_moves.json") as f:
            outputs["developed_moves"] = json.load(f)
        print("   ✓ Loaded developed key moves from II.3")
    except FileNotFoundError:
        raise ValueError("Could not find all_developed_moves.json. Run Phase II.3 first.")
    
    # Load II.4 Detailed Outline
    try:
        with open("./outputs/detailed_outline/detailed_outline_final.json") as f:
            outputs["detailed_outline"] = json.load(f)
        print("   ✓ Loaded detailed outline from II.4")
    except FileNotFoundError:
        raise ValueError("Could not find detailed_outline_final.json. Run Phase II.4 first.")
    
    return outputs


def run_phase_2_5():
    """Run Phase II.5: Quick Synthesis + Quality Audit"""
    
    start_time = time.time()
    
    print("\n" + "="*60)
    print("PHASE II.5: Quick Synthesis + Quality Audit")
    print("="*60)
    print("\nStage 5a: Quick synthesis and coherence check")
    print("Stage 5b: Targeted quality audit with remediation guidance")
    
    try:
        print("\n1. Loading outputs from Phases II.1-4...")
        outputs = load_phase_outputs()
        
        print("\n2. Loading configuration...")
        config = load_config()
        
        # Prepare state for workers
        state = {
            "literature_synthesis": outputs["literature_synthesis"],
            "abstract_framework": outputs["abstract_framework"],
            "developed_moves": outputs["developed_moves"],
            "detailed_outline": outputs["detailed_outline"]
        }
        
        # Stage II.5a: Quick Synthesis
        print("\n3. Running Stage II.5a: Quick Synthesis...")
        synthesis_worker = SynthesisWorker(config)
        synthesis_results = synthesis_worker.run(state)
        
        print(f"   ✓ Synthesis complete - coherence assessment done")
        
        # Update state with synthesis results
        state["synthesis_results"] = synthesis_results
        
        # Stage II.5b: Quality Audit
        print("\n4. Running Stage II.5b: Quality Audit...")
        audit_worker = QualityAuditWorker(config)
        audit_results = audit_worker.run(state)
        
        print(f"   ✓ Quality audit complete - remediation guidance generated")
        
        # Combine results
        combined_results = {
            "synthesis_analysis": synthesis_results,
            "quality_audit": audit_results,
            "phase_2_5_summary": {
                "synthesis_status": synthesis_results.get("coherence_status", "unknown"),
                "major_issues_identified": synthesis_results.get("major_issues", []),
                "audit_priority_count": len(audit_results.get("priority_recommendations", [])),
                "paper_readiness": audit_results.get("overall_assessment", {}).get("readiness_level", "unknown"),
                "next_phase_guidance": audit_results.get("next_phase_guidance", {})
            },
            "raw_outputs": outputs,
            "timestamp": datetime.now().isoformat()
        }
        
        # Save combined results
        output_file = "./outputs/phase_2_5_consolidated_context.json"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, "w", encoding='utf-8') as f:
            json.dump(combined_results, f, indent=2)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n✓ Phase II.5 complete! Results saved to: {output_file}")
        print(f"⏱️  Phase II.5 duration: {duration:.1f} seconds")
        
        print("\n" + "-"*60)
        print("PHASE II.5 SUMMARY")
        print("-"*60)
        
        summary = combined_results["phase_2_5_summary"]
        print(f"Synthesis status: {summary['synthesis_status']}")
        print(f"Paper readiness: {summary['paper_readiness']}")
        print(f"Major issues identified: {len(summary['major_issues_identified'])}")
        print(f"Priority recommendations: {summary['audit_priority_count']}")
        
        if summary['major_issues_identified']:
            print("\nMajor issues found:")
            for issue in summary['major_issues_identified'][:3]:
                print(f"  • {issue}")
        
        if audit_results.get("priority_recommendations"):
            print("\nTop priority actions:")
            for i, rec in enumerate(audit_results["priority_recommendations"][:3], 1):
                print(f"  {i}. {rec.get('action', rec)}")
        
        return combined_results
        
    except Exception as e:
        print(f"\n❌ Error in Phase II.5: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    run_phase_2_5() 