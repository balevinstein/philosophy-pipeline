import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, Any, List

from src.phases.phase_three.stages.stage_one.workers.writing.section_writer import SectionWritingWorker
from src.phases.phase_three.stages.stage_one.workers.critic.section_critic import SectionCriticWorker
from src.phases.phase_three.stages.stage_one.workers.refinement.section_refinement import SectionRefinementWorker
from src.utils.api import load_config


def load_writing_context() -> Dict[str, Any]:
    """Load the writing context created by Phase II.8"""
    try:
        with open("./outputs/phase_2_8_writing_context.json") as f:
            context = json.load(f)
            # Transform the new structure to match what Phase III expects
            transformed_context = {
                "paper_overview": {
                    "thesis": context["paper_metadata"]["thesis"],
                    "abstract": f"{context['paper_metadata']['thesis']} {context['paper_metadata']['core_contribution']}",
                    "target_words": context["paper_metadata"]["word_target"],
                    "sections_count": len(context["section_blueprints"])
                },
                "sections": [],
                "content_bank": {
                    "arguments": [
                        {
                            "move_text": move.get("key_move_text", ""),
                            "content": move.get("refined_content", ""),
                            "move_index": i,
                            "status": move.get("status", "Unknown")
                        }
                        for i, move in enumerate(context.get("refined_moves", []))
                    ],
                    "examples": [],  # We'll extract these from moves if needed
                    "citations": []  # We'll use citation_placement from content_organization
                },
                "writing_aids": context.get("writing_aids", {}),
                "content_organization": context.get("content_organization", {}),
                "literature_synthesis": context.get("literature_context", {})
            }
            
            # Transform section blueprints into sections
            for blueprint in context.get("section_blueprints", []):
                section = {
                    "section_name": blueprint["title"],
                    "content_guidance": blueprint["content_guidance"],
                    "word_target": blueprint["word_target"],
                    "transition_in": blueprint.get("transition_in", ""),
                    "transition_out": blueprint.get("transition_out", ""),
                    "suggested_moves": blueprint.get("suggested_moves", [])
                }
                transformed_context["sections"].append(section)
                
            # Add introduction hooks if available
            if "introduction_hooks" in context.get("writing_aids", {}):
                transformed_context["introduction_hooks"] = context["writing_aids"]["introduction_hooks"]
                
            # Add phrase banks
            if "phrase_banks" in context.get("writing_aids", {}):
                transformed_context["phrase_banks"] = context["writing_aids"]["phrase_banks"]
                
            return transformed_context
            
    except FileNotFoundError:
        raise ValueError("Could not find phase_2_8_writing_context.json. Run Phase II.8 first.")


def process_section_with_critique(writing_context: Dict[str, Any], section_index: int, config: Dict[str, Any]) -> Dict[str, Any]:
    """Process a single section through the full 3-stage pipeline: write → critique → refine"""
    
    section = writing_context["sections"][section_index]
    print(f"\n{'='*70}")
    print(f"Processing Section {section_index + 1}: {section['section_name']}")
    print(f"Target: {section['word_target']} words")
    print(f"Using 3-stage process: Write → Critique → Refine")
    print(f"{'='*70}")
    
    # STAGE 1: Write initial section
    print(f"\n📝 Stage 1: Writing initial section...")
    writer = SectionWritingWorker(config)
    writer.set_section_index(section_index)
    
    write_state = {
        "writing_context": writing_context,
        "section_index": section_index,
        "revision_mode": False,
    }
    
    write_output = writer.execute(write_state)
    if write_output.status != "completed":
        raise Exception(f"Writing failed: {write_output.notes}")
    
    initial_content = write_output.modifications["section_content"]
    initial_word_count = write_output.modifications["word_count"]
    print(f"✓ Initial draft complete: {initial_word_count} words")
    
    # STAGE 2: Critique the section
    print(f"\n🔍 Stage 2: Critiquing section...")
    critic = SectionCriticWorker(config)
    
    critique_state = {
        "writing_context": writing_context,
        "section_index": section_index,
        "current_section_content": initial_content,
    }
    
    critique_output = critic.execute(critique_state)
    if critique_output.status != "completed":
        raise Exception(f"Critique failed: {critique_output.notes}")
    
    critique_content = critique_output.modifications["content"]
    assessment = critique_output.modifications["summary_assessment"]
    major_issues = len(critique_output.modifications["critical_issues"].get("major", []))
    minor_issues = len(critique_output.modifications["critical_issues"].get("minor", []))
    
    print(f"✓ Critique complete: {assessment}")
    print(f"  Major issues: {major_issues}, Minor issues: {minor_issues}")
    
    # STAGE 3: Refine the section (if needed)
    final_content = initial_content
    final_word_count = initial_word_count
    changes_made = []
    
    if assessment in ["MAJOR_REVISION", "MINOR_REFINEMENT"]:
        print(f"\n✨ Stage 3: Refining section based on critique...")
        refiner = SectionRefinementWorker(config)
        
        refinement_state = {
            "writing_context": writing_context,
            "section_index": section_index,
            "current_section_content": initial_content,
            "current_critique": critique_content,
        }
        
        refinement_output = refiner.execute(refinement_state)
        if refinement_output.status != "completed":
            raise Exception(f"Refinement failed: {refinement_output.notes}")
        
        final_content = refinement_output.modifications["refined_section_content"]
        final_word_count = refinement_output.modifications["word_count"]
        changes_made = refinement_output.modifications.get("changes_made", [])
        
        print(f"✓ Refinement complete: {final_word_count} words, {len(changes_made)} changes made")
    else:
        print(f"\n✨ Stage 3: Skipping refinement (assessment: {assessment})")
    
    return {
        "section_content": final_content,
        "word_count": final_word_count,
        "initial_word_count": initial_word_count,
        "assessment": assessment,
        "major_issues": major_issues,
        "minor_issues": minor_issues,
        "changes_made": changes_made,
        "refined": assessment in ["MAJOR_REVISION", "MINOR_REFINEMENT"]
    }


