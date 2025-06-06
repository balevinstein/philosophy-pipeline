#!/usr/bin/env python3
"""
Validate the quality of philosophical moves extraction by comparing with manual analysis
"""

import json
from pathlib import Path
import random


def load_extraction_results():
    """Load the extracted moves database"""
    db_path = Path("outputs/philosophical_moves_db/raw_extractions.json")
    if db_path.exists():
        with open(db_path, "r") as f:
            return json.load(f)
    return None


def display_move_for_validation(move, paper_info):
    """Display a move in a readable format for validation"""
    print("\n" + "="*80)
    print(f"📄 PAPER: {paper_info['title']}")
    print(f"👤 AUTHOR: {paper_info['author']}")
    print(f"📍 LOCATION: {move['location']}")
    print("\n📌 MOVE NAME: " + move['move_name'])
    print("🏷️  CATEGORIES: " + ", ".join(move['categories']))
    print("\n📝 QUOTE:")
    print("-" * 40)
    print(move['quote'])
    print("-" * 40)
    print(f"\n🎯 PATTERN: {move['transferable_pattern']}")
    print(f"⚙️  MECHANISM: {move['mechanism']}")
    print(f"✅ ACHIEVEMENT: {move['achievement']}")
    print(f"💪 EFFECTIVENESS: {move['effectiveness']}")
    print("="*80)


def validate_extractions():
    """Interactive validation of extraction quality"""
    
    extractions = load_extraction_results()
    if not extractions:
        print("❌ No extractions found. Run extract_philosophical_moves.py first.")
        return
    
    print("🔍 PHILOSOPHICAL MOVES EXTRACTION VALIDATION")
    print(f"📊 Loaded {len(extractions)} paper extractions")
    
    # Collect all moves with paper info
    all_moves = []
    for extraction in extractions:
        if extraction and 'philosophical_moves' in extraction:
            paper_info = extraction.get('paper_info', {})
            for move in extraction['philosophical_moves']:
                all_moves.append((move, paper_info))
    
    print(f"📊 Total moves to validate: {len(all_moves)}")
    
    # Sample validation approach
    print("\n🎲 Showing 5 random moves for spot-check validation:")
    print("(You can manually verify these against the original papers)")
    
    sample_moves = random.sample(all_moves, min(5, len(all_moves)))
    
    for i, (move, paper_info) in enumerate(sample_moves, 1):
        print(f"\n\n{'='*20} MOVE {i}/5 {'='*20}")
        display_move_for_validation(move, paper_info)
        
        # Show source file for manual verification
        source_file = extraction.get('source_file', 'Unknown')
        print(f"\n📂 Source file: analysis_cache/extracted_texts/{source_file}")
        print("💡 To verify: Check if the quote accurately represents a philosophical move")
        print("   and if the categorization/pattern extraction makes sense")
        
        input("\nPress Enter to continue to next move...")


def generate_validation_report():
    """Generate a report summarizing extraction patterns"""
    
    extractions = load_extraction_results()
    if not extractions:
        return
    
    report = {
        'total_papers': len(extractions),
        'total_moves': 0,
        'moves_per_paper': [],
        'category_distribution': {},
        'effectiveness_distribution': {},
        'originality_distribution': {},
        'sample_patterns': []
    }
    
    all_patterns = set()
    
    for extraction in extractions:
        if extraction and 'philosophical_moves' in extraction:
            moves = extraction['philosophical_moves']
            report['total_moves'] += len(moves)
            report['moves_per_paper'].append(len(moves))
            
            for move in moves:
                # Category distribution
                for cat in move.get('categories', []):
                    report['category_distribution'][cat] = \
                        report['category_distribution'].get(cat, 0) + 1
                
                # Effectiveness distribution
                eff = move.get('effectiveness', 'Unknown')
                report['effectiveness_distribution'][eff] = \
                    report['effectiveness_distribution'].get(eff, 0) + 1
                
                # Originality distribution
                orig = move.get('originality', 'Unknown')
                report['originality_distribution'][orig] = \
                    report['originality_distribution'].get(orig, 0) + 1
                
                # Collect patterns
                pattern = move.get('transferable_pattern', '')
                if pattern:
                    all_patterns.add(pattern)
    
    # Sample some patterns
    report['sample_patterns'] = list(all_patterns)[:10]
    
    # Calculate averages
    if report['moves_per_paper']:
        report['avg_moves_per_paper'] = \
            sum(report['moves_per_paper']) / len(report['moves_per_paper'])
    
    # Save report
    with open("outputs/philosophical_moves_db/validation_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print("\n📊 VALIDATION SUMMARY REPORT")
    print(f"Papers analyzed: {report['total_papers']}")
    print(f"Total moves extracted: {report['total_moves']}")
    print(f"Average moves per paper: {report.get('avg_moves_per_paper', 0):.1f}")
    print("\nCategory distribution:")
    for cat, count in sorted(report['category_distribution'].items(), 
                            key=lambda x: x[1], reverse=True):
        print(f"  - {cat}: {count}")
    print(f"\nUnique patterns identified: {len(all_patterns)}")


if __name__ == "__main__":
    print("Choose validation mode:")
    print("1. Interactive spot-check validation")
    print("2. Generate validation summary report")
    print("3. Both")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice in ['1', '3']:
        validate_extractions()
    
    if choice in ['2', '3']:
        generate_validation_report() 