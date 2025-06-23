#!/usr/bin/env python3
"""
Archive pipeline outputs after each run for quality tracking
"""

import os
import json
import shutil
from datetime import datetime
import argparse

class PipelineArchiver:
    def __init__(self, archive_root="outputs/archive"):
        self.archive_root = archive_root
        os.makedirs(self.archive_root, exist_ok=True)
        
    def archive_run(self, run_name=None, notes=""):
        """Archive key outputs from a pipeline run"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if run_name:
            # Sanitize run name
            run_name = run_name.replace(" ", "_").replace("/", "_")
        else:
            run_name = f"run_{timestamp}"
            
        archive_path = os.path.join(self.archive_root, run_name)
        os.makedirs(archive_path, exist_ok=True)
        
        # Files to archive (with graceful handling if missing)
        files_to_archive = {
            # Final outputs
            "outputs/final_paper.md": "final_paper.md",
            "outputs/final_paper_metadata.json": "final_paper_metadata.json",
            
            # Key intermediate files  
            "outputs/final_selection.json": "topic_selection.json",
            "outputs/literature_synthesis.json": "literature_synthesis.json",
            "outputs/framework_development/abstract_framework.json": "abstract_framework.json",
            "outputs/key_moves_development/key_moves_development/all_developed_moves.json": "key_moves.json",
            "outputs/detailed_outline/detailed_outline_final.json": "detailed_outline.json",
            
            # Phase II.5 Consolidation
            "outputs/phase_2_5_consolidated_context.json": "phase_2_5_consolidated_context.json",
            "outputs/debug_consolidation_response.txt": "debug_consolidation_response.txt",
            
            # Phase II.6 Review
            "outputs/paper_vision_review/referee_report.json": "paper_vision_review/referee_report.json",
            "outputs/paper_vision_review/final_writing_plan.json": "paper_vision_review/final_writing_plan.json",
            
            # Phase 3 drafts
            "outputs/phase_3_1_draft.md": "phase_3_1_draft.md",
            "outputs/phase_3_1_progress.json": "phase_3_1_progress.json",
            
            # Config used
            "config/conceptual_config.yaml": "config_used.yaml"
        }
        
        # Copy files and track what was archived
        archived_files = []
        missing_files = []
        
        for source, dest in files_to_archive.items():
            if os.path.exists(source):
                dest_path = os.path.join(archive_path, dest)
                # Create subdirectories if needed
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(source, dest_path)
                archived_files.append(source)
            else:
                missing_files.append(source)
                
        # Auto-analyze paper if it exists
        paper_stats = None
        if os.path.exists("outputs/final_paper.md"):
            paper_stats = self._analyze_paper("outputs/final_paper.md")
            
        # Create metadata
        metadata = {
            "timestamp": timestamp,
            "run_name": run_name,
            "notes": notes,
            "files_archived": archived_files,
            "files_missing": missing_files,
            "paper_stats": paper_stats,
            "archive_path": archive_path
        }
        
        # Save metadata
        metadata_path = os.path.join(archive_path, "archive_metadata.json")
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
            
        # Print summary
        print(f"\n=== Archive Summary ===")
        print(f"Run Name: {run_name}")
        print(f"Archived to: {archive_path}")
        print(f"Files archived: {len(archived_files)}")
        print(f"Files missing: {len(missing_files)}")
        
        if paper_stats:
            print(f"\nPaper Statistics:")
            print(f"  Word count: {paper_stats['word_count']}")
            print(f"  Citations: ~{paper_stats['citation_count']}")
            print(f"  Sections: {paper_stats['section_count']}")
            
        if missing_files:
            print(f"\nWarning: Some files were missing:")
            for f in missing_files[:5]:  # Show first 5
                print(f"  - {f}")
                
        return archive_path
        
    def _analyze_paper(self, paper_path):
        """Auto-analyze paper statistics"""
        try:
            with open(paper_path, 'r') as f:
                content = f.read()
                
            # Count various elements (rough but useful)
            stats = {
                'word_count': len(content.split()),
                'citation_count': content.count('(19') + content.count('(20'),
                'quote_count': content.count('"') // 2,
                'section_count': content.count('\n##'),
                'subsection_count': content.count('\n###'),
                'has_abstract': 'Abstract' in content or 'abstract' in content,
                'has_objections': 'Objection' in content or 'objection' in content,
                'references_count': content.count('\n- ') if 'References' in content else 0
            }
            return stats
        except Exception as e:
            print(f"Error analyzing paper: {e}")
            return None
            
    def list_archives(self):
        """List all archived runs"""
        archives = []
        for run_dir in os.listdir(self.archive_root):
            metadata_path = os.path.join(self.archive_root, run_dir, "archive_metadata.json")
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                archives.append({
                    'run_name': run_dir,
                    'timestamp': metadata.get('timestamp'),
                    'notes': metadata.get('notes'),
                    'word_count': metadata.get('paper_stats', {}).get('word_count') if metadata.get('paper_stats') else None
                })
                
        # Sort by timestamp
        archives.sort(key=lambda x: x['timestamp'], reverse=True)
        
        print("\n=== Archived Runs ===")
        for arch in archives:
            wc = f"({arch['word_count']} words)" if arch['word_count'] else "(no paper)"
            notes = f" - {arch['notes']}" if arch['notes'] else ""
            print(f"{arch['run_name']} - {arch['timestamp']} {wc}{notes}")
            
        return archives


def main():
    parser = argparse.ArgumentParser(description="Archive pipeline outputs")
    parser.add_argument("--name", help="Name for this run (e.g., 'enhanced_pdf_test')")
    parser.add_argument("--notes", help="Notes about this run", default="")
    parser.add_argument("--list", action="store_true", help="List all archived runs")
    
    args = parser.parse_args()
    
    archiver = PipelineArchiver()
    
    if args.list:
        archiver.list_archives()
    else:
        archiver.archive_run(run_name=args.name, notes=args.notes)


if __name__ == "__main__":
    main() 