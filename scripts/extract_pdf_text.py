#!/usr/bin/env python3
"""
Simple PDF text extractor to let Claude read Analysis papers directly
"""

from pathlib import Path
from src.utils.api import APIHandler


def extract_pdf_text(pdf_path: Path, output_path: Path):
    """Extract text from PDF using the existing API handler"""
    
    api_handler = APIHandler()
    
    # Simple extraction prompt
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
        
        # Save extracted text
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(response)
            
        print(f"✅ Extracted text from {pdf_path.name} to {output_path.name}")
        return True
        
    except Exception as e:
        print(f"❌ Error extracting {pdf_path.name}: {e}")
        return False


def main():
    """Extract text from a few Analysis papers for direct reading"""
    
    papers_dir = Path("./Analysis_papers")
    output_dir = Path("./text_extracts")
    output_dir.mkdir(exist_ok=True)
    
    # Extract text from a few representative papers
    papers_to_extract = [
        "anae044 (1).pdf",  # Short paper
        "anae045 (1).pdf",  # Short paper  
        "anae047 (1).pdf"   # Medium paper
    ]
    
    for pdf_name in papers_to_extract:
        pdf_path = papers_dir / pdf_name
        if pdf_path.exists():
            text_name = pdf_name.replace(".pdf", ".txt")
            output_path = output_dir / text_name
            extract_pdf_text(pdf_path, output_path)
        else:
            print(f"❌ PDF not found: {pdf_name}")


if __name__ == "__main__":
    main() 