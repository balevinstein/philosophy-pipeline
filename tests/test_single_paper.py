#!/usr/bin/env python3
"""Test enhanced Phase II.1 on a single paper"""

from pathlib import Path
import json
import sys

from run_utils import load_final_selection, setup_logging
from src.phases.phase_two.stages.stage_one.lit_processor import InitialReader


def test_single_paper():
    """Test the enhanced PDF reading on a single paper"""
    print("Testing enhanced Phase II.1 on single paper...")
    setup_logging()
    
    # Load Phase I output
    final_selection = load_final_selection()
    
    # Get a single PDF to test
    papers_dir = Path("./papers")
    pdfs = list(papers_dir.glob("*.pdf"))
    
    if not pdfs:
        print("No PDFs found in ./papers directory")
        return
    
    # Use the first PDF for testing
    test_pdf = pdfs[0]
    print(f"\nTesting with: {test_pdf.name}")
    
    # Load config
    config = {
        "models": {
            "initialreader": {
                "provider": "anthropic",
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 8192,
                "temperature": 0.3,
            }
        }
    }
    
    # Create reader and test
    reader = InitialReader(config)
    
    # Prepare state
    state = {
        "current_paper": test_pdf,
        "final_selection": final_selection
    }
    
    try:
        # Run the enhanced two-stage reading
        print("\nRunning enhanced two-stage reading...")
        result = reader.run(state)
        
        # Check if we got quotes
        if "initial_reading" in result.modifications:
            reading = result.modifications["initial_reading"]
            
            # Check for extracted quotes
            if "extracted_quotes" in reading:
                quotes = reading["extracted_quotes"]
                print(f"\n✓ Successfully extracted {len(quotes)} quotes")
                
                # Show first quote as example
                if quotes:
                    print(f"\nExample quote:")
                    print(f"  Text: {quotes[0].get('text', 'N/A')[:100]}...")
                    print(f"  Page: {quotes[0].get('page', 'N/A')}")
                    print(f"  Type: {quotes[0].get('type', 'N/A')}")
            else:
                print("\n✗ No extracted_quotes field found")
            
            # Check other key fields
            if "thesis" in reading:
                print(f"\n✓ Thesis extracted")
                print(f"  Statement: {reading['thesis'].get('statement', 'N/A')[:100]}...")
            
            if "engagement_opportunities" in reading:
                print(f"\n✓ Found {len(reading['engagement_opportunities'])} engagement opportunities")
            
            # Save result for inspection
            output_path = Path("test_output.json")
            with open(output_path, "w") as f:
                json.dump(reading, f, indent=2)
            print(f"\nFull output saved to: {output_path}")
            
            print("\n✓ Test completed successfully!")
            
        else:
            print("\n✗ No initial_reading in result")
            
    except Exception as e:
        print(f"\n✗ Error during test: {str(e)}")
        import traceback
        traceback.print_exc()
        

if __name__ == "__main__":
    test_single_paper() 