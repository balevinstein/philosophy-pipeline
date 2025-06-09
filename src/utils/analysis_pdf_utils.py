"""
Analysis PDF Integration Utilities
Enables Analysis journal patterns to be integrated into early development phases (II.2-6)
"""

import random
from pathlib import Path
from typing import List, Optional, Dict, Any


class AnalysisPatternIntegrator:
    """Handles Analysis paper integration for conceptual development phases"""
    
    def __init__(self):
        self.analysis_dir = Path("./analysis_cache/extracted_texts")
        self.selected_texts = []
        
    def get_files_for_phase(self, phase: str) -> int:
        """Return optimal number of text files for each development phase"""
        phase_file_counts = {
            # Phase II.2 - Framework Development
            "abstract and thesis development": 2,
            "outline structure": 2, 
            "key moves development": 2,
            
            # Phase II.3 - Key Moves Development  
            "key moves development (initial)": 1,     # Argumentation patterns
            "key moves development (examples)": 2,    # Variety crucial for examples
            "key moves development (literature)": 1,  # Strategic engagement patterns
            
            # Phase II.4 - Content Development
            "content development": 1,
            
            # Default fallback
            "default": 1
        }
        
        return phase_file_counts.get(phase, phase_file_counts["default"])
        
    def get_analysis_exemplars_for_development(self, phase: str = "default") -> Dict[str, Any]:
        """
        Select Analysis paper texts for development phases (II.2-6)
        Returns both text file paths and philosophical guidance
        Phase-aware selection for optimal file count
        """
        if not self.analysis_dir.exists():
            return {
                "available": False,
                "guidance": self._get_fallback_guidance(),
                "file_paths": [],
                "paper_names": []
            }
        
        texts = list(self.analysis_dir.glob("*.txt"))
        if not texts:
            return {
                "available": False,
                "guidance": self._get_fallback_guidance(),
                "file_paths": [],
                "paper_names": []
            }
        
        # Get optimal number of files for this phase
        num_files = self.get_files_for_phase(phase)
        
        # Select files for style reference
        selected = random.sample(texts, min(num_files, len(texts)))
        self.selected_texts = selected
        
        return {
            "available": True,
            "guidance": self._get_analysis_development_guidance(selected, phase),
            "file_paths": selected,
            "paper_names": [p.name for p in selected]
        }
    
    def _get_analysis_development_guidance(self, selected_texts: List[Path], phase: str) -> str:
        """Generate phase-specific guidance for development based on Analysis patterns"""
        paper_names = [p.name for p in selected_texts]
        
        # Phase-specific guidance
        phase_guidance = self._get_phase_specific_guidance(phase)
        
        return f"""
=== ANALYSIS JOURNAL DEVELOPMENT PATTERNS ===

The following Analysis papers are available for reference:
{', '.join(paper_names)}

PHASE-SPECIFIC FOCUS: {phase_guidance}

CRITICAL DEVELOPMENT PRINCIPLES for Analysis journal:

🎯 THESIS AND FRAMEWORK DEVELOPMENT:
- Analysis papers make BOLD, clear claims early
- Thesis statements are conversational yet precise: "I argue that..." 
- Problems are motivated through concrete, relatable examples
- Theoretical frameworks emerge FROM examples rather than preceding them

🔧 ARGUMENT DEVELOPMENT PATTERNS:
- Heavy use of intuitive examples that do real argumentative work
- "Consider this case..." style presentation 
- Examples build incrementally toward general principles
- Objections addressed through additional concrete cases

📚 LITERATURE ENGAGEMENT STYLE:
- Minimal literature review - jump quickly to the problem
- Cite strategically, not comprehensively
- Build on existing work rather than extensively reviewing it
- Focus on philosophical substance over scholarly positioning

💬 VOICE AND PRESENTATION:
- First-person engagement: "I will show...", "My argument is..."
- Direct reader address: "Notice that...", "Consider..."
- Conversational transitions: "Here's why...", "The key insight is..."
- Accessible explanations without sacrificing precision

🏗️ STRUCTURAL PREFERENCES:
- Shorter sections with clear, descriptive headings
- Examples integrated throughout, not relegated to separate sections
- Objections woven into development, not just end-section responses
- Conclusions that gesture toward broader implications

DEVELOPMENT MANDATE: Design arguments and frameworks that are inherently 
example-driven, accessible, and conversational from the conceptual stage.

=== END ANALYSIS PATTERNS ===
"""

    def _get_phase_specific_guidance(self, phase: str) -> str:
        """Get specific guidance for different development phases"""
        phase_guidance = {
            "key moves development (initial)": "Focus on Analysis argumentation patterns - how they make bold philosophical claims and structure core arguments",
            "key moves development (examples)": "Study how Analysis uses examples - concrete cases that do real philosophical work, not just illustrations",
            "key moves development (literature)": "Observe Analysis literature engagement - strategic citations that position arguments efficiently",
            "abstract and thesis development": "Note how Analysis abstracts immediately engage with concrete problems and state clear theses",
            "outline structure": "Examine Analysis paper organization - logical flow and section structure",
            "content development": "Study overall Analysis argumentation style and voice"
        }
        
        return phase_guidance.get(phase, "Study overall Analysis patterns and philosophical approach")

    def _get_fallback_guidance(self) -> str:
        """Fallback guidance when no Analysis papers are available"""
        return """
=== ANALYSIS JOURNAL STYLE (from memory) ===

Key principles for Analysis journal style:
- Conversational but rigorous academic tone
- Heavy use of concrete examples that do argumentative work
- First-person presentation ("I argue", "I will show")
- Direct reader engagement ("Consider...", "Notice that...")
- Minimal literature review, quick problem engagement
- Accessible explanations without sacrificing philosophical precision

=== END ANALYSIS PATTERNS ===
"""

    def get_selected_texts(self) -> List[Path]:
        """Return currently selected Analysis texts for API calls"""
        return self.selected_texts
    
    def enhance_prompt_with_analysis_patterns(self, base_prompt: str, phase: str) -> str:
        """
        Enhance any development phase prompt with Analysis awareness
        """
        exemplars = self.get_analysis_exemplars_for_development(phase)
        
        if not exemplars["available"]:
            # Add lightweight guidance without PDFs
            enhanced_prompt = base_prompt + "\n\n" + exemplars["guidance"]
            return enhanced_prompt
        
        # Add full Analysis guidance with PDF support indicator
        analysis_section = f"""

{exemplars["guidance"]}

NOTE: {len(exemplars["file_paths"])} Analysis paper texts are available as PDFs in your context for detailed style reference.
Study these papers to understand how Analysis approaches philosophical problems, develops arguments, and presents ideas.

Your {phase} development should reflect Analysis journal patterns: example-driven, conversational, accessible.
"""
        
        return base_prompt + analysis_section


# Global instance for easy import
analysis_integrator = AnalysisPatternIntegrator()


def enhance_development_prompt(prompt: str, phase: str) -> tuple[str, List[Path]]:
    """
    Convenience function to enhance any development prompt with Analysis patterns
    Returns (enhanced_prompt, pdf_paths_for_api)
    Phase-aware: Returns optimal number of PDFs for the specified phase
    """
    enhanced_prompt = analysis_integrator.enhance_prompt_with_analysis_patterns(prompt, phase)
    file_paths = analysis_integrator.get_selected_texts()
    
    return enhanced_prompt, file_paths


def get_analysis_texts_for_api() -> List[Path]:
    """Get current Analysis texts for API calls"""
    return analysis_integrator.get_selected_texts() 