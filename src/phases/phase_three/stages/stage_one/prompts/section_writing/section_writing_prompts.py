import json
from typing import Dict, Any


class SectionWritingPrompts:
    """Prompts for section-by-section writing"""

    def __init__(self):
        self.system_prompt = """You are an expert philosophy writer crafting sections for publication in Analysis journal. Your role is to write philosophically rigorous sections that advance the paper's thesis while maintaining clarity and precision. You must produce publication-ready prose within strict word limits. Your writing will be used in an automated pipeline."""
        
        self.context = """You are writing a section for a philosophy paper for Analysis, a journal with a strict 4,000 word limit. Your task is to write one specific section that contributes to the overall argument while maintaining philosophical rigor and clarity.

You have access to:
1. The complete paper overview (thesis, abstract, roadmap)
2. Detailed guidance for this specific section
3. A content bank of developed arguments and examples
4. The full context from previous phases

Your writing should:
- Be philosophically rigorous and well-argued
- Use clear, precise language appropriate for Analysis
- Stay within the target word count for this section
- Connect smoothly to other sections
- Draw effectively from the content bank when relevant"""

        self.output_requirements = """
OUTPUT REQUIREMENTS:
1. Response must be valid JSON with NO literal newlines in string values
2. Use \\n for line breaks within strings (properly escaped)
3. Use simple ASCII characters only (no special quotes or unicode) 
4. Keep all text fields clear and well-formed
5. The "section_content" should be a single string with \\n for paragraph breaks
6. Target the specified word count (aim within 50 words)
7. Include section transitions and connections
8. Reference content bank arguments when appropriate

CRITICAL: Ensure all JSON is properly escaped - no unescaped newlines, quotes, or control characters."""

        self.output_format = """
{
    "section_content": "The complete written section with all paragraphs and arguments",
    "word_count": actual_word_count_number,
    "content_bank_usage": [
        "List of specific arguments/examples used from content bank"
    ],
    "section_notes": "Brief notes on approach, challenges, or connections to other sections",
    "transition_points": {
        "opening_connection": "How this section connects to previous content",
        "closing_transition": "How this section leads to the next section"
    }
}"""

    def construct_writing_prompt(self, writing_context: Dict[str, Any], section_index: int) -> str:
        """Generate prompt for writing a specific section"""
        
        section = writing_context["sections"][section_index]
        paper_overview = writing_context["paper_overview"]
        content_bank = writing_context["content_bank"]
        
        # Create section context
        previous_sections = []
        upcoming_sections = []
        
        for i, s in enumerate(writing_context["sections"]):
            if i < section_index:
                previous_sections.append(f"{i+1}. {s['section_name']}")
            elif i > section_index:
                upcoming_sections.append(f"{i+1}. {s['section_name']}")
        
        previous_context = "\n".join(previous_sections) if previous_sections else "None (this is the first section)"
        upcoming_context = "\n".join(upcoming_sections) if upcoming_sections else "None (this is the final section)"
        
        return f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase III.1 (Section Writing).
You are writing one specific section of a philosophy paper for Analysis journal.
Previous phases have developed the thesis, arguments, and detailed outline.
Your task is to write publication-ready prose for this specific section.
</context>

<task>
Write section {section_index + 1} of the philosophy paper: "{section['section_name']}"
Target {section['word_target']} words for this section.
Create philosophically rigorous prose that advances the paper's thesis.
Draw from the content bank of developed arguments when relevant.
</task>

<paper_information>
THESIS: {paper_overview['thesis']}
TARGET LENGTH: {paper_overview['target_words']} words total
ABSTRACT: {paper_overview['abstract'][:200]}...

CURRENT SECTION: Section {section_index + 1} - {section['section_name']}
TARGET WORDS: {section['word_target']}
</paper_information>

<section_guidance>
{section['content_guidance']}
</section_guidance>

<structural_context>
PREVIOUS SECTIONS:
{previous_context}

UPCOMING SECTIONS:
{upcoming_context}
</structural_context>

<content_bank>
ARGUMENTS READY FOR USE:
{json.dumps(content_bank['arguments'], indent=2)}

EXAMPLES AVAILABLE:
{json.dumps(content_bank['examples'], indent=2)}

CITATIONS IDENTIFIED:
{json.dumps(content_bank['citations'], indent=2)}
</content_bank>

<requirements>
{self.output_requirements}
</requirements>

<output_format>
{self.output_format}
</output_format>"""

    def construct_revision_prompt(self, writing_context: Dict[str, Any], section_index: int, 
                                current_content: str, revision_notes: str) -> str:
        """Generate prompt for revising a section based on feedback"""
        
        section = writing_context["sections"][section_index]
        
        return f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase III.1 (Section Writing).
You are revising a section based on feedback to improve its quality.
The core arguments must be preserved while enhancing presentation.
Your task is to create an improved version that addresses the critique.
</context>

<task>
Revise section {section_index + 1}: "{section['section_name']}"
Implement the revision guidance while maintaining philosophical rigor.
Stay within the target of {section['word_target']} words.
Preserve core arguments while improving presentation.
</task>

<current_section>
{current_content}
</current_section>

<revision_guidance>
{revision_notes}
</revision_guidance>

<requirements>
- Address all points in the revision guidance
- Maintain the section's core function in the paper
- Stay within the target word count
- Preserve philosophical rigor and clarity
- Ensure smooth transitions with other sections
{self.output_requirements}
</requirements>

<output_format>
{self.output_format}
</output_format>"""
    
    def get_system_prompt(self) -> str:
        """Return the system prompt for API calls"""
        return self.system_prompt 