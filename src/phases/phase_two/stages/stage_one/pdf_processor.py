# src/stages/phase_two/stages/stage_one/pdf_processor.py
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging
from dataclasses import dataclass

import pdfplumber
import fitz  # PyMuPDF


@dataclass
class PaperAccess:
    """Tracks paper accessibility status"""

    has_text: bool
    extraction_method: str
    confidence: str
    limitations: List[str]
    recommendations: List[str]


class DualPDFProcessor:
    """Handles PDF processing with two methods"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def process_paper(self, pdf_path: Path) -> Dict[str, Any]:
        """Process paper with appropriate method"""
        # Try text extraction
        result = self.extract_text(pdf_path)

        if result["content"]:
            # We got text, process normally
            return {
                "paper_info": {
                    "title": pdf_path.stem,
                    "access_type": "full",
                    "chunks": self._create_chunks(result["content"]),
                    "extraction_method": result["method"],
                    "confidence": result["confidence"],
                }
            }
        else:
            # Create limited access info
            return {
                "paper_info": {
                    "title": pdf_path.stem,
                    "access_type": "limited",
                    "chunks": None,
                    "access_status": self._create_limited_access_status(),
                }
            }

    def extract_text(self, pdf_path: Path) -> Dict[str, Any]:
        """Try both methods to extract text"""
        # Try pdfplumber first
        text = self._try_pdfplumber(pdf_path)
        if text:
            return {"content": text, "method": "pdfplumber", "confidence": "high"}

        # Fallback to PyMuPDF
        text = self._try_pymupdf(pdf_path)
        if text:
            return {"content": text, "method": "pymupdf", "confidence": "medium"}

        return {"content": None, "method": "none", "confidence": "none"}

    def _create_limited_access_status(self) -> PaperAccess:
        """Create status for papers we can't process"""
        return PaperAccess(
            has_text=False,
            extraction_method="none",
            confidence="limited",
            limitations=[
                "Unable to extract text from PDF",
                "Cannot verify specific quotes or claims",
                "Page numbers and specific locations unavailable",
            ],
            recommendations=[
                "Work from general knowledge of paper",
                "Focus on main conceptual points",
                "Flag all claims as based on memory",
                "Be explicit about confidence levels",
                "Consider seeking newer edition if available",
            ],
        )

    def _try_pdfplumber(self, pdf_path: Path) -> Optional[str]:
        """Attempt extraction with pdfplumber"""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = []
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text.append(extracted)
                return "\n\n".join(text) if text else None
        except Exception as e:
            self.logger.warning(f"pdfplumber failed: {str(e)}")
            return None

    def _try_pymupdf(self, pdf_path: Path) -> Optional[str]:
        """Attempt extraction with PyMuPDF"""
        try:
            doc = fitz.open(pdf_path)
            text = []
            for page in doc:
                extracted = page.get_text()
                if extracted:
                    text.append(extracted)
            doc.close()
            return "\n\n".join(text) if text else None
        except Exception as e:
            self.logger.warning(f"PyMuPDF failed: {str(e)}")
            return None

    def chunk_paper(self, pdf_path: Path) -> List[Dict[str, Any]]:
        """Extract and chunk paper content"""
        # Get text content
        result = self.extract_text(pdf_path)
        content = result.get("content")

        if not content:
            self.logger.warning(f"No text could be extracted from {pdf_path}")
            return []

        # Split into chunks (roughly 3K tokens each)
        chunks = []
        lines = content.split("\n")
        current_chunk = []
        current_size = 0
        chunk_number = 1

        for line in lines:
            current_chunk.append(line)
            current_size += len(line.split())  # Rough word count

            # Aim for ~3K tokens per chunk
            if current_size >= 2250:  # ~750 words ≈ 3K tokens
                chunk_text = "\n".join(current_chunk)
                chunks.append(
                    {
                        "content": chunk_text,
                        "chunk_number": chunk_number,
                        "estimated_tokens": current_size * 4,  # Rough estimate
                        "extraction_method": result["method"],
                        "confidence": result["confidence"],
                    }
                )
                current_chunk = []
                current_size = 0
                chunk_number += 1

        # Add any remaining content as final chunk
        if current_chunk:
            chunk_text = "\n".join(current_chunk)
            chunks.append(
                {
                    "content": chunk_text,
                    "chunk_number": chunk_number,
                    "estimated_tokens": current_size * 4,
                    "extraction_method": result["method"],
                    "confidence": result["confidence"],
                }
            )

        return chunks
