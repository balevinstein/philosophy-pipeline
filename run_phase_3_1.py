import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List

from src.phases.phase_three.stages.stage_one.workers.writing.section_writer import SectionWritingWorker
from src.phases.phase_three.stages.stage_one.workers.critic.section_critic import SectionCriticWorker
from src.phases.phase_three.stages.stage_one.workers.refinement.section_refinement import SectionRefinementWorker
from src.utils.api import load_config


def load_writing_context() -> Dict[str, Any]:
    """Load the writing context created by Phase II.6"""
    try:
        with open("./outputs/phase_3_writing_context.json") as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValueError("Could not find phase_3_writing_context.json. Run Phase II.6 first.")


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
    
    # STAGE 3: Refine based on critique (if needed)
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
            print(f"⚠️  Refinement failed: {refinement_output.notes}")
            print("Using initial version instead...")
            final_section = write_output.modifications
        else:
            # Use refined version
            final_section = {
                "section_content": refinement_output.modifications["refined_section_content"],
                "word_count": refinement_output.modifications["word_count"],
                "content_bank_usage": refinement_output.modifications["content_bank_usage"],
                "section_notes": refinement_output.modifications["refinement_notes"],
                "transition_points": refinement_output.modifications["transition_points"],
                "changes_made": refinement_output.modifications["changes_made"],
                "refined": True
            }
            
            changes_count = len(refinement_output.modifications["changes_made"])
            refined_word_count = refinement_output.modifications["word_count"]
            print(f"✓ Refinement complete: {refined_word_count} words, {changes_count} changes made")
    else:
        print(f"\n✅ Stage 3: Minimal changes needed - using initial version")
        final_section = write_output.modifications
        final_section["refined"] = False
    
    # Add critique metadata
    final_section["critique_assessment"] = assessment
    final_section["major_issues_found"] = major_issues
    final_section["minor_issues_found"] = minor_issues
    
    final_word_count = final_section["word_count"]
    print(f"\n🎯 Section {section_index + 1} complete: {final_word_count} words")
    
    return final_section


def save_section_progress(sections_processed: List[Dict[str, Any]], writing_context: Dict[str, Any]):
    """Save progress after each section with critique metadata"""
    
    # Calculate statistics
    total_words = sum(s.get("word_count", 0) for s in sections_processed)
    refined_count = sum(1 for s in sections_processed if s.get("refined", False))
    major_issues_total = sum(s.get("major_issues_found", 0) for s in sections_processed)
    
    # Create comprehensive output structure
    paper_progress = {
        "metadata": {
            "timestamp": "2024-01-01T00:00:00",  # Would be actual timestamp
            "phase": "III.1",
            "stage": "section_writing_with_critique",
            "sections_completed": len(sections_processed),
            "total_sections": len(writing_context["sections"]),
            "total_words_written": total_words,
            "target_total_words": writing_context["paper_overview"]["target_words"],
            "sections_refined": refined_count,
            "total_major_issues": major_issues_total
        },
        "paper_overview": writing_context["paper_overview"],
        "sections": []
    }
    
    # Add each completed section
    for i, section_data in enumerate(sections_processed):
        if section_data:  # Only add completed sections
            section_info = writing_context["sections"][i].copy()
            section_info.update({
                "section_index": i,
                "content": section_data["section_content"],
                "actual_word_count": section_data["word_count"],
                "content_bank_usage": section_data["content_bank_usage"],
                "notes": section_data["section_notes"],
                "transitions": section_data["transition_points"],
                "was_refined": section_data.get("refined", False),
                "critique_assessment": section_data.get("critique_assessment", "UNKNOWN"),
                "major_issues_found": section_data.get("major_issues_found", 0),
                "minor_issues_found": section_data.get("minor_issues_found", 0),
                "changes_made": section_data.get("changes_made", [])
            })
            paper_progress["sections"].append(section_info)
    
    # Save progress
    progress_file = "./outputs/phase_3_1_progress.json"
    with open(progress_file, "w") as f:
        json.dump(paper_progress, f, indent=2)
    
    print(f"\n📄 Progress saved to: {progress_file}")
    print(f"   Sections completed: {len(sections_processed)}/{len(writing_context['sections'])}")
    print(f"   Words written: {total_words}")
    print(f"   Sections refined: {refined_count}")


def create_draft_paper(sections_processed: List[Dict[str, Any]], writing_context: Dict[str, Any]) -> str:
    """Combine all sections into a complete draft paper"""
    
    paper_parts = []
    
    # Add title and abstract - use full thesis, not truncated
    paper_parts.append(f"# {writing_context['paper_overview']['thesis']}\n")
    paper_parts.append("## Abstract\n")
    paper_parts.append(f"{writing_context['paper_overview']['abstract']}\n")
    
    # Add each section
    for i, section_data in enumerate(sections_processed):
        if section_data:
            section_name = writing_context["sections"][i]["section_name"]
            paper_parts.append(f"\n## {section_name}\n")
            paper_parts.append(f"{section_data['section_content']}\n")
    
    return "\n".join(paper_parts)


def run_phase_3_1():
    """Run Phase III.1: Section-by-section writing with critique and refinement"""
    
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
        
        for i in range(len(sections)):
            try:
                section_result = process_section_with_critique(writing_context, i, config)
                sections_processed.append(section_result)
                
                words_this_section = section_result.get("word_count", 0)
                total_words += words_this_section
                
                if section_result.get("refined", False):
                    total_refined += 1
                
                print(f"   ✓ Section {i+1} complete: {words_this_section} words")
                print(f"   ✓ Running total: {total_words} words")
                
                # Save progress after each section
                save_section_progress(sections_processed, writing_context)
                
            except Exception as e:
                print(f"\n❌ Error processing section {i+1}: {str(e)}")
                print("Saving progress up to this point...")
                save_section_progress(sections_processed, writing_context)
                sys.exit(1)
        
        # Create complete draft
        print(f"\n2. Creating complete draft paper...")
        draft_paper = create_draft_paper(sections_processed, writing_context)
        
        # Save final draft
        draft_file = "./outputs/phase_3_1_draft.md"
        with open(draft_file, "w") as f:
            f.write(draft_paper)
        
        print(f"\n✓ Phase III.1 complete!")
        print(f"\n📋 FINAL SUMMARY:")
        print(f"   Sections processed: {len(sections_processed)}")
        print(f"   Total words: {total_words}")
        print(f"   Target words: {writing_context['paper_overview']['target_words']}")
        print(f"   Sections refined: {total_refined}")
        print(f"   Draft saved to: {draft_file}")
        
        # Calculate word distribution and refinement stats
        print(f"\n📊 SECTION ANALYSIS:")
        for i, section_data in enumerate(sections_processed):
            section_name = sections[i]["section_name"]
            actual_words = section_data.get("word_count", 0)
            target_words = sections[i]["word_target"]
            diff = actual_words - target_words
            refined = "✨" if section_data.get("refined", False) else "📝"
            assessment = section_data.get("critique_assessment", "UNKNOWN")
            
            print(f"   {refined} {section_name}: {actual_words} words (target: {target_words}, diff: {diff:+d}) [{assessment}]")
        
        return {
            "sections_processed": len(sections_processed),
            "total_words": total_words,
            "sections_refined": total_refined,
            "draft_file": draft_file,
            "success": True
        }
        
    except Exception as e:
        print(f"\n❌ Error in Phase III.1: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    run_phase_3_1() 