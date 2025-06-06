from typing import Dict, Any


class PaperIntegrationPrompts:
    """Prompts for integrating improvements into complete papers in Phase III.2"""
    
    def __init__(self):
        self.system_prompt = """You are an expert Analysis journal editor creating publication-ready papers. Your role is to integrate recommended improvements while preserving intellectual content and ensuring the final paper meets Analysis journal publication standards - conversational rigor, example-driven argumentation, and accessible presentation. You must deliver complete Analysis-quality papers ready for submission."""

        self.analysis_publication_standards = """
ANALYSIS JOURNAL PUBLICATION STANDARDS:

VOICE & ACCESSIBILITY REQUIREMENTS:
- Conversational but rigorous tone throughout
- Heavy first person usage: "I argue that...", "I will show...", "My response is...", "I contend that..."
- Direct reader engagement: "Consider this case...", "You might think...", "Notice that..."
- Short, clear sentences (15-25 words) - avoid complex subordination
- Technical terms defined immediately when introduced
- Professional but friendly tone - readable by general philosophy audience

STRUCTURAL REQUIREMENTS:
- Numbered sections (1, 2.1, 2.2, etc.) for clear organization
- Thesis clearly stated within first 300-400 words
- Preview sentences at section beginnings: "In this section, I will..."
- Explicit signposting throughout: "This suggests...", "It follows that...", "However..."
- Smooth transitions using Analysis-style patterns

EXAMPLE-DRIVEN ARGUMENTATION:
- Concrete examples introduced early (by second paragraph)
- Examples must do argumentative work, not just illustrate
- Core examples revisited from multiple analytical angles
- Systematic development: Concrete case → Analysis → General principle → Test against intuitions
- Examples should be immediately graspable scenarios

LITERATURE INTEGRATION:
- Strategic and minimal - focus on 2-3 key interlocutors maximum
- Inline citations (Author Year: page) - avoid footnotes except for clarifications
- Brief context-setting rather than extended literature review
- Engage with specific claims, not general positions

DEVELOPMENT PATTERNS:
- Progressive refinement rather than dramatic turns
- Systematic rather than surprising development
- Address objections throughout text, not in dedicated section
- Clear transition patterns: "However...", "On the other hand...", "This suggests..."

ANALYSIS EFFICIENCY STANDARDS:
- Every word must earn its place - no unnecessary elaboration
- Target 2000-4000 words total (efficiency over comprehensiveness)
- Clean, professional presentation suitable for Analysis readership
"""

    def construct_integration_prompt(self, draft_paper: str, paper_analysis: str, 
                                   paper_overview: Dict[str, Any]) -> str:
        """Generate prompt for integrating improvements into Analysis-quality paper"""
        
        total_words = len(draft_paper.split())
        
        return f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase III.2 (Global Integration).
You are creating the final, Analysis journal publication-ready version of the philosophy paper.
You have access to Analysis journal papers as style exemplars.
Your task is to integrate improvements while ensuring Analysis publication standards.
IMPORTANT: This is an automated API call. Deliver the COMPLETE final paper immediately.
</context>

<analysis_publication_standards>
{self.analysis_publication_standards}
</analysis_publication_standards>

<task>
Create the final, Analysis journal publication-ready version of the philosophy paper.
Integrate all recommended improvements from the analysis.
Ensure the paper meets Analysis journal publication standards throughout.
Deliver the complete paper ready for submission to Analysis journal.
Do NOT ask if you should continue - deliver the full paper immediately.
</task>

<paper_information>
THESIS: {paper_overview['thesis']}
TARGET LENGTH: {paper_overview['target_words']} words
CURRENT LENGTH: {total_words} words
TARGET JOURNAL: Analysis
ABSTRACT: {paper_overview['abstract']}
</paper_information>

<integration_principles>
1. PRESERVE INTELLECTUAL CONTENT - Maintain core arguments, evidence, and philosophical positions
2. ACHIEVE ANALYSIS STYLE - Implement conversational rigor and example-driven argumentation
3. ENHANCE ACCESSIBILITY - Make sophisticated arguments accessible to Analysis readership
4. ENSURE EFFICIENCY - Every word must earn its place (Analysis standard)
5. MAINTAIN THESIS FOCUS - Every element clearly supports the main argument
6. TAKE PHILOSOPHICAL STANDS (RLHF-Proofing) - Your training wants you to hedge and equivocate. RESIST:
   - Keep bold claims bold: "I argue X" not "This paper explores whether X"
   - Maintain strong positions: "This view fails" not "This view faces challenges"
   - State controversial implications clearly, don't bury them
   - Philosophy advances through defendable claims, not surveys of possibilities
</integration_principles>

<current_draft>
{draft_paper}
</current_draft>

<analysis_and_recommendations>
{paper_analysis}
</analysis_and_recommendations>

<analysis_integration_instructions>
1. ANALYSIS VOICE IMPLEMENTATION
   - Convert to conversational but rigorous tone throughout
   - Add heavy first person usage ("I argue...", "I will show...", "My response is...")
   - Include direct reader engagement ("Consider...", "Notice that...", "You might think...")
   - Ensure short, clear sentences (15-25 words average)
   - Define technical terms immediately upon introduction

2. ANALYSIS STRUCTURAL PATTERNS
   - Implement numbered sections (1, 2.1, 2.2, etc.) for clear organization
   - Ensure thesis clearly stated within first 300-400 words
   - Add preview sentences at section beginnings ("In this section, I will...")
   - Include explicit signposting ("This suggests...", "It follows that...", "However...")

3. EXAMPLE-DRIVEN ARGUMENTATION
   - Ensure concrete examples introduced early (by second paragraph)
   - Make examples do genuine argumentative work, not just illustration
   - Revisit core examples from multiple analytical angles throughout
   - Follow pattern: Concrete case → Analysis → General principle → Test against intuitions

4. ANALYSIS LITERATURE INTEGRATION
   - Streamline to strategic, minimal literature use (2-3 key interlocutors maximum)
   - Use inline citations (Author Year: page) consistently
   - Provide brief context-setting rather than extended literature review
   - Engage with specific claims, not general positions

5. ANALYSIS DEVELOPMENT PATTERNS
   - Ensure progressive refinement rather than dramatic turns
   - Make development systematic rather than surprising
   - Address objections throughout text, not in dedicated section
   - Use clear Analysis transition patterns ("However...", "On the other hand...")

6. FINAL ANALYSIS POLISH
   - Ensure every word earns its place (efficiency over comprehensiveness)
   - Target appropriate length for Analysis (typically 2000-4000 words)
   - Polish to publication-ready quality for Analysis readership
   - Maintain professional but friendly tone throughout
</analysis_integration_instructions>

<output_format>
Provide ONLY the complete final paper in markdown format following Analysis journal standards.
Start immediately with a concise, professional title (maximum 10 words).
Continue through all sections without interruption in Analysis journal style.
Do not include meta-commentary, summaries, or requests for continuation.
The paper should meet Analysis publication standards and be approximately {paper_overview['target_words']} words.
</output_format>

<requirements>
- Create a concise, professional academic title suitable for Analysis
- Deliver the COMPLETE paper from title to conclusion
- Implement Analysis journal style throughout (conversational rigor, examples, accessibility)
- Ensure all improvements are smoothly integrated while maintaining Analysis standards
- Stay within target word count while meeting Analysis efficiency standards
- Make the paper publication-ready for Analysis journal submission
</requirements>"""
    
    def get_system_prompt(self) -> str:
        """Return the system prompt for API calls"""
        return self.system_prompt 