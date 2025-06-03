#!/usr/bin/env python3
"""
Analysis Paper Cache Builder
Extracts text from Analysis papers and creates a searchable cache for future use
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
from src.utils.api import APIHandler


def extract_pdf_text(pdf_path: Path, api_handler: APIHandler) -> str:
    """Extract text from PDF using the existing API handler"""
    
    prompt = "Please extract and return the complete text content of this PDF document. Format it cleanly with paragraph breaks but don't add any commentary or analysis - just return the raw text content."
    
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
        return response
        
    except Exception as e:
        print(f"❌ Error extracting {pdf_path.name}: {e}")
        return None


def analyze_paper_metadata(text_content: str, pdf_name: str) -> Dict[str, Any]:
    """Extract basic metadata from paper text"""
    lines = text_content.split('\n')
    
    # Try to find title (usually in first few lines)
    title = "Unknown"
    author = "Unknown"
    abstract = ""
    
    for i, line in enumerate(lines[:20]):
        line = line.strip()
        if line and not line.startswith('Analysis Vol') and not line.startswith('doi:'):
            if title == "Unknown" and len(line) > 10:
                title = line
            elif author == "Unknown" and len(line.split()) <= 5 and len(line) > 3:
                author = line
            elif line.lower().startswith('abstract'):
                # Extract abstract
                abstract_lines = []
                for j in range(i+1, min(i+15, len(lines))):
                    if lines[j].strip() and not lines[j].lower().startswith('keywords'):
                        abstract_lines.append(lines[j].strip())
                    elif lines[j].lower().startswith('keywords'):
                        break
                abstract = ' '.join(abstract_lines)
                break
    
    # Estimate word count
    word_count = len(text_content.split())
    
    return {
        "pdf_name": pdf_name,
        "title": title,
        "author": author,
        "abstract": abstract[:300] + "..." if len(abstract) > 300 else abstract,
        "word_count": word_count,
        "extraction_date": datetime.now().isoformat()
    }


def main():
    """Build comprehensive Analysis paper cache"""
    
    # Setup directories
    cache_dir = Path("./analysis_cache")
    texts_dir = cache_dir / "extracted_texts"
    cache_dir.mkdir(exist_ok=True)
    texts_dir.mkdir(exist_ok=True)
    
    # Get all available PDFs
    papers_dir = Path("./Analysis_papers")
    if not papers_dir.exists():
        print("❌ Analysis_papers directory not found")
        return
    
    pdf_files = list(papers_dir.glob("*.pdf"))
    if not pdf_files:
        print("❌ No PDF files found in Analysis_papers directory")
        return
    
    print(f"Found {len(pdf_files)} Analysis papers to process")
    
    # Initialize API handler
    api_handler = APIHandler()
    
    # Process papers
    paper_index = []
    successful_extractions = 0
    
    for pdf_path in pdf_files:
        print(f"\nProcessing: {pdf_path.name}")
        
        # Check if already extracted
        text_path = texts_dir / f"{pdf_path.stem}.txt"
        
        if text_path.exists():
            print(f"✅ Already extracted: {pdf_path.name}")
            with open(text_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
        else:
            # Extract text
            text_content = extract_pdf_text(pdf_path, api_handler)
            
            if text_content:
                # Save extracted text
                with open(text_path, 'w', encoding='utf-8') as f:
                    f.write(text_content)
                print(f"✅ Extracted: {pdf_path.name}")
            else:
                print(f"❌ Failed to extract: {pdf_path.name}")
                continue
        
        # Analyze metadata
        metadata = analyze_paper_metadata(text_content, pdf_path.name)
        paper_index.append(metadata)
        successful_extractions += 1
    
    # Save paper index
    index_path = cache_dir / "paper_index.json"
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump({
            "extraction_summary": {
                "total_papers": len(pdf_files),
                "successful_extractions": successful_extractions,
                "extraction_date": datetime.now().isoformat(),
                "cache_directory": str(cache_dir.absolute())
            },
            "papers": paper_index
        }, f, indent=2)
    
    # Create .gitignore for cache directory
    gitignore_path = cache_dir / ".gitignore"
    with open(gitignore_path, 'w') as f:
        f.write("# Analysis paper cache - too large for git\n")
        f.write("*\n")
        f.write("!.gitignore\n")
    
    # Copy our existing style guide to cache
    existing_guide = Path("./outputs/analysis_style_guide.md")
    if existing_guide.exists():
        cache_guide = cache_dir / "analysis_style_guide.md"
        with open(existing_guide, 'r') as src, open(cache_guide, 'w') as dst:
            dst.write(src.read())
    
    print(f"\n🎉 Cache building complete!")
    print(f"📊 Successfully processed {successful_extractions}/{len(pdf_files)} papers")
    print(f"📁 Cache location: {cache_dir.absolute()}")
    print(f"📋 Paper index: {index_path}")
    print(f"🚫 Cache directory is git-ignored")
    
    # Display some statistics
    if paper_index:
        word_counts = [p['word_count'] for p in paper_index]
        avg_words = sum(word_counts) / len(word_counts)
        print(f"\n📈 Statistics:")
        print(f"   Average word count: {avg_words:.0f}")
        print(f"   Shortest paper: {min(word_counts)} words")
        print(f"   Longest paper: {max(word_counts)} words")


if __name__ == "__main__":
    main() 