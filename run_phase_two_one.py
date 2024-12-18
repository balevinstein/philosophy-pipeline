# run_phase_two_one.py

import sys
from pathlib import Path
import json
import logging
from typing import Dict, Any

from src.stages.phase_two.stages.stage_one.lit_processor import (
    LiteratureManager
)

def setup_logging():
    """Configure logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def load_final_selection() -> Dict[str, Any]:
    """Load final selection from Phase I"""
    try:
        with open("./outputs/final_selection.json") as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValueError("Could not find final_selection.json. Run Phase I first.")

def main():
    print("Starting Phase II.1: Literature Processing")
    setup_logging()
    
    try:
        # Load Phase I output
        final_selection = load_final_selection()
        
        # Get PDFs
        papers_dir = Path("./papers")
        if not papers_dir.exists():
            raise ValueError("Please create ./papers directory and add required PDFs")
        
        pdfs = list(papers_dir.glob("*.pdf"))
        if not pdfs:
            raise ValueError("No PDFs found in ./papers directory")
            
        print(f"\nFound {len(pdfs)} PDF files:")
        for pdf in pdfs:
            print(f"- {pdf.name}")
            
        # Load config and process papers
        config = {
            "paths": {
                "papers_dir": "./papers",
                "output_dir": "./outputs",
                "literature_output": {
                    "initial_readings": "literature_readings.json",
                    "synthesis": {
                        "json": "literature_synthesis.json",
                        "markdown": "literature_synthesis.md"
                    }
                }
            },
            "models": {
                "initialreader": {
                    "provider": "anthropic",
                    "model": "claude-3-5-sonnet-20241022",
                    "max_tokens": 8192,
                    "temperature": 0.3
                },
                "projectspecificreader": {
                    "provider": "anthropic",
                    "model": "claude-3-5-sonnet-20241022",
                    "max_tokens": 8192,
                    "temperature": 0.5
                },
                "literaturesynthesizer": {
                    "provider": "anthropic",
                    "model": "claude-3-5-sonnet-20241022",
                    "max_tokens": 8192,
                    "temperature": 0.7
                }
            }
        }
        
        manager = LiteratureManager(config)
        result = manager.process_papers(pdfs, final_selection)
        
        # Save outputs properly
        output_dir = Path("./outputs")
        
        # Extract and save paper readings
        paper_readings = {
            paper_id: {
                "initial": reading["initial"].modifications["initial_reading"],
                "project_specific": reading["project_specific"].modifications["project_specific_reading"]
            }
            for paper_id, reading in result['paper_readings'].items()
        }
        
        with open(output_dir / "literature_readings.json", 'w') as f:
            json.dump(paper_readings, f, indent=2)
            
        # Save synthesis
        if 'synthesis' in result:
            synthesis_data = result['synthesis'].modifications['literature_synthesis']
            
            with open(output_dir / "literature_synthesis.json", 'w') as f:
                json.dump(synthesis_data['structured_data'], f, indent=2)
                
            with open(output_dir / "literature_synthesis.md", 'w') as f:
                f.write(synthesis_data['narrative_analysis'])
        
        print("\nPhase II.1 completed successfully!")
        print("\nOutputs saved to:")
        print("- outputs/literature_readings.json")
        print("- outputs/literature_synthesis.json")
        print("- outputs/literature_synthesis.md")
        
    except Exception as e:
        print(f"\nError during Phase II.1: {str(e)}")
        raise

if __name__ == "__main__":
    main()