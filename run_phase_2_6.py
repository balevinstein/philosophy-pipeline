import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List


def load_abstract_framework() -> Dict[str, Any]:
    """Load the final abstract framework from Phase II.2"""
    try:
        with open("./outputs/framework_development/abstract_framework.json") as f:
            data = json.load(f)
            return data.get("abstract_framework", {})
    except FileNotFoundError:
        raise ValueError("Could not find abstract_framework.json. Run Phase II.2 first.")


def load_developed_key_moves() -> List[Dict[str, Any]]:
    """Load the fully developed key moves from Phase II.3"""
    try:
        with open("./outputs/key_moves_development/key_moves_development/all_developed_moves.json") as f:
            data = json.load(f)
            return data.get("developed_moves", [])
    except FileNotFoundError:
        raise ValueError("Could not find all_developed_moves.json. Run Phase II.3 first.")


def load_detailed_outline() -> Dict[str, Any]:
    """Load the final detailed outline from Phase II.4"""
    try:
        with open("./outputs/detailed_outline/detailed_outline_final.json") as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValueError("Could not find detailed_outline_final.json. Run Phase II.4 first.")


def load_literature_context() -> Dict[str, Any]:
    """Load the literature context from existing Phase II.5 output if available"""
    try:
        with open("./outputs/phase_3_context.json") as f:
            data = json.load(f)
            return data.get("literature", {})
    except FileNotFoundError:
        print("No existing literature context found. This is okay - continuing without it.")
        return {}


def extract_section_structure(detailed_outline: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract section structure from detailed outline for writing guidance"""
    sections = []
    
    # Define metadata sections that should not be treated as real paper sections
    metadata_sections = {
        "Revised Balance Assessment",
        "Changes Made", 
        "FINAL VALIDATED OUTLINE",
        "VERSION",
    }
    
    # Try to extract sections from different possible structures
    outline_content = detailed_outline.get("detailed_outline", "")
    if not outline_content:
        outline_content = detailed_outline.get("content", "")
    if not outline_content:
        outline_content = detailed_outline.get("outline", "")
    
    if isinstance(outline_content, str):
        # Parse markdown-style sections
        lines = outline_content.split("\n")
        current_section = None
        current_content = []
        
        for line in lines:
            if line.startswith("## ") and not line.startswith("### "):
                # Save previous section if it's not metadata
                if current_section and not any(meta in current_section for meta in metadata_sections):
                    sections.append({
                        "section_name": current_section,
                        "content_guidance": "\n".join(current_content).strip(),
                        "word_target": estimate_word_target(current_section, len(sections))
                    })
                
                # Start new section
                current_section = line.strip("# ").strip()
                current_content = []
            else:
                current_content.append(line)
        
        # Don't forget the last section (if it's not metadata)
        if current_section and not any(meta in current_section for meta in metadata_sections):
            sections.append({
                "section_name": current_section,
                "content_guidance": "\n".join(current_content).strip(),
                "word_target": estimate_word_target(current_section, len(sections))
            })
    
    return sections


def estimate_word_target(section_name: str, section_index: int) -> int:
    """Estimate word targets for different sections (4000 word total)"""
    section_lower = section_name.lower()
    
    if "introduction" in section_lower:
        return 600
    elif "conclusion" in section_lower:
        return 500
    elif section_index == 0:  # First section
        return 600
    elif "objection" in section_lower or "reply" in section_lower:
        return 400
    else:
        return 700  # Main argumentative sections


def create_content_bank(developed_moves: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a content bank of ready-to-use arguments and examples"""
    arguments = []
    examples = []
    citations = []
    
    for move in developed_moves:
        # Extract final content
        final_content = move.get("final_content", "")
        if not final_content:
            final_content = move.get("development", {}).get("literature", "")
        
        if final_content:
            arguments.append({
                "move_text": move.get("key_move_text", ""),
                "content": final_content,
                "move_index": move.get("key_move_index", len(arguments))
            })
        
        # Extract examples from development phases
        development = move.get("development", {})
        if "examples" in development and development["examples"]:
            examples.append({
                "move_index": move.get("key_move_index", 0),
                "examples_content": development["examples"]
            })
        
        # Extract citations (basic pattern matching)
        if final_content:
            # Look for citation patterns like "Author (Year)" or "Author Year"
            import re
            citation_pattern = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*\((\d{4})[^\)]*\)'
            citations_found = re.findall(citation_pattern, final_content)
            for author, year in citations_found:
                citations.append(f"{author} ({year})")
    
    return {
        "arguments": arguments,
        "examples": examples,
        "citations": list(set(citations))  # Remove duplicates
    }


