import json
import os
import sys
from pathlib import Path
from typing import Dict, Any

from src.phases.phase_three.stages.stage_two.workers.reader.paper_reader import PaperReaderWorker
from src.phases.phase_three.stages.stage_two.workers.integration.paper_integration import PaperIntegrationWorker
from src.utils.api import load_config


def load_phase_3_1_output() -> Dict[str, Any]:
    """Load the output from Phase III.1"""
    try:
        # Load the draft paper
        with open("./outputs/phase_3_1_draft.md", "r") as f:
            draft_paper = f.read()
        
        # Load the progress metadata
        with open("./outputs/phase_3_1_progress.json", "r") as f:
            progress_data = json.load(f)
        
        return {
            "draft_paper": draft_paper,
            "paper_overview": progress_data["paper_overview"],
            "sections_metadata": progress_data["sections"],
            "metadata": progress_data["metadata"]
        }
    except FileNotFoundError as e:
        raise ValueError(f"Could not find Phase III.1 output. Run Phase III.1 first. Missing: {e.filename}")


def analyze_paper_globally(phase_3_1_output: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze the complete paper for global issues and integration opportunities"""
    
    print(f"\n🔍 Stage 1: Global Paper Analysis")
    print(f"Analyzing complete draft for flow, transitions, and coherence...")
    
    reader = PaperReaderWorker(config)
    
    # Prepare analysis state
    analysis_state = {
        "draft_paper": phase_3_1_output["draft_paper"],
        "paper_overview": phase_3_1_output["paper_overview"],
        "sections_metadata": phase_3_1_output["sections_metadata"]
    }
    
    # Execute analysis
    analysis_output = reader.execute(analysis_state)
    if analysis_output.status != "completed":
        raise Exception(f"Paper analysis failed: {analysis_output.notes}")
    
    assessment = analysis_output.modifications["summary_assessment"]
    major_issues = len(analysis_output.modifications["critical_issues"]["major"])
    minor_issues = len(analysis_output.modifications["critical_issues"]["minor"])
    priority_actions = len(analysis_output.modifications["priority_actions"])
    
    print(f"✓ Analysis complete: {assessment}")
    print(f"  Major issues: {major_issues}")
    print(f"  Minor issues: {minor_issues}")
    print(f"  Priority actions: {priority_actions}")
    
    return analysis_output.modifications


def integrate_improvements(phase_3_1_output: Dict[str, Any], analysis_results: Dict[str, Any], 
                         config: Dict[str, Any]) -> Dict[str, Any]:
    """Integrate improvements into the paper based on analysis"""
    
    print(f"\n✨ Stage 2: Paper Integration")
    print(f"Implementing improvements for final publication-ready version...")
    
    integrator = PaperIntegrationWorker(config)
    
    # Prepare integration state
    integration_state = {
        "draft_paper": phase_3_1_output["draft_paper"],
        "paper_analysis": analysis_results["analysis_content"],
        "paper_overview": phase_3_1_output["paper_overview"]
    }
    
    # Execute integration
    integration_output = integrator.execute(integration_state)
    if integration_output.status != "completed":
        raise Exception(f"Paper integration failed: {integration_output.notes}")
    
    final_word_count = integration_output.modifications["final_word_count"]
    changes_made = len(integration_output.modifications["changes_made"])
    
    # Debug: Check if we have the response content
    response_content = integration_output.modifications.get("response_content", "")
    print(f"DEBUG: Response content length: {len(response_content)}")
    print(f"DEBUG: Final paper length: {len(integration_output.modifications.get('final_paper', ''))}")
    
    print(f"✓ Integration complete: {final_word_count} words")
    print(f"  Changes implemented: {changes_made}")
    
    return integration_output.modifications


def save_final_paper(integration_results: Dict[str, Any], analysis_results: Dict[str, Any],
                    phase_3_1_output: Dict[str, Any]) -> str:
    """Save the final paper and create summary metadata"""
    
    final_paper = integration_results["final_paper"]
    
    # Save the final paper
    final_paper_file = "./outputs/final_paper.md"
    with open(final_paper_file, "w") as f:
        f.write(final_paper)
    
    # Debug: Save the full response content
    response_content = integration_results.get("response_content", "")
    if response_content:
        with open("./outputs/debug_integration_response.txt", "w") as f:
            f.write(response_content)
        print(f"DEBUG: Saved full response to debug_integration_response.txt ({len(response_content)} chars)")
    
    # Create comprehensive metadata
    final_metadata = {
        "metadata": {
            "timestamp": "2024-01-01T00:00:00",  # Would be actual timestamp
            "phase": "III.2", 
            "stage": "paper_integration",
            "final_word_count": integration_results["final_word_count"],
            "target_word_count": phase_3_1_output["paper_overview"]["target_words"],
            "sections_count": len(phase_3_1_output["sections_metadata"]),
            "global_assessment": analysis_results["summary_assessment"],
            "improvements_made": len(integration_results["changes_made"])
        },
        "paper_overview": phase_3_1_output["paper_overview"],
        "analysis_summary": {
            "assessment": analysis_results["summary_assessment"],
            "major_issues_found": len(analysis_results["major_issues"]),
            "minor_issues_found": len(analysis_results["minor_issues"]),
            "priority_actions": analysis_results["priority_actions"],
            "strengths_identified": analysis_results["strengths"]
        },
        "integration_summary": {
            "changes_made": integration_results["changes_made"],
            "final_statistics": integration_results["final_statistics"],
            "integration_notes": integration_results["integration_summary"]
        },
        "pipeline_history": {
            "phase_3_1_sections_refined": phase_3_1_output["metadata"]["sections_refined"],
            "phase_3_1_total_words": phase_3_1_output["metadata"]["total_words_written"],
            "final_improvement": "Global integration and presentation enhancement"
        }
    }
    
    # Save metadata
    metadata_file = "./outputs/final_paper_metadata.json"
    with open(metadata_file, "w") as f:
        json.dump(final_metadata, f, indent=2)
    
    return final_paper_file


def run_phase_3_2():
    """Run Phase III.2: Global Paper Integration and Final Polish"""
    
    print("\n" + "="*70)
    print("PHASE III.2: Global Paper Integration")
    print("="*70)
    print("\nCreating final publication-ready paper through global analysis and integration")
    print("  Stage 1: Analyze complete paper for global issues")
    print("  Stage 2: Integrate improvements for final version")
    
    try:
        # Load configuration and Phase III.1 output
        print("\n1. Loading configuration and Phase III.1 output...")
        config = load_config()
        phase_3_1_output = load_phase_3_1_output()
        
        draft_word_count = len(phase_3_1_output["draft_paper"].split())
        sections_count = len(phase_3_1_output["sections_metadata"])
        
        print(f"   ✓ Loaded draft paper: {draft_word_count} words, {sections_count} sections")
        print(f"   ✓ Target: {phase_3_1_output['paper_overview']['target_words']} words")
        
        # Stage 1: Global Analysis
        print("\n2. Analyzing paper for global integration opportunities...")
        analysis_results = analyze_paper_globally(phase_3_1_output, config)
        
        # Stage 2: Integration
        print("\n3. Integrating improvements into final paper...")
        integration_results = integrate_improvements(phase_3_1_output, analysis_results, config)
        
        # Save final outputs
        print("\n4. Saving final publication-ready paper...")
        final_paper_file = save_final_paper(integration_results, analysis_results, phase_3_1_output)
        
        final_word_count = integration_results["final_word_count"]
        target_words = phase_3_1_output["paper_overview"]["target_words"]
        word_efficiency = (final_word_count / target_words) * 100
        
        print(f"\n✓ Phase III.2 complete!")
        print(f"\n📋 FINAL PAPER SUMMARY:")
        print(f"   📄 Final paper: {final_paper_file}")
        print(f"   📊 Word count: {final_word_count} ({word_efficiency:.1f}% of target)")
        print(f"   ✨ Global assessment: {analysis_results['summary_assessment']}")
        print(f"   🔧 Improvements made: {len(integration_results['changes_made'])}")
        
        print(f"\n📈 PIPELINE SUMMARY:")
        print(f"   Phase III.1 → Phase III.2 improvement:")
        print(f"   • Sections refined in III.1: {phase_3_1_output['metadata']['sections_refined']}")
        print(f"   • Global improvements in III.2: {len(integration_results['changes_made'])}")
        print(f"   • Final presentation quality: Publication-ready")
        
        # Show specific improvements made
        print(f"\n🎯 KEY IMPROVEMENTS:")
        for i, change in enumerate(integration_results["changes_made"][:5], 1):
            print(f"   {i}. {change}")
        if len(integration_results["changes_made"]) > 5:
            print(f"   ... and {len(integration_results['changes_made']) - 5} more")
        
        return {
            "final_paper_file": final_paper_file,
            "final_word_count": final_word_count,
            "global_assessment": analysis_results["summary_assessment"],
            "improvements_made": len(integration_results["changes_made"]),
            "success": True
        }
        
    except Exception as e:
        print(f"\n❌ Error in Phase III.2: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    run_phase_3_2() 