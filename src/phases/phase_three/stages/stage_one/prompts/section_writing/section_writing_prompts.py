import json
from typing import Dict, Any


class SectionWritingPrompts:
    """Prompts for section-by-section writing"""

    def __init__(self):
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
        
        return f"""
{self.context}

PAPER OVERVIEW:
Thesis: {paper_overview['thesis']}
Target Length: {paper_overview['target_words']} words total
Abstract: {paper_overview['abstract'][:200]}...

CURRENT SECTION TO WRITE:
Section {section_index + 1}: {section['section_name']}
Target Words: {section['word_target']}

Content Guidance:
{section['content_guidance']}

STRUCTURAL CONTEXT:
Previous Sections:
{previous_context}

Upcoming Sections:
{upcoming_context}

CONTENT BANK AVAILABLE:
Arguments Ready for Use:
{json.dumps(content_bank['arguments'], indent=2)}

Examples Available:
{json.dumps(content_bank['examples'], indent=2)}

Citations Identified:
{json.dumps(content_bank['citations'], indent=2)}

{self.output_requirements}

Write the complete section following this format:
{self.output_format}

Focus on creating a well-argued, philosophically rigorous section that advances the paper's thesis while staying within the target word count."""

    def construct_revision_prompt(self, writing_context: Dict[str, Any], section_index: int, 
                                current_content: str, revision_notes: str) -> str:
        """Generate prompt for revising a section based on feedback"""
        
        section = writing_context["sections"][section_index]
        
        return f"""
{self.context}

You are revising a section based on feedback. Your task is to improve the section while maintaining its core function in the paper.

SECTION INFORMATION:
Section {section_index + 1}: {section['section_name']}
Target Words: {section['word_target']}

CURRENT SECTION CONTENT:
{current_content}

REVISION GUIDANCE:
{revision_notes}

Available Resources:
- Content bank with developed arguments and examples
- Paper overview and structural context
- Content guidance for this section

{self.output_requirements}

Provide the revised section in this format:
{self.output_format}

Focus on addressing the revision guidance while maintaining philosophical rigor and staying within the target word count.""" 