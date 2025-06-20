#!/usr/bin/env python3
"""
Curate philosophical moves for strategic injection into pipeline prompts
"""

import json
from pathlib import Path
from typing import Dict, List, Any


def load_moves_database():
    """Load the consolidated moves database"""
    db_path = Path("outputs/philosophical_moves_db_v2/moves_database.json")
    with open(db_path, "r") as f:
        return json.load(f)


def categorize_by_worker_relevance():
    """Organize moves by which pipeline workers would benefit most"""
    
    db = load_moves_database()
    
    # Categories mapped to pipeline workers
    worker_categories = {
        "abstract_development": {
            "description": "Moves for developing clear thesis statements and framing",
            "patterns": ["scope limitation", "thesis setup", "framing"],
            "moves": []
        },
        "key_moves_development": {
            "description": "Core dialectical and conceptual moves",
            "patterns": ["objection", "response", "distinction", "counterexample"],
            "moves": []
        },
        "outline_development": {
            "description": "Structural and organizational moves",
            "patterns": ["progressive", "systematic", "structure"],
            "moves": []
        },
        "section_writing": {
            "description": "Detailed argumentation and example development",
            "patterns": ["example", "case", "application", "analysis"],
            "moves": []
        },
        "critics_all": {
            "description": "Moves showing philosophical rigor for critics to look for",
            "patterns": ["extreme case", "self-undermining", "counterexample", "boundary"],
            "moves": []
        }
    }
    
    # Sort moves into categories
    for move in db["all_moves"]:
        pattern = move.get("pattern", "").lower()
        quote_lower = move.get("quote", "").lower()
        
        # Abstract development
        if any(p in pattern for p in ["scope", "thesis", "framing", "limitation"]):
            worker_categories["abstract_development"]["moves"].append(move)
        
        # Key moves development
        if any(p in pattern for p in ["objection", "response", "distinction", "counterexample"]):
            worker_categories["key_moves_development"]["moves"].append(move)
        
        # Outline development
        if any(p in pattern for p in ["structure", "systematic", "organization"]):
            worker_categories["outline_development"]["moves"].append(move)
        
        # Section writing
        if any(p in quote_lower for p in ["example", "consider", "case", "suppose"]):
            worker_categories["section_writing"]["moves"].append(move)
        
        # Critics (looking for Hájek-style moves)
        if any(p in pattern for p in ["extreme", "boundary", "self-undermining", "prove too much"]):
            worker_categories["critics_all"]["moves"].append(move)
    
    return worker_categories


def select_top_moves_per_category(categories: Dict, n: int = 3) -> Dict:
    """Select top N moves from each category based on quality"""
    
    curated = {}
    
    for cat_name, category in categories.items():
        # Sort by quality and select top N
        moves = category["moves"]
        high_quality = [m for m in moves if m.get("quality") == "High"]
        medium_quality = [m for m in moves if m.get("quality") == "Medium"]
        
        # Prefer high quality, fall back to medium
        selected = high_quality[:n]
        if len(selected) < n:
            selected.extend(medium_quality[:n - len(selected)])
        
        curated[cat_name] = {
            "description": category["description"],
            "total_available": len(moves),
            "selected_moves": selected
        }
    
    return curated


def create_injectable_examples(curated: Dict) -> Dict:
    """Format moves as injectable few-shot examples"""
    
    injectable = {}
    
    for worker, data in curated.items():
        examples = []
        
        for move in data["selected_moves"]:
            example = {
                "pattern_name": move["move_name"],
                "pattern_description": move["pattern"],
                "example_quote": move["quote"],
                "mechanism": move["mechanism"],
                "achievement": move["achievement"],
                "source": f"{move['source_paper']} by {move['source_author']}"
            }
            
            # Add context notes if present
            if move.get("context_notes"):
                example["context"] = move["context_notes"]
            
            examples.append(example)
        
        injectable[worker] = {
            "description": data["description"],
            "examples": examples
        }
    
    return injectable


def main():
    """Curate moves for pipeline injection"""
    
    print("🔍 Analyzing philosophical moves database...")
    
    # Categorize by worker relevance
    categories = categorize_by_worker_relevance()
    
    # Report on categorization
    print("\n📊 Moves by Worker Category:")
    for cat, data in categories.items():
        print(f"  - {cat}: {len(data['moves'])} moves found")
    
    # Select top moves per category
    curated = select_top_moves_per_category(categories, n=3)
    
    print("\n✅ Selected Top Moves:")
    for cat, data in curated.items():
        print(f"  - {cat}: {len(data['selected_moves'])} moves selected")
    
    # Create injectable examples
    injectable = create_injectable_examples(curated)
    
    # Save results
    output_dir = Path("outputs/curated_moves")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / "categorized_moves.json", "w") as f:
        json.dump(categories, f, indent=2)
    
    with open(output_dir / "curated_moves.json", "w") as f:
        json.dump(curated, f, indent=2)
    
    with open(output_dir / "injectable_examples.json", "w") as f:
        json.dump(injectable, f, indent=2)
    
    # Create a markdown preview
    preview = "# Curated Philosophical Moves for Pipeline Injection\n\n"
    
    for worker, data in injectable.items():
        preview += f"## {worker}\n{data['description']}\n\n"
        
        for i, example in enumerate(data['examples'], 1):
            preview += f"### Example {i}: {example['pattern_name']}\n"
            preview += f"**Pattern**: {example['pattern_description']}\n"
            preview += f"**Quote**: {example['example_quote'][:200]}...\n"
            preview += f"**Source**: {example['source']}\n\n"
    
    with open(output_dir / "preview.md", "w") as f:
        f.write(preview)
    
    print(f"\n📁 Curated moves saved to: {output_dir}")
    print("📋 Files created:")
    print("  - categorized_moves.json (full categorization)")
    print("  - curated_moves.json (selected top moves)")
    print("  - injectable_examples.json (ready for prompts)")
    print("  - preview.md (human-readable preview)")


if __name__ == "__main__":
    main() 