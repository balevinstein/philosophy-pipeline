#!/usr/bin/env python3
"""
Extract text from additional Analysis PDFs to expand our corpus
"""

from pathlib import Path
from src.utils.api import APIHandler
import time


def extract_pdf_text(pdf_path: Path, output_path: Path, api_handler: APIHandler):
    """Extract text from PDF using the existing API handler"""
    
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
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(response)
            
        print(f"✅ Extracted text from {pdf_path.name}")
        return True
        
    except Exception as e:
        print(f"❌ Error extracting {pdf_path.name}: {e}")
        return False


def main():
    """Extract text from additional Analysis papers"""
    
    papers_dir = Path("./Analysis_papers")
    output_dir = Path("./analysis_cache/extracted_texts")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Papers we haven't extracted yet
    papers_to_extract = [
        "anab009.pdf",
        "anab023.pdf", 
        "anab031.pdf",
        "anab033.pdf",
        "anab035.pdf",
        "anab039.pdf",
        "anab042.pdf",
        "anad017.pdf"
    ]
    
    api_handler = APIHandler()
    extracted_count = 0
    
    print(f"📚 Extracting text from {len(papers_to_extract)} additional papers...")
    
    for pdf_name in papers_to_extract:
        pdf_path = papers_dir / pdf_name
        if pdf_path.exists():
            text_name = pdf_name.replace(".pdf", ".txt")
            output_path = output_dir / text_name
            
            # Skip if already extracted
            if output_path.exists():
                print(f"⏭️  Skipping {pdf_name} - already extracted")
                continue
                
            if extract_pdf_text(pdf_path, output_path, api_handler):
                extracted_count += 1
                
            # Rate limiting
            time.sleep(2)
        else:
            print(f"❌ PDF not found: {pdf_name}")
    
    print(f"\n✅ Extracted {extracted_count} new papers")
    print(f"📊 Total papers now available: {len(list(output_dir.glob('*.txt')))}")


if __name__ == "__main__":
    main() 