def save_progress(writing_context: Dict[str, Any], sections_data: List[Dict[str, Any]]) -> None:
    """Save progress to phase_3_1_progress.json"""
    
    sections_completed = len(sections_data)
    total_words = sum(section["word_count"] for section in sections_data)
    sections_refined = sum(1 for section in sections_data if section["refined"])
    
    progress_data = {
        "paper_overview": writing_context["paper_overview"],
        "sections": [
            {
                "section_name": writing_context["sections"][i]["section_name"],
                "target_words": writing_context["sections"][i]["word_target"],
                "actual_words": sections_data[i]["word_count"],
                "initial_words": sections_data[i]["initial_word_count"],
                "assessment": sections_data[i]["assessment"],
                "major_issues": sections_data[i]["major_issues"],
                "minor_issues": sections_data[i]["minor_issues"],
                "changes_made": len(sections_data[i]["changes_made"]),
                "refined": sections_data[i]["refined"]
            }
            for i in range(len(sections_data))
        ],
        "metadata": {
            "sections_completed": sections_completed,
            "total_sections": len(writing_context["sections"]),
            "total_words": total_words,
            "target_words": writing_context["paper_overview"]["target_words"],
            "sections_refined": sections_refined,
            "completion_percentage": (sections_completed / len(writing_context["sections"])) * 100
        }
    }
    
    with open("./outputs/phase_3_1_progress.json", "w") as f:
        json.dump(progress_data, f, indent=2)
    
    print(f"📄 Progress saved to: ./outputs/phase_3_1_progress.json")
    print(f"   Sections completed: {sections_completed}/{len(writing_context['sections'])}")
    print(f"   Words written: {total_words}")
    print(f"   Sections refined: {sections_refined}")


def create_complete_draft(writing_context: Dict[str, Any], sections_data: List[Dict[str, Any]]) -> str:
    """Create the complete draft paper from all sections"""
    
    # Start with the paper title (from thesis)
    paper_title = writing_context["paper_overview"]["thesis"]
    
    # Build the complete paper
    paper_parts = [f"# {paper_title}"]
    
    for i, section_data in enumerate(sections_data):
        section_content = section_data["section_content"]
        paper_parts.append(section_content)
    
    return "\n\n".join(paper_parts)


def run_phase_3_1():
    """Run Phase III.1: Section-by-section writing with critique and refinement"""
    
    start_time = time.time()
    
    print("\n" + "="*70)
    print("PHASE III.1: Section-by-Section Writing")
    print("="*70)
    print("\nGenerating complete draft paper using 3-stage process:")
    print("  Stage 1: Write initial section")
    print("  Stage 2: Critique section quality")
    print("  Stage 3: Refine based on feedback")
    
    try:
        # Load configuration and writing context
        print("\n1. Loading configuration and writing context...")
        config = load_config()
        writing_context = load_writing_context()
        
        sections = writing_context["sections"]
        print(f"   ✓ Found {len(sections)} sections to process")
        print(f"   ✓ Target paper length: {writing_context['paper_overview']['target_words']} words")
        
        # Process each section through the full pipeline
        sections_processed = []
        total_words = 0
        total_refined = 0
        
        for i, section in enumerate(sections):
            section_data = process_section_with_critique(writing_context, i, config)
            sections_processed.append(section_data)
            
            # Update running totals
            total_words += section_data["word_count"]
            if section_data["refined"]:
                total_refined += 1
            
            # Calculate target difference
            target = section["word_target"]
            actual = section_data["word_count"]
            diff = actual - target
            diff_str = f"+{diff}" if diff > 0 else str(diff)
            
            print(f"\n🎯 Section {i + 1} complete: {actual} words")
            print(f"   ✓ Section {i + 1} complete: {actual} words")
            print(f"   ✓ Running total: {total_words} words")
            
            # Save progress after each section
            save_progress(writing_context, sections_processed)
        
        # Create complete draft paper
        print("\n2. Creating complete draft paper...")
        complete_draft = create_complete_draft(writing_context, sections_processed)
        
        # Save the draft
        with open("./outputs/phase_3_1_draft.md", "w") as f:
            f.write(complete_draft)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n✓ Phase III.1 complete!")
        print(f"\n📋 FINAL SUMMARY:")
        print(f"   Sections processed: {len(sections_processed)}")
        print(f"   Total words: {total_words}")
        print(f"   Target words: {writing_context['paper_overview']['target_words']}")
        print(f"   Sections refined: {total_refined}")
        print(f"   Draft saved to: ./outputs/phase_3_1_draft.md")
        print(f"⏱️  Phase III.1 duration: {duration:.1f} seconds ({duration/60:.1f} minutes)")
        
        # Print section analysis
        print(f"\n📊 SECTION ANALYSIS:")
        for i, (section, section_data) in enumerate(zip(sections, sections_processed)):
            target = section["word_target"]
            actual = section_data["word_count"]
            diff = actual - target
            diff_str = f"+{diff}" if diff > 0 else str(diff)
            assessment = section_data["assessment"]
            
            print(f"   ✨ {section['section_name']}: {actual} words (target: {target}, diff: {diff_str}) [{assessment}]")
        
    except Exception as e:
        print(f"\n❌ Phase III.1 failed: {str(e)}")
        raise


if __name__ == "__main__":
    run_phase_3_1() 