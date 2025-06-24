#!/usr/bin/env python3
"""
Compare extracted philosophical moves with source text for quality validation
"""

import json
from pathlib import Path


def load_paper_text(filename):
    """Load the extracted text of a paper"""
    path = Path(f"analysis_cache/extracted_texts/{filename}")
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return None


def find_quote_in_text(quote, text):
    """Find where a quote appears in the source text"""
    # Clean up quote and text for comparison
    clean_quote = " ".join(quote.split())
    
    # Try to find exact match first
    if clean_quote in text:
        start = text.index(clean_quote)
        # Get surrounding context (200 chars before and after)
        context_start = max(0, start - 200)
        context_end = min(len(text), start + len(clean_quote) + 200)
        return text[context_start:context_end]
    
    # Try to find partial match (first 50 chars)
    partial = clean_quote[:50]
    if partial in text:
        start = text.index(partial)
        context_start = max(0, start - 200)
        context_end = min(len(text), start + 500)
        return text[context_start:context_end]
    
    return None


def validate_single_paper():
    """Validate moves from a single paper"""
    
    # Load extractions
    with open("outputs/philosophical_moves_db/raw_extractions.json", "r") as f:
        extractions = json.load(f)
    
    if not extractions:
        print("No extractions found!")
        return
    
    # Show available papers
    print("Available papers:")
    for i, ext in enumerate(extractions):
        if ext:
            print(f"{i+1}. {ext.get('paper_info', {}).get('title', 'Unknown')} "
                  f"({ext.get('source_file', 'Unknown')})")
    
    # Select paper
    choice = int(input("\nSelect paper number: ")) - 1
    extraction = extractions[choice]
    
    # Load source text
    source_file = extraction.get('source_file')
    text = load_paper_text(source_file)
    
    if not text:
        print(f"Could not load source text for {source_file}")
        return
    
    print(f"\n📄 Validating: {extraction['paper_info']['title']}")
    print(f"📊 Total moves extracted: {len(extraction['philosophical_moves'])}")
    
    # Check each move
    accurate_count = 0
    for i, move in enumerate(extraction['philosophical_moves']):
        print(f"\n{'='*60}")
        print(f"Move {i+1}: {move['move_name']}")
        print(f"Categories: {', '.join(move['categories'])}")
        print(f"Pattern: {move['transferable_pattern']}")
        
        # Find quote in source
        context = find_quote_in_text(move['quote'], text)
        
        if context:
            print("✅ Quote found in source!")
            accurate_count += 1
        else:
            print("❌ Quote not found exactly as extracted")
            print(f"Extracted quote: {move['quote'][:100]}...")
        
        # Quick manual check option
        check = input("\nDoes this look like a valid philosophical move? (y/n/s to skip): ")
        if check.lower() == 's':
            break
    
    print(f"\n📊 Validation Summary:")
    print(f"Quotes found in source: {accurate_count}/{len(extraction['philosophical_moves'])}")


if __name__ == "__main__":
    validate_single_paper() 