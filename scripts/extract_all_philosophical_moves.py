#!/usr/bin/env python3
"""
Extract philosophical moves from ALL Analysis papers with improved context
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any
import time
from datetime import datetime

from src.utils.api import APIHandler


def extract_new_texts_first():
    """Extract text from PDFs we haven't processed yet"""
    papers_dir = Path("./Analysis_papers")
    output_dir = Path("./data/analysis_extracts")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all PDFs
    all_pdfs = list(papers_dir.glob("*.pdf"))
    
    # Check which ones we already have as TXT
    existing_txts = {f.stem for f in output_dir.glob("*.txt")}
    
    # Find PDFs we haven't extracted
    to_extract = []
    for pdf in all_pdfs:
        txt_name = pdf.stem
        if txt_name not in existing_txts:
            to_extract.append(pdf)
    
    print(f"📚 Found {len(all_pdfs)} PDFs total")
    print(f"📄 Already have {len(existing_txts)} TXT files")
    print(f"🆕 Need to extract {len(to_extract)} new papers")
    
    if to_extract:
        api_handler = APIHandler()
        print("\n🔄 Extracting new PDFs to TXT...")
        
        for i, pdf_path in enumerate(to_extract[:10], 1):  # Limit to 10 at a time
            print(f"\n[{i}/{min(10, len(to_extract))}] Extracting {pdf_path.name}...")
            
            prompt = """Please extract and return the complete text content of this PDF document. 
Format it cleanly with paragraph breaks but don't add any commentary or analysis - 
just return the raw text content of the paper."""
            
            try:
                response = api_handler._call_anthropic_with_pdf(
                    prompt=prompt,
                    pdf_path=pdf_path,
                    config={
                        "model": "claude-3-5-sonnet-20241022",
                        "max_tokens": 8192,
                        "temperature": 0.1
                    }
                )
                
                # Save extracted text
                output_path = output_dir / f"{pdf_path.stem}.txt"
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(response)
                    
                print(f"✅ Extracted to {output_path.name}")
                time.sleep(2)  # Rate limiting
                
            except Exception as e:
                print(f"❌ Error: {e}")
    
    return len(existing_txts) + min(10, len(to_extract))


def load_improved_prompt() -> str:
    """Load the improved extraction prompt with context requirements"""
    with open("docs/philosophical_moves_extraction_prompt_v2.md", "r") as f:
        return f.read()


