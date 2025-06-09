import json
import os
import sys
from pathlib import Path
from typing import Dict, Any
import time
from datetime import datetime
import yaml

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.phases.phase_two.stages.stage_five.workers import ConsolidationWorker


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


def create_consolidated_context(outputs: Dict[str, Any]) -> Dict[str, Any]:
    """Create an intelligently consolidated view of the paper-to-be"""
    
    # Extract key components
    framework = outputs["abstract_framework"].get("abstract_framework", {})
    main_thesis = framework.get("main_thesis", "")
    core_contribution = framework.get("core_contribution", "")
    abstract = framework.get("abstract", "")
    
    # Extract developed moves
    developed_moves = outputs["developed_moves"].get("developed_moves", [])
    
    # Extract outline
    outline_data = outputs["detailed_outline"]
    final_outline = outline_data.get("final_outline", "")
    
    # Create consolidated context
    consolidated = {
        "paper_vision": {
            "thesis": main_thesis,
            "core_contribution": core_contribution,
            "abstract": abstract,
            "structure": extract_structure_from_outline(final_outline),
        },
        "philosophical_content": {
            "key_moves": consolidate_key_moves(developed_moves),
            "argument_flow": extract_argument_flow(developed_moves, final_outline),
        },
        "literature_context": {
            "synthesis": outputs["literature_synthesis"].get("synthesis", {}),
            "key_sources": extract_key_sources(outputs["literature_synthesis"]),
        },
        "metadata": {
            "word_target": 4000,
            "journal": "Analysis",
            "phase_timings": extract_timings(outputs),
        },
        "raw_outputs": outputs  # Keep raw outputs for reference
    }
    
    return consolidated


def extract_structure_from_outline(outline_text: str) -> Dict[str, Any]:
    """Extract the section structure from the outline text"""
    sections = []
    
    # Parse the outline text to extract sections
    lines = outline_text.split('\n')
    current_section = None
    current_subsections = []
    
    for line in lines:
        line = line.strip()
        if line.startswith('# ') and not line.startswith('## '):
            # Main section
            if current_section:
                sections.append({
                    "title": current_section,
                    "subsections": current_subsections
                })
            current_section = line[2:].strip()
            current_subsections = []
        elif line.startswith('## '):
            # Subsection
            current_subsections.append(line[3:].strip())
    
    # Don't forget the last section
    if current_section:
        sections.append({
            "title": current_section,
            "subsections": current_subsections
        })
    
    return {"sections": sections}


def consolidate_key_moves(developed_moves: list) -> list:
    """Consolidate key moves into a cleaner format"""
    consolidated_moves = []
    
    for move in developed_moves:
        consolidated_move = {
            "index": move.get("key_move_index", 0),
            "description": move.get("key_move_text", ""),
            "content": move.get("final_content", ""),
            "development_phases": {
                "initial": move.get("development", {}).get("initial", ""),
                "examples": move.get("development", {}).get("examples", ""),
                "literature": move.get("development", {}).get("literature", ""),
            }
        }
        consolidated_moves.append(consolidated_move)
    
    return consolidated_moves


def extract_argument_flow(developed_moves: list, outline_text: str) -> Dict[str, Any]:
    """Extract how arguments flow through the paper"""
    # This is a simple implementation - could be enhanced
    return {
        "move_count": len(developed_moves),
        "outline_present": bool(outline_text),
        "flow_type": "sequential"  # Could analyze for more complex flows
    }


def extract_key_sources(literature_synthesis: Dict[str, Any]) -> list:
    """Extract the most important sources from the literature"""
    key_sources = []
    
    # Try to find key sources in different possible locations
    if "key_sources" in literature_synthesis:
        return literature_synthesis["key_sources"]
    
    # Extract from synthesis if available
    synthesis = literature_synthesis.get("synthesis", {})
    if "sources" in synthesis:
        sources = synthesis["sources"]
        # Take first 5 sources as key sources
        for source in sources[:5]:
            if isinstance(source, dict):
                key_sources.append({
                    "title": source.get("title", ""),
                    "author": source.get("author", ""),
                    "relevance": source.get("relevance", "")
                })
    
    return key_sources


def extract_timings(outputs: Dict[str, Any]) -> Dict[str, float]:
    """Extract timing information from phase outputs"""
    timings = {}
    
    # Extract timings from developed moves if available
    developed_moves_data = outputs.get("developed_moves", {})
    if "metadata" in developed_moves_data:
        timing_summary = developed_moves_data["metadata"].get("timing_summary", {})
        if "total_duration" in timing_summary:
            timings["phase_2_3_duration"] = timing_summary["total_duration"]
    
    return timings


def load_config():
    """Load configuration from config file"""
    config_path = Path("config/conceptual_config.yaml")
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        full_config = yaml.safe_load(f)
    
    # Return the full config structure that APIHandler expects
    return full_config