def create_writing_context(
    abstract_framework: Dict[str, Any],
    developed_moves: List[Dict[str, Any]], 
    detailed_outline: Dict[str, Any],
    literature_context: Dict[str, Any]
) -> Dict[str, Any]:
    """Create the optimized context for Phase III writing"""
    
    sections = extract_section_structure(detailed_outline)
    content_bank = create_content_bank(developed_moves)
    
    # Extract key paper information
    main_thesis = abstract_framework.get("main_thesis", "")
    abstract = abstract_framework.get("abstract", "")
    
    return {
        "paper_overview": {
            "thesis": main_thesis,
            "abstract": abstract,
            "target_words": 4000,
            "sections_count": len(sections)
        },
        "sections": sections,
        "content_bank": content_bank,
        "raw_inputs": {
            "abstract_framework": abstract_framework,
            "developed_moves": developed_moves,
            "detailed_outline": detailed_outline,
            "literature_context": literature_context
        }
    }


def run_phase_2_6():
    """Run Phase II.6: Create writing-optimized context for Phase III"""
    
    print("\n" + "="*60)
    print("PHASE II.6: Writing Context Optimization")
    print("="*60)
    print("\nConsolidating developed content for Phase III writing...")
    
    try:
        # Load all the developed content
        print("\n1. Loading abstract framework from Phase II.2...")
        abstract_framework = load_abstract_framework()
        print(f"   ✓ Loaded framework with thesis: {abstract_framework.get('main_thesis', 'N/A')[:100]}...")
        
        print("\n2. Loading developed key moves from Phase II.3...")
        developed_moves = load_developed_key_moves()
        print(f"   ✓ Loaded {len(developed_moves)} developed key moves")
        
        print("\n3. Loading detailed outline from Phase II.4...")
        detailed_outline = load_detailed_outline()
        print(f"   ✓ Loaded detailed outline")
        
        print("\n4. Loading literature context from Phase II.5...")
        literature_context = load_literature_context()
        print(f"   ✓ Loaded literature context")
        
        # Create writing-optimized context
        print("\n5. Creating writing-optimized context structure...")
        writing_context = create_writing_context(
            abstract_framework, developed_moves, detailed_outline, literature_context
        )
        
        print(f"   ✓ Structured {len(writing_context['sections'])} sections for writing")
        print(f"   ✓ Created content bank with {len(writing_context['content_bank']['arguments'])} arguments")
        
        # Save the writing context
        output_file = "./outputs/phase_3_writing_context.json"
        with open(output_file, "w") as f:
            json.dump(writing_context, f, indent=2)
        
        print(f"\n✓ Phase II.6 complete! Writing context saved to: {output_file}")
        
        # Print summary for review
        print("\n" + "-"*60)
        print("WRITING CONTEXT SUMMARY")
        print("-"*60)
        print(f"Paper thesis: {writing_context['paper_overview']['thesis'][:150]}...")
        print(f"Target length: {writing_context['paper_overview']['target_words']} words")
        print(f"Sections to write: {writing_context['paper_overview']['sections_count']}")
        
        print(f"\nSections:")
        for i, section in enumerate(writing_context['sections']):
            print(f"  {i+1}. {section['section_name']} ({section['word_target']} words)")
        
        print(f"\nContent bank:")
        print(f"  - {len(writing_context['content_bank']['arguments'])} developed arguments")
        print(f"  - {len(writing_context['content_bank']['examples'])} example sets")
        print(f"  - {len(writing_context['content_bank']['citations'])} citations identified")
        
        return writing_context
        
    except Exception as e:
        print(f"\n❌ Error in Phase II.6: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    run_phase_2_6() 