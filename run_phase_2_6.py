import json
import os
import sys
from pathlib import Path
from typing import Dict, Any
import time
import yaml

from src.phases.phase_two.stages.stage_six.workflows.master_workflow import PaperVisionReviewWorkflow


def load_consolidated_context() -> Dict[str, Any]:
    """Load the consolidated context from Phase II.5"""
    try:
        with open("./outputs/phase_2_5_consolidated_context.json", encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValueError("Could not find phase_2_5_consolidated_context.json. Run Phase II.5 first.")


def run_phase_2_6():
    """Run Phase II.6: Holistic Review (formerly II.5)"""
    
    start_time = time.time()
    
    print("\n" + "="*60)
    print("PHASE II.6: Holistic Review")
    print("="*60)
    print("\nPerforming comprehensive philosophical review of the paper vision...")
    
    try:
        # Load configuration
        with open("config/conceptual_config.yaml", 'r') as f:
            config = yaml.safe_load(f)
        
        print("\n1. Loading consolidated context from Phase II.5...")
        consolidated_context = load_consolidated_context()
        
        # Extract thesis from raw outputs
        raw_outputs = consolidated_context.get("raw_outputs", {})
        abstract_framework = raw_outputs.get("abstract_framework", {}).get("abstract_framework", {})
        thesis = abstract_framework.get("main_thesis", "No thesis found")
        
        # Get move count from raw outputs
        developed_moves = raw_outputs.get("developed_moves", {}).get("developed_moves", [])
        move_count = len(developed_moves)
        
        print(f"   ✓ Loaded paper vision with thesis: {thesis[:100]}...")
        print(f"   ✓ Found {move_count} key moves to review")
        
        print("\n2. Running holistic review workflow...")
        workflow = PaperVisionReviewWorkflow(config)
        
        # The workflow expects the raw outputs, which we've preserved
        review_results = workflow.run_with_consolidated_context(consolidated_context)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n✓ Phase II.6 complete!")
        print(f"⏱️  Phase II.6 duration: {duration:.1f} seconds ({duration/60:.1f} minutes)")
        
        # Display review summary
        if "referee_report" in review_results:
            report = review_results["referee_report"]
            assessment = report.get("review_summary", {}).get("overall_assessment", "Unknown")
            most_damaging = report.get("review_summary", {}).get("most_damaging_flaw", "None identified")
            
            print("\n" + "-"*60)
            print("REVIEW SUMMARY")
            print("-"*60)
            print(f"Overall Assessment: {assessment}")
            print(f"Most Damaging Flaw: {most_damaging}")
            
            coherence_issues = report.get("coherence_issues", [])
            if coherence_issues:
                print(f"\nCoherence Issues: {len(coherence_issues)}")
                for i, issue in enumerate(coherence_issues[:3]):  # Show first 3
                    print(f"  {i+1}. {issue.get('issue_type', 'Unknown')}: {issue.get('description', '')[:100]}...")
        
        return review_results
        
    except Exception as e:
        print(f"\n❌ Error in Phase II.6: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    run_phase_2_6() 