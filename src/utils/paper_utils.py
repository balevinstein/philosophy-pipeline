# src/utils/paper_utils.py

from pathlib import Path
from typing import Dict, List


class PaperHandler:
    """Simple utility for handling paper PDFs"""

    def __init__(self):
        self.papers_dir = Path(__file__).parent.parent.parent / "papers"
        self.papers_dir.mkdir(exist_ok=True)

    def get_required_papers(self, selection_json: Dict) -> List[str]:
        """Extract list of required papers from selection output"""
        papers = []
        literature_needs = selection_json["phase_two_setup"]["phase_two_setup"][
            "literature_needs"
        ]

        for paper in literature_needs.get("remembered_papers", []):
            papers.append(
                {
                    "title": paper["title"],
                    "authors": paper["authors"],
                    "confidence": paper["confidence"],
                }
            )

        return papers

    def get_available_papers(self) -> List[Path]:
        """Get list of available PDFs in papers directory"""
        return list(self.papers_dir.glob("*.pdf"))

    def print_paper_status(self, selection_json: Dict):
        """Print status of required papers vs available papers"""
        required = self.get_required_papers(selection_json)
        available = self.get_available_papers()

        print("\nPaper Status:")
        for paper in required:
            print(f"\nTitle: {paper['title']}")
            print(f"Authors: {', '.join(paper['authors'])}")
            filename = f"{paper['title'].lower().replace(' ', '_')}.pdf"
            if self.papers_dir / filename in available:
                print("Status: ✓ Available")
            else:
                print("Status: ✗ Missing")