def extract_moves_from_paper(paper_path: Path, api_handler: APIHandler) -> Dict[str, Any]:
    """Extract philosophical moves with improved context"""
    
    print(f"\n📄 Extracting moves from: {paper_path.name}")
    
    # Load paper text
    with open(paper_path, "r", encoding="utf-8") as f:
        paper_text = f.read()
    
    # Get improved extraction prompt
    extraction_prompt = load_improved_prompt()
    
    # Construct full prompt
    full_prompt = f"""{extraction_prompt}

Now analyze this Analysis paper:

<paper>
{paper_text}
</paper>

Extract philosophical moves following the guidelines above. 
Remember: Each move must be SELF-CONTAINED and understandable without reading the full paper.
Return ONLY valid JSON with no additional text."""

    # Make API call
    try:
        response = api_handler.make_api_call(
            stage="literature_processing",
            prompt=full_prompt,
            system_prompt="You are an expert philosophy researcher extracting reusable philosophical moves. Focus on self-contained examples that could teach someone how to do philosophy. You must respond with valid JSON only."
        )
        
        # Clean and parse response
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        if response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        response = response.strip()
        
        result = json.loads(response)
        result["source_file"] = paper_path.name
        
        move_count = len(result.get('philosophical_moves', []))
        quality_count = sum(1 for m in result.get('philosophical_moves', []) 
                          if m.get('quality') == 'High')
        
        print(f"✅ Extracted {move_count} moves ({quality_count} high quality)")
        return result
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        print(f"Response preview: {response[:200]}...")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def consolidate_moves_v2(all_extractions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Consolidate with focus on high-quality, self-contained moves"""
    
    consolidated = {
        "extraction_date": datetime.now().isoformat(),
        "papers_analyzed": len(all_extractions),
        "total_moves": 0,
        "high_quality_moves": 0,
        "move_categories": {
            "offensive": [],
            "defensive": [],
            "constructive": [],
            "meta": []
        },
        "all_moves": [],
        "pattern_frequency": {},
        "domain_distribution": {}
    }
    
    # Process each extraction
    for extraction in all_extractions:
        if not extraction:
            continue
            
        paper_info = extraction.get("paper_info", {})
        
        for move in extraction.get("philosophical_moves", []):
            # Add paper info
            move["source_paper"] = paper_info.get("title", "Unknown")
            move["source_author"] = paper_info.get("author", "Unknown")
            
            # Add to all moves
            consolidated["all_moves"].append(move)
            consolidated["total_moves"] += 1
            
            # Count high quality
            if move.get("quality") == "High":
                consolidated["high_quality_moves"] += 1
            
            # Categorize (using new classification)
            for category in move.get("classification", []):
                if category in consolidated["move_categories"]:
                    consolidated["move_categories"][category].append(move)
            
            # Track patterns
            pattern = move.get("pattern", "")
            if pattern:
                consolidated["pattern_frequency"][pattern] = \
                    consolidated["pattern_frequency"].get(pattern, 0) + 1
            
            # Track domains
            domain = move.get("domain", "General")
            consolidated["domain_distribution"][domain] = \
                consolidated["domain_distribution"].get(domain, 0) + 1
    
    # Sort patterns by frequency
    consolidated["top_patterns"] = sorted(
        consolidated["pattern_frequency"].items(),
        key=lambda x: x[1],
        reverse=True
    )[:30]
    
    # Find best self-contained examples
    consolidated["exemplar_moves"] = [
        m for m in consolidated["all_moves"]
        if m.get("quality") == "High" and 
           len(m.get("quote", "")) > 200 and
           not m.get("context_notes")  # Prefer moves that didn't need extra notes
    ][:20]
    
    return consolidated


def main():
    """Main extraction workflow"""
    
    print("🚀 Starting Comprehensive Philosophical Moves Extraction")
    
    # First, extract any new PDFs to TXT
    total_available = extract_new_texts_first()
    
    # Initialize API handler
    api_handler = APIHandler()
    
    # Get all text files
    text_dir = Path("data/analysis_extracts")
    text_files = list(text_dir.glob("*.txt"))
    
    print(f"\n📚 Total papers available for analysis: {len(text_files)}")
    
    # For now, let's process in batches to avoid rate limits
    batch_size = 10
    print(f"\n🔬 Processing first batch of {batch_size} papers...")
    
    # Extract moves from batch
    all_extractions = []
    for i, paper_path in enumerate(text_files[:batch_size], 1):
        print(f"\n[{i}/{batch_size}] Processing {paper_path.name}")
        extraction = extract_moves_from_paper(paper_path, api_handler)
        if extraction:
            all_extractions.append(extraction)
        time.sleep(3)  # Rate limiting
    
    # Consolidate results
    print("\n📊 Consolidating extracted moves...")
    consolidated = consolidate_moves_v2(all_extractions)
    
    # Save results
    output_dir = Path("outputs/philosophical_moves_db_v2")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save raw extractions
    with open(output_dir / "raw_extractions.json", "w") as f:
        json.dump(all_extractions, f, indent=2)
    
    # Save consolidated database
    with open(output_dir / "moves_database.json", "w") as f:
        json.dump(consolidated, f, indent=2)
    
    # Generate report
    report = f"""# Philosophical Moves Extraction Report V2

Generated: {consolidated['extraction_date']}
Papers Analyzed: {consolidated['papers_analyzed']}
Total Moves: {consolidated['total_moves']}
High Quality Moves: {consolidated['high_quality_moves']}

## Category Distribution (New Ontology)
- Offensive: {len(consolidated['move_categories']['offensive'])}
- Defensive: {len(consolidated['move_categories']['defensive'])}
- Constructive: {len(consolidated['move_categories']['constructive'])}
- Meta: {len(consolidated['move_categories']['meta'])}

## Top 10 Patterns
"""
    
    for i, (pattern, count) in enumerate(consolidated['top_patterns'][:10], 1):
        report += f"{i}. {pattern} (×{count})\n"
    
    report += f"\n## Quality Metrics\n"
    report += f"- High-quality self-contained examples: {len(consolidated['exemplar_moves'])}\n"
    report += f"- Average moves per paper: {consolidated['total_moves']/consolidated['papers_analyzed']:.1f}\n"
    
    with open(output_dir / "extraction_report.md", "w") as f:
        f.write(report)
    
    print(f"\n✅ Extraction complete!")
    print(f"📁 Results saved to: {output_dir}")
    print(f"📊 High-quality moves: {consolidated['high_quality_moves']}/{consolidated['total_moves']}")
    print(f"🌟 Self-contained exemplars: {len(consolidated['exemplar_moves'])}")
    
    print(f"\n💡 To process more papers, run again or modify batch_size")
    print(f"📝 Remaining papers to process: {len(text_files) - batch_size}")


if __name__ == "__main__":
    main() 