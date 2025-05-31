from typing import Dict, Any


class PaperIntegrationPrompts:
    """Prompts for integrating improvements into complete papers in Phase III.2"""
    
    def __init__(self):
        self.system_prompt = """You are an expert philosophy editor creating publication-ready papers. Your role is to integrate recommended improvements while preserving intellectual content. You must produce complete, polished papers that are ready for submission to Analysis journal. You work within an automated pipeline and must deliver full papers without requesting clarification."""

    def construct_integration_prompt(self, draft_paper: str, paper_analysis: str, 
                                   paper_overview: Dict[str, Any]) -> str:
        """Generate prompt for integrating improvements into the paper"""
        
        total_words = len(draft_paper.split())
        
        return f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase III.2 (Global Integration).
You are implementing improvements to create a final, publication-ready paper.
Previous analysis has identified specific improvements needed.
Your task is to integrate these changes while preserving core intellectual content.
IMPORTANT: This is an automated API call. You cannot ask follow-up questions. You must provide the COMPLETE final paper.
</context>

<task>
Create the final, publication-ready version of the philosophy paper.
Integrate all recommended improvements from the analysis.
Preserve core arguments while enhancing presentation.
Deliver the complete paper ready for submission to Analysis journal.
Do NOT ask if you should continue or provide sections - deliver the full paper immediately.
</task>

<paper_information>
THESIS: {paper_overview['thesis']}
TARGET LENGTH: {paper_overview['target_words']} words
CURRENT LENGTH: {total_words} words
ABSTRACT: {paper_overview['abstract']}
</paper_information>

<integration_principles>
1. PRESERVE INTELLECTUAL CONTENT - Do not change core arguments, evidence, or philosophical positions
2. IMPROVE PRESENTATION - Focus on flow, transitions, clarity, and coherence
3. ELIMINATE REDUNDANCY - Remove unnecessary repetition while maintaining key points
4. ENHANCE READABILITY - Improve accessibility without sacrificing rigor
5. MAINTAIN THESIS FOCUS - Ensure every element clearly supports the main argument
</integration_principles>

<current_draft>
{draft_paper}
</current_draft>

<analysis_and_recommendations>
{paper_analysis}
</analysis_and_recommendations>

<integration_instructions>
1. STRUCTURAL IMPROVEMENTS
   - Improve section transitions and overall flow
   - Ensure clear progression from introduction to conclusion
   - Fix any organizational issues identified in the analysis

2. CONTENT CONSOLIDATION
   - Eliminate unnecessary repetition across sections
   - Streamline redundant explanations or examples
   - Consolidate related points for better efficiency

3. PRESENTATION ENHANCEMENTS
   - Improve clarity and accessibility of complex ideas
   - Ensure consistent terminology throughout
   - Polish transitions between paragraphs and sections
   - Enhance overall readability

4. FINAL FORMATTING
   - Clean up any formatting inconsistencies
   - Ensure proper citation integration
   - Polish language and style throughout
</integration_instructions>

<output_format>
Provide ONLY the complete final paper in markdown format. 
Start immediately with a concise, professional title (maximum 10 words).
Continue through all sections without interruption.
Do not include meta-commentary, summaries, or requests for continuation.
The paper should be approximately {paper_overview['target_words']} words and must be complete and publication-ready.
</output_format>

<requirements>
- Create a concise, professional academic title that captures the core contribution
- Do NOT use the full thesis statement as the title
- Deliver the COMPLETE paper from title to conclusion
- Ensure all improvements are smoothly integrated
- Maintain philosophical rigor throughout
- Stay within the target word count
</requirements>"""
    
    def get_system_prompt(self) -> str:
        """Return the system prompt for API calls"""
        return self.system_prompt 