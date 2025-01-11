# test_literature.py

import sys
from pathlib import Path
import json
import logging
from typing import Dict, Any

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from src.phases.phase_two.stages.stage_one.lit_processor import LiteratureProcessor
from src.utils.json_utils import JSONHandler
from src.utils.api import APIHandler

def setup_logging():
    """Configure logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def load_test_config() -> Dict[str, Any]:
    """Load minimal config for testing"""
    return {
        "paths": {
            "papers_dir": "./papers",
            "output_dir": "./test_outputs"
        },
        "models": {
            "literature_processing": {
                "provider": "anthropic",
                "model": "claude-3-5-sonnet-20241022",
                "max_tokens": 8192,
                "temperature": 0.5
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
        raise ValueError("Please create ./papers directory and add test PDF")
    
    pdf_files = list(papers_dir.glob("*.pdf"))
    if not pdf_files:
        raise ValueError("No PDF files found in ./papers directory")
    
    print(f"Found {len(pdf_files)} PDF files:")
    for pdf in pdf_files:
        print(f"- {pdf.name}")
    
    return pdf_files[0]  # Return first PDF for testing

def test_literature_processing(test_pdf: Path):
    """Test complete literature processing pipeline"""
    config = load_test_config()
    processor = LiteratureProcessor(config)
    
    # Create minimal state for testing
    test_state = {
        "current_thesis": "Exploring the relationship between epistemic deference and chance",
        "core_contribution": "Developing a new framework for understanding epistemic deference",
        "key_moves": [
            "Distinguish types of deference",
            "Analyze relationship to chance"
        ]
    }
    
    print(f"\nProcessing paper: {test_pdf.name}")
    
    try:
        # Run processor
        result = processor.run(test_state)
        
        # Save results
        output_file = Path("./test_outputs/processed_literature.json")
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
            
        print(f"\nResults saved to: {output_file}")
        
        # Print summary
        if "literature_processed" in result:
            processed = result["literature_processed"]
            print("\nProcessing Summary:")
            print(f"Title: {processed['paper_info']['title']}")
            print("\nKey Arguments:")
            for arg in processed['core_content']['key_arguments']:
                print(f"- {arg['claim']}")
                print(f"  Confidence: {arg['confidence']}")
            
            print("\nEngagement Points:")
            for point in processed['engagement_points']:
                print(f"- {point['topic']}")
                
            print("\nConfidence Assessment:")
            for aspect, level in processed['analysis_notes']['confidence_assessment'].items():
                print(f"- {aspect}: {level}")
                
    except Exception as e:
        print(f"\nError during processing: {str(e)}")
        raise

def main():
    print("Starting Literature Processing Test")
    setup_logging()
    
    try:
        # Setup and run test
        test_pdf = setup_test_environment()
        test_literature_processing(test_pdf)
        
        print("\nTest completed successfully!")
        
    except Exception as e:
        print(f"\nTest failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()