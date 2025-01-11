# test_literature_processing.py

import sys
from pathlib import Path
import json
import logging
from typing import Dict, Any, List

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from src.phases.phase_two.stages.stage_one.lit_processor import (
    LiteratureManager,
    InitialReader,
    ProjectSpecificReader,
    LiteratureSynthesizer
)
from src.utils.json_utils import JSONHandler

def setup_logging():
    """Configure logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def load_config() -> Dict[str, Any]:
    """Load test configuration"""
    return {
        "paths": {
            "papers_dir": "./papers",
            "output_dir": "./test_outputs",
            "literature_output": {
                "initial_readings": "initial_paper_readings.json",
                "project_readings": "project_specific_readings.json",
                "synthesis": {
                    "json": "literature_synthesis.json",
                    "markdown": "literature_synthesis.md"
                }
            }
        },
        "models": {
            "literature_processing": {
                "provider": "anthropic",
                "model": "claude-3-5-sonnet-20241022",
                "max_tokens": 8192,
                "temperature": 0.5
            }
        },
        "parameters": {
            "literature_processing": {
                "max_retries": 3,
                "min_wait": 4,
                "max_wait": 60
            }
        }
    }

def setup_test_environment():
    """Create necessary directories and verify test data"""
    print("\nSetting up test environment...")
    
    # Create output directory
    Path("./test_outputs").mkdir(exist_ok=True)
    
    # Check for test PDFs
    papers_dir = Path("./papers")
    if not papers_dir.exists():
        raise ValueError("Please create ./papers directory and add test PDFs")
    
    pdf_files = list(papers_dir.glob("*.pdf"))
    if not pdf_files:
        raise ValueError("No PDF files found in ./papers directory")
    
    print(f"Found {len(pdf_files)} PDF files:")
    for pdf in pdf_files:
        print(f"- {pdf.name}")
    
    # Load final_selection
    try:
        with open("./outputs/final_selection.json") as f:
            final_selection = json.load(f)
        print("\nLoaded final_selection.json")
    except FileNotFoundError:
        raise ValueError("Could not find final_selection.json")
    
    return pdf_files, final_selection

def test_literature_processing(pdfs: List[Path], final_selection: Dict):
    """Test complete literature processing pipeline"""
    config = load_config()
    manager = LiteratureManager(config)
    
    print("\nStarting literature processing...")
    
    try:
        # Process all papers through pipeline
        result = manager.process_papers(pdfs, final_selection)
        
        # Save results
        output_dir = Path("./test_outputs")
        
        # Extract actual data from WorkerOutput objects
        paper_readings = {
            paper_id: {
                "initial": reading["initial"].modifications["initial_reading"],
                "project_specific": reading["project_specific"].modifications["project_specific_reading"]
            }
            for paper_id, reading in result['paper_readings'].items()
        }
        
        # Save paper readings
        with open(output_dir / config['paths']['literature_output']['initial_readings'], 'w') as f:
            json.dump(paper_readings, f, indent=2)
            
        # Save synthesis separately
        if 'synthesis' in result:
            synthesis_data = result['synthesis'].modifications['literature_synthesis']
            
            with open(output_dir / config['paths']['literature_output']['synthesis']['json'], 'w') as f:
                json.dump(synthesis_data['structured_data'], f, indent=2)
                
            with open(output_dir / config['paths']['literature_output']['synthesis']['markdown'], 'w') as f:
                f.write(synthesis_data['narrative_analysis'])
            
        print("\nResults saved to test_outputs/")
        
        # Print summary
        print("\nProcessing Summary:")
        print(f"Papers processed: {len(pdfs)}")
        if 'synthesis' in result:
            synthesis_data = result['synthesis'].modifications['literature_synthesis']
            structured = synthesis_data['structured_data']
            
            print("\nPaper Classifications:")
            print(f"Primary papers: {len(structured.get('literature_overview', {}).get('primary_papers', []))}")
            print(f"Supporting papers: {len(structured.get('literature_overview', {}).get('supporting_papers', []))}")
            print(f"Background papers: {len(structured.get('literature_overview', {}).get('background_papers', []))}")
            
            # Use .get() for safer dictionary access
            print("\nKey concepts identified:", len(structured.get('key_concepts', [])))
            print("Engagement priorities:", len(structured.get('engagement_priorities', [])))
            
    except Exception as e:
        print(f"\nError during processing: {str(e)}")
        raise

def main():
    print("Starting Literature Processing Test")
    setup_logging()
    
    try:
        # Setup and run test
        pdfs, final_selection = setup_test_environment()
        test_literature_processing(pdfs, final_selection)
        
        print("\nTest completed successfully!")
        
    except Exception as e:
        print(f"\nTest failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()