#!/usr/bin/env python3
"""
Compare outputs before and after Hájek/RLHF improvements
"""

import json
from pathlib import Path
import difflib


def load_json_file(path):
    """Load JSON file if it exists"""
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return None


def compare_critic_feedback(baseline_path, improved_path):
    """Compare critic feedback between runs"""
    
    print("\n" + "="*80)
    print("CRITIC FEEDBACK COMPARISON")
    print("="*80)
    
    # Phase II.2 - Abstract Critics
    baseline_abstract = load_json_file(baseline_path / "abstract_refinement_history.json")
    improved_abstract = load_json_file(improved_path / "abstract_refinement_history.json")
    
    if baseline_abstract and improved_abstract:
        print("\n📋 ABSTRACT CRITICS:")
        
        # Get first cycle critiques
        baseline_critique = baseline_abstract.get("cycles", [{}])[0].get("critique", {})
        improved_critique = improved_abstract.get("cycles", [{}])[0].get("critique", {})
        
        print("\n🔴 BASELINE Abstract Critique Issues:")
        if baseline_critique:
            for issue_type, issues in baseline_critique.items():
                if isinstance(issues, list) and issues:
                    print(f"  - {issue_type}: {len(issues)} issues")
                    for issue in issues[:2]:  # Show first 2
                        print(f"    • {issue[:100]}...")
        
        print("\n🟢 IMPROVED Abstract Critique Issues:")
        if improved_critique:
            for issue_type, issues in improved_critique.items():
                if isinstance(issues, list) and issues:
                    print(f"  - {issue_type}: {len(issues)} issues")
                    for issue in issues[:2]:  # Show first 2
                        print(f"    • {issue[:100]}...")
    
    # Phase II.3 - Key Moves Critics
    baseline_moves = load_json_file(baseline_path / "key_moves_refinement_history.json")
    improved_moves = load_json_file(improved_path / "key_moves_refinement_history.json")
    
    if baseline_moves and improved_moves:
        print("\n\n📋 KEY MOVES CRITICS:")
        
        # Look for specific Hájek-style critiques
        baseline_moves_critique = baseline_moves.get("moves", [{}])[0].get("refinement_history", {}).get("cycles", [{}])[0].get("critique", {})
        improved_moves_critique = improved_moves.get("moves", [{}])[0].get("refinement_history", {}).get("cycles", [{}])[0].get("critique", {})
        
        # Check for extreme case testing
        print("\n🔍 Looking for Hájek Heuristics Application:")
        
        # Search for keywords in improved critique
        improved_text = json.dumps(improved_moves_critique).lower()
        hajek_keywords = ["extreme case", "boundary", "self-undermining", "counterexample", "edge case", "limit"]
        
        found_keywords = [kw for kw in hajek_keywords if kw in improved_text]
        print(f"  - Hájek keywords found in improved: {found_keywords}")
        
        baseline_text = json.dumps(baseline_moves_critique).lower()
        baseline_keywords = [kw for kw in hajek_keywords if kw in baseline_text]
        print(f"  - Hájek keywords in baseline: {baseline_keywords}")


def compare_philosophical_boldness(baseline_path, improved_path):
    """Check if RLHF-proofing made arguments bolder"""
    
    print("\n\n" + "="*80)
    print("PHILOSOPHICAL BOLDNESS COMPARISON (RLHF-Proofing)")
    print("="*80)
    
    # Check abstracts for hedging language
    baseline_abstract = load_json_file(baseline_path / "abstract_development_history.json")
    improved_abstract = load_json_file(improved_path / "abstract_development_history.json")
    
    if baseline_abstract and improved_abstract:
        baseline_text = baseline_abstract.get("cycles", [{}])[-1].get("content", {}).get("abstract_text", "")
        improved_text = improved_abstract.get("cycles", [{}])[-1].get("content", {}).get("abstract_text", "")
        
        # Count hedging phrases
        hedging_phrases = ["might", "perhaps", "arguably", "seems", "appears", "suggests", "could be", "may be", "possibly"]
        
        baseline_hedges = sum(1 for phrase in hedging_phrases if phrase in baseline_text.lower())
        improved_hedges = sum(1 for phrase in hedging_phrases if phrase in improved_text.lower())
        
        print(f"\n📊 Hedging Language in Abstracts:")
        print(f"  - Baseline: {baseline_hedges} hedging phrases")
        print(f"  - Improved: {improved_hedges} hedging phrases")
        print(f"  - Reduction: {baseline_hedges - improved_hedges} fewer hedges")
        
        # Look for bold claims
        bold_phrases = ["I argue", "demonstrates", "proves", "establishes", "shows that", "refutes"]
        
        baseline_bold = sum(1 for phrase in bold_phrases if phrase in baseline_text)
        improved_bold = sum(1 for phrase in bold_phrases if phrase in improved_text)
        
        print(f"\n💪 Bold Claims:")
        print(f"  - Baseline: {baseline_bold} bold phrases")
        print(f"  - Improved: {improved_bold} bold phrases")
        print(f"  - Increase: {improved_bold - baseline_bold} more bold claims")


def compare_key_moves_quality(baseline_path, improved_path):
    """Compare the philosophical sophistication of key moves"""
    
    print("\n\n" + "="*80)
    print("KEY MOVES QUALITY COMPARISON")
    print("="*80)
    
    baseline_moves = load_json_file(baseline_path / "key_moves_final.json")
    improved_moves = load_json_file(improved_path / "key_moves_final.json")
    
    if baseline_moves and improved_moves:
        print("\n📐 Move Structure Analysis:")
        
        for i, (base_move, imp_move) in enumerate(zip(
            baseline_moves.get("moves", [])[:2], 
            improved_moves.get("moves", [])[:2]
        ), 1):
            print(f"\n🎯 Move {i}: {base_move.get('title', 'Unknown')}")
            
            # Check for dialectical sophistication
            base_content = base_move.get("refined_content", base_move.get("content", ""))
            imp_content = imp_move.get("refined_content", imp_move.get("content", ""))
            
            # Count objection-response patterns
            base_objections = base_content.lower().count("objection") + base_content.lower().count("might argue")
            imp_objections = imp_content.lower().count("objection") + imp_content.lower().count("might argue")
            
            print(f"  - Baseline objections anticipated: {base_objections}")
            print(f"  - Improved objections anticipated: {imp_objections}")
            
            # Check for examples
            base_examples = base_content.lower().count("example") + base_content.lower().count("consider")
            imp_examples = imp_content.lower().count("example") + imp_content.lower().count("consider")
            
            print(f"  - Baseline examples: {base_examples}")
            print(f"  - Improved examples: {imp_examples}")


def main():
    """Run comparison analysis"""
    
    baseline_path = Path("outputs/archive/run_20250605_141342")
    improved_path = Path("outputs")
    
    print("🔬 Comparing Hájek/RLHF Improvements")
    print(f"📁 Baseline: {baseline_path}")
    print(f"📁 Improved: {improved_path}")
    
    # Run comparisons
    compare_critic_feedback(baseline_path, improved_path)
    compare_philosophical_boldness(baseline_path, improved_path)
    compare_key_moves_quality(baseline_path, improved_path)
    
    print("\n\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print("\n✅ Improvements to look for:")
    print("  1. Critics using Hájek heuristics (extreme cases, self-undermining)")
    print("  2. Less hedging language, more bold claims")
    print("  3. More anticipated objections and counterexamples")
    print("  4. Better dialectical structure in key moves")


if __name__ == "__main__":
    main() 