def run_phase_2_5():
    """Run Phase II.5: Intelligent Consolidation"""
    
    start_time = time.time()
    
    print("\n" + "="*60)
    print("PHASE II.5: Intelligent Consolidation")
    print("="*60)
    print("\nPerforming intelligent consolidation and diagnostic analysis...")
    
    try:
        print("\n1. Loading outputs from Phases II.1-4...")
        outputs = load_phase_outputs()
        
        print("\n2. Initializing consolidation worker...")
        # Create config for workers
        config = load_config()
        
        # Initialize worker
        consolidation_worker = ConsolidationWorker(config)
        
        print("\n3. Running intelligent consolidation...")
        # Prepare state for worker
        state = {
            "literature_synthesis": outputs["literature_synthesis"],
            "abstract_framework": outputs["abstract_framework"],
            "developed_moves": outputs["developed_moves"],
            "detailed_outline": outputs["detailed_outline"]
        }
        
        # Run consolidation analysis
        consolidation_result = consolidation_worker.run(state)
        
        # Extract consolidated analysis
        consolidated_analysis = consolidation_result["consolidated_analysis"]
        diagnostic_summary = consolidation_result["diagnostic_summary"]
        
        print("\n4. Processing consolidation results...")
        print(f"   ✓ Identified {diagnostic_summary['total_issues']} issues")
        print(f"   ✓ High priority issues: {diagnostic_summary['high_priority_issues']}")
        print(f"   ✓ Paper readiness: {diagnostic_summary['paper_readiness']}")
        
        # Create enhanced consolidated context
        consolidated_context = {
            "consolidated_vision": consolidated_analysis["consolidated_vision"],
            "diagnostic_analysis": {
                "key_move_assessment": consolidated_analysis["key_move_assessment"],
                "identified_issues": consolidated_analysis["identified_issues"],
                "redundancy_analysis": consolidated_analysis["redundancy_analysis"],
                "gap_analysis": consolidated_analysis["gap_analysis"],
                "diagnostic_details": consolidated_analysis.get("diagnostic_details", {}),
                "quality_standard_violations": consolidated_analysis.get("diagnostic_details", {}).get("quality_standard_violations", {}),
                "thesis_support_analysis": consolidated_analysis.get("diagnostic_details", {}).get("thesis_support_analysis", {}),
                "argumentative_gaps": consolidated_analysis.get("diagnostic_details", {}).get("argumentative_gaps", {}),
                "conceptual_clarity": consolidated_analysis.get("diagnostic_details", {}).get("conceptual_clarity", {}),
                "example_quality": consolidated_analysis.get("diagnostic_details", {}).get("example_quality", {}),
                "structural_issues": consolidated_analysis.get("diagnostic_details", {}).get("structural_issues", {}),
                "literature_integration": consolidated_analysis.get("diagnostic_details", {}).get("literature_integration", {})
            },
            "priority_recommendations": consolidated_analysis["priority_recommendations"],
            "overall_assessment": consolidated_analysis["overall_assessment"],
            "diagnostic_summary": diagnostic_summary,
            "raw_outputs": outputs,  # Keep original outputs for reference
            "timestamp": consolidation_result["timestamp"]
        }
        
        # Save consolidated context
        output_file = "./outputs/phase_2_5_consolidated_context.json"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, "w", encoding='utf-8') as f:
            json.dump(consolidated_context, f, indent=2)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n✓ Phase II.5 complete! Consolidated context saved to: {output_file}")
        print(f"⏱️  Phase II.5 duration: {duration:.1f} seconds")
        
        print("\n" + "-"*60)
        print("INTELLIGENT CONSOLIDATION SUMMARY")
        print("-"*60)
        print(f"Paper readiness: {diagnostic_summary['paper_readiness']}")
        print(f"Total issues identified: {diagnostic_summary['total_issues']}")
        print(f"High priority issues: {diagnostic_summary['high_priority_issues']}")
        
        if diagnostic_summary['main_strengths']:
            print("\nMain strengths:")
            for strength in diagnostic_summary['main_strengths'][:3]:
                print(f"  • {strength}")
        
        if diagnostic_summary['main_weaknesses']:
            print("\nMain weaknesses:")
            for weakness in diagnostic_summary['main_weaknesses'][:3]:
                print(f"  • {weakness}")
        
        if consolidated_analysis.get("priority_recommendations"):
            print("\nTop priority actions:")
            for rec in consolidated_analysis["priority_recommendations"][:3]:
                print(f"  {rec['priority']}. {rec['action']}")
        
        return consolidated_context
        
    except Exception as e:
        print(f"\n❌ Error in Phase II.5: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    run_phase_2_5() 