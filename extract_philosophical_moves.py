#!/usr/bin/env python3
"""
Extract philosophical moves from Analysis papers for database generation.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any
import time
from datetime import datetime

from src.utils.api import APIHandler


def load_extraction_prompt() -> str:
    """Load the philosophical moves extraction prompt"""
    with open("docs/philosophical_moves_extraction_prompt.md", "r") as f:
        return f.read()


def extract_moves_from_paper(paper_path: Path, api_handler: APIHandler) -> Dict[str, Any]:
    """Extract philosophical moves from a single paper"""
    
    print(f"\n📄 Extracting moves from: {paper_path.name}")
    
    # Load paper text
    with open(paper_path, "r", encoding="utf-8") as f:
        paper_text = f.read()
    
    # Get extraction prompt
    extraction_prompt = load_extraction_prompt()
    
    # Construct full prompt
    full_prompt = f"""{extraction_prompt}

Now analyze this Analysis paper:

<paper>
{paper_text}
</paper>

Extract philosophical moves following the guidelines above. Return ONLY valid JSON with no additional text."""

    # Make API call
    try:
        response = api_handler.make_api_call(
            stage="literature_processing",  # Use existing stage
            prompt=full_prompt,
            system_prompt="You are an expert philosophy researcher analyzing papers to extract reusable philosophical moves and techniques. Focus on identifying transferable argumentative patterns. You must respond with valid JSON only, no additional text or markdown."
        )
        
        # Clean response and parse JSON
        # Remove any markdown code blocks if present
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        if response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        response = response.strip()
        
        # Parse JSON response
        result = json.loads(response)
        result["source_file"] = paper_path.name
        
        print(f"✅ Extracted {len(result.get('philosophical_moves', []))} moves")
        return result
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error for {paper_path.name}: {e}")
        print(f"Response was: {response[:500]}...")  # Show first 500 chars
        return None
    except Exception as e:
        print(f"❌ Error extracting from {paper_path.name}: {e}")
        return None


def consolidate_moves(all_extractions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Consolidate all extracted moves into a unified database"""
    
    consolidated = {
        "extraction_date": datetime.now().isoformat(),
        "papers_analyzed": len(all_extractions),
        "total_moves": 0,
        "move_categories": {
            "dialectical": [],
            "conceptual": [],
            "example": [],
            "structural": [],
            "literature": []
        },
        "all_moves": [],
        "pattern_frequency": {}
    }
    
    # Process each extraction
    for extraction in all_extractions:
        if not extraction:
            continue
            
        paper_info = extraction.get("paper_info", {})
        
        for move in extraction.get("philosophical_moves", []):
            # Add paper info to each move
            move["source_paper"] = paper_info.get("title", "Unknown")
            move["source_author"] = paper_info.get("author", "Unknown")
            
            # Add to all moves
            consolidated["all_moves"].append(move)
            consolidated["total_moves"] += 1
            
            # Categorize
            for category in move.get("categories", []):
                if category in consolidated["move_categories"]:
                    consolidated["move_categories"][category].append(move)
            
            # Track pattern frequency
            pattern = move.get("transferable_pattern", "")
            if pattern:
                consolidated["pattern_frequency"][pattern] = \
                    consolidated["pattern_frequency"].get(pattern, 0) + 1
    
    # Sort patterns by frequency
    consolidated["top_patterns"] = sorted(
        consolidated["pattern_frequency"].items(),
        key=lambda x: x[1],
        reverse=True
    )[:20]
    
    return consolidated


def generate_analysis_report(consolidated: Dict[str, Any]) -> str:
    """Generate a human-readable analysis of the extracted moves"""
    
    report = f"""# Philosophical Moves Analysis Report

Generated: {consolidated['extraction_date']}
Papers Analyzed: {consolidated['papers_analyzed']}
Total Moves Extracted: {consolidated['total_moves']}

## Move Distribution by Category

"""
    
    for category, moves in consolidated["move_categories"].items():
        report += f"- **{category.capitalize()}**: {len(moves)} moves\n"
    
    report += "\n## Top 10 Transferable Patterns\n\n"
    
    for i, (pattern, count) in enumerate(consolidated["top_patterns"][:10], 1):
        report += f"{i}. **{pattern}** (used {count} times)\n"
    
    report += "\n## High-Value Moves (Highly Effective & Original)\n\n"
    
    high_value_moves = [
        m for m in consolidated["all_moves"]
        if m.get("effectiveness", "").startswith("High") and
           m.get("originality", "") in ["Novel", "Variation"]
    ]
    
    for move in high_value_moves[:10]:
        report += f"""### {move['move_name']}
- **Source**: {move['source_paper']} by {move['source_author']}
- **Pattern**: {move.get('transferable_pattern', 'N/A')}
- **Achievement**: {move.get('achievement', 'N/A')}

"""
    
    return report


def main():
    """Main extraction workflow"""
    
    print("🚀 Starting Philosophical Moves Extraction")
    
    # Initialize API handler
    api_handler = APIHandler()
    
    # Get all text files
    text_dir = Path("analysis_cache/extracted_texts")
    text_files = list(text_dir.glob("*.txt"))
    
    print(f"📚 Found {len(text_files)} Analysis papers to analyze")
    
    # For pilot, let's just do 3 papers
    pilot_files = text_files[:3]
    print(f"\n🔬 Pilot extraction from {len(pilot_files)} papers")
    
    # Extract moves from each paper
    all_extractions = []
    for paper_path in pilot_files:
        extraction = extract_moves_from_paper(paper_path, api_handler)
        if extraction:
            all_extractions.append(extraction)
        time.sleep(2)  # Rate limiting
    
    # Consolidate results
    print("\n📊 Consolidating extracted moves...")
    consolidated = consolidate_moves(all_extractions)
    
    # Save results
    output_dir = Path("outputs/philosophical_moves_db")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save raw extractions
    with open(output_dir / "raw_extractions.json", "w") as f:
        json.dump(all_extractions, f, indent=2)
    
    # Save consolidated database
    with open(output_dir / "moves_database.json", "w") as f:
        json.dump(consolidated, f, indent=2)
    
    # Generate and save analysis report
    report = generate_analysis_report(consolidated)
    with open(output_dir / "analysis_report.md", "w") as f:
        f.write(report)
    
    print(f"\n✅ Extraction complete!")
    print(f"📁 Results saved to: {output_dir}")
    print(f"📊 Total moves extracted: {consolidated['total_moves']}")
    print(f"🎯 Top pattern: {consolidated['top_patterns'][0] if consolidated['top_patterns'] else 'None'}")


if __name__ == "__main__":
    main() 