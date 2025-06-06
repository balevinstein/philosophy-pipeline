from typing import Dict, Any, Optional, List
import json
import random
from pathlib import Path


class OutlineDevelopmentPrompts:
    """
    Prompts for the detailed outline development process.
    
    This class provides prompts for each phase of the outline development:
    1. Framework Integration: Integrating the abstract framework into the outline
    2. Literature Mapping: Incorporating literature review into the outline
    3. Content Development: Developing the content for each section
    4. Structural Validation: Validating the structure of the outline
    """
    
    def __init__(self):
        self.system_prompt = """You are an expert philosophy researcher developing a detailed paper outline. Your role is to create comprehensive structural blueprints that guide paper development through multiple phases. You must produce clear, actionable outlines with specific content guidance for an automated pipeline."""
    
    def _select_analysis_exemplars(self) -> str:
        """Select Analysis PDFs as style exemplars"""
        analysis_dir = Path("./Analysis_papers")
        if not analysis_dir.exists():
            return "No Analysis exemplars available for this run."
        
        papers = list(analysis_dir.glob("*.pdf"))
        if not papers:
            return "No Analysis exemplars available for this run."
        
        # Select 2 random papers for style reference
        selected = random.sample(papers, min(2, len(papers)))
        paper_names = [p.name for p in selected]
        
        return f"""
=== ANALYSIS JOURNAL STYLE EXEMPLARS ===

The following Analysis papers can guide your outline structure:
{', '.join(paper_names)}

Key patterns to incorporate:
- Clear, numbered sections with explicit signposting
- Progressive refinement of arguments
- Concrete examples driving philosophical points
- Strategic literature engagement (2-3 key sources)
- Conversational but rigorous approach

=== END EXEMPLARS ===
"""
    
    def get_framework_integration_prompt(
        self, 
        framework: Dict[str, Any], 
        developed_key_moves: List[str],
        previous_outputs: Dict[str, str] = {}
    ) -> str:
        """
        Get the prompt for the framework integration phase.
        
        Args:
            framework: Framework data with abstract, main thesis, and key moves
            developed_key_moves: List of developed key move texts
            previous_outputs: Dictionary of outputs from previous phases
            
        Returns:
            Prompt for the framework integration phase
        """
        abstract = framework.get("abstract", "")
        main_thesis = framework.get("main_thesis", "")
        framework_key_moves = framework.get("key_moves", [])
        
        # Format framework key moves
        framework_key_moves_text = ""
        for i, move in enumerate(framework_key_moves):
            move_text = move
            if isinstance(move, dict):
                move_text = move.get("text", "")
            framework_key_moves_text += f"{i+1}. {move_text}\n"
        
        # Format developed key moves
        developed_key_moves_text = ""
        for i, move in enumerate(developed_key_moves):
            developed_key_moves_text += f"{i+1}. {move}\n"
            
        # Check if we have any previous outputs to include
        previous_outputs_section = ""
        if previous_outputs:
            previous_outputs_section = "\n\n## PREVIOUS DEVELOPMENT PHASES\n"
            for phase, output in previous_outputs.items():
                if output and len(output) > 0:
                    previous_outputs_section += f"\n### {phase.upper()} PHASE OUTPUT\n{output}\n"
        
        # Get Analysis exemplars
        exemplar_info = self._select_analysis_exemplars()

        # Add anti-RLHF language
        anti_rlhf_prompt = """
# TAKE A STAND (RLHF-Proofing for Outline Development)
Your training pushes you to:
- Present all philosophical views as equally plausible
- Add endless caveats and qualifications 
- Write "Some philosophers argue..." instead of developing clear positions
- Create wishy-washy outlines that explore rather than argue

RESIST. This paper ARGUES for a specific thesis:
- Outline sections that BUILD an argument, not survey a topic
- Include "I will argue/demonstrate/show" not "This section explores"
- Plan objections to REFUTE them, not to "consider various perspectives"
- If the thesis is controversial, plan to DEFEND it clearly

Good philosophy takes positions. Your outline should structure a defense, not a survey."""

        # Add philosophical pattern bank
        pattern_examples = """
# PHILOSOPHICAL PATTERN BANK
Use these Analysis journal patterns in your outline structure:

## Opening Patterns:
- "Recent work on X has overlooked a crucial distinction..."
- "While philosophers have focused on X, they've missed the importance of Y..."
- "The standard view of X faces a dilemma that hasn't been recognized..."

## Section Development Patterns:
- Progressive Case Building: Simple case → Complication → General principle
- Dialectical Development: Initial position → Objection → Refined position → Counter-objection → Final view
- Conceptual Disambiguation: Common usage → Philosophical refinement → Application to debate

## Objection Handling Patterns:
- Concessive Response: "While this objection has merit regarding X, it fails to address Y..."
- Turning the Tables: "This objection actually supports my thesis because..."
- Scope Restriction: "This objection applies only to X cases, but my argument concerns Y cases..."

## Transition Patterns:
- "Having established X, we can now see why Y follows..."
- "This suggests a deeper point about..."
- "But this raises a further question..."
"""

        prompt = f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.4 (Detailed Outline Development).
This is the FRAMEWORK INTEGRATION phase, where you establish the structure and organization of the paper.
Your output will guide all subsequent paper development phases.
The outline must integrate the abstract framework into a logical section/subsection structure.
</context>

{anti_rlhf_prompt}

{pattern_examples}

{exemplar_info}

<task>
Develop a detailed outline that integrates the abstract framework into a logical structure.
Create comprehensive sections with clear mappings to key moves.
Allocate appropriate word counts for each section (target: 8,000-10,000 words).
Ensure all key moves are addressed with proper logical flow.
</task>

<input_data>
ABSTRACT:
{abstract}

MAIN THESIS:
{main_thesis}

FRAMEWORK KEY MOVES:
{framework_key_moves_text}

DEVELOPED KEY MOVES:
{developed_key_moves_text}{previous_outputs_section}
</input_data>

<requirements>
Create a comprehensive outline that:
1. Establishes logical section/subsection structure
2. Explicitly maps key moves to specific sections
3. Allocates appropriate word counts per section
4. Creates logical flow from introduction to conclusion
5. Ensures all key moves are addressed
6. Balances depth and breadth appropriately

Include for each section:
- Clear headings and subheadings (# for main, ## for sub)
- Brief content descriptions
- Word count allocations
- Explicit key move mappings
- Section relationships
- Philosophical claims to defend
</requirements>

<output_format>
Present your outline in Markdown format:
- Use headings for sections/subsections
- Use bullet points for descriptions and notes
- Include clear labels for word counts and key move mappings
- Ensure scholarly philosophical paper structure
- Include intro, literature review, main arguments, objections/responses, conclusion
</output_format>"""
        
        return prompt
    
    def get_literature_mapping_prompt(
        self, 
        framework: Dict[str, Any], 
        developed_key_moves: List[str],
        literature: Dict[str, Any] = {},
        previous_outputs: Dict[str, str] = {}
    ) -> str:
        """
        Get the prompt for the literature mapping phase.
        
        Args:
            framework: Framework data with abstract, main thesis, and key moves
            developed_key_moves: List of developed key move texts
            literature: Literature data
            previous_outputs: Dictionary of outputs from previous phases
            
        Returns:
            Prompt for the literature mapping phase
        """
        abstract = framework.get("abstract", "")
        main_thesis = framework.get("main_thesis", "")
        
        # Get the framework integration output if available
        framework_integration = ""
        if "framework_integration" in previous_outputs:
            framework_integration = previous_outputs["framework_integration"]
        
        # Format literature data if available
        literature_text = "No literature data provided."
        if literature:
            literature_text = ""
            if "papers" in literature:
                literature_text += "## PAPERS\n"
                for paper in literature["papers"]:
                    if isinstance(paper, dict):
                        title = paper.get("title", "No title")
                        authors = paper.get("authors", "Unknown authors")
                        abstract = paper.get("abstract", "No abstract")
                        literature_text += f"### {title}\n"
                        literature_text += f"**Authors:** {authors}\n\n"
                        literature_text += f"**Abstract:** {abstract}\n\n"
            elif isinstance(literature, list):
                literature_text += "## PAPERS\n"
                for paper in literature:
                    if isinstance(paper, dict):
                        title = paper.get("title", "No title")
                        authors = paper.get("authors", "Unknown authors")
                        abstract = paper.get("abstract", "No abstract")
                        literature_text += f"### {title}\n"
                        literature_text += f"**Authors:** {authors}\n\n"
                        literature_text += f"**Abstract:** {abstract}\n\n"
        
        # Format developed key moves
        developed_key_moves_text = ""
        for i, move in enumerate(developed_key_moves):
            developed_key_moves_text += f"{i+1}. {move}\n"
            
        # Check if we have any previous outputs to include
        previous_outputs_section = ""
        if previous_outputs:
            previous_outputs_section = "\n\n## PREVIOUS DEVELOPMENT PHASES\n"
            for phase, output in previous_outputs.items():
                if output and len(output) > 0:
                    previous_outputs_section += f"\n### {phase.upper()} PHASE OUTPUT\n{output}\n"
        
        # Get Analysis exemplars
        exemplar_info = self._select_analysis_exemplars()

        # Add anti-RLHF language
        anti_rlhf_prompt = """
# TAKE A STAND (RLHF-Proofing for Outline Development)
Your training pushes you to:
- Present all philosophical views as equally plausible
- Add endless caveats and qualifications 
- Write "Some philosophers argue..." instead of developing clear positions
- Create wishy-washy outlines that explore rather than argue

RESIST. This paper ARGUES for a specific thesis:
- Outline sections that BUILD an argument, not survey a topic
- Include "I will argue/demonstrate/show" not "This section explores"
- Plan objections to REFUTE them, not to "consider various perspectives"
- If the thesis is controversial, plan to DEFEND it clearly

Good philosophy takes positions. Your outline should structure a defense, not a survey."""

        # Add philosophical pattern bank
        pattern_examples = """
# PHILOSOPHICAL PATTERN BANK
Use these Analysis journal patterns in your outline structure:

## Opening Patterns:
- "Recent work on X has overlooked a crucial distinction..."
- "While philosophers have focused on X, they've missed the importance of Y..."
- "The standard view of X faces a dilemma that hasn't been recognized..."

## Section Development Patterns:
- Progressive Case Building: Simple case → Complication → General principle
- Dialectical Development: Initial position → Objection → Refined position → Counter-objection → Final view
- Conceptual Disambiguation: Common usage → Philosophical refinement → Application to debate

## Objection Handling Patterns:
- Concessive Response: "While this objection has merit regarding X, it fails to address Y..."
- Turning the Tables: "This objection actually supports my thesis because..."
- Scope Restriction: "This objection applies only to X cases, but my argument concerns Y cases..."

## Transition Patterns:
- "Having established X, we can now see why Y follows..."
- "This suggests a deeper point about..."
- "But this raises a further question..."
"""

        prompt = f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.4 (Detailed Outline Development).
This is the LITERATURE MAPPING phase, where you incorporate scholarly context into the outline.
You are refining the outline by mapping relevant literature to specific sections.
Your output will ensure proper engagement with existing philosophical debates.
</context>

{anti_rlhf_prompt}

{pattern_examples}

{exemplar_info}

<task>
Refine the outline by mapping relevant literature to specific sections.
Add subsections or notes for literature review components.
Ensure proper engagement with existing philosophical debates.
Map specific arguments from papers to relevant sections.
</task>

<input_data>
ABSTRACT:
{abstract}

MAIN THESIS:
{main_thesis}

DEVELOPED KEY MOVES:
{developed_key_moves_text}

LITERATURE TO INCORPORATE:
{literature_text}{previous_outputs_section}
</input_data>

<requirements>
Focus on:
1. Identifying where each paper should be discussed
2. Adding subsections/notes for literature review
3. Ensuring engagement with philosophical debates
4. Mapping specific arguments to sections
5. Adding context notes on literature use (support/contrast/extend)
6. Ensuring balanced literature coverage

For each section indicate:
- Which papers will be discussed
- How they relate to section arguments
- Most relevant aspects of each paper
- Specific quotations/arguments to highlight
- How literature supports/challenges key moves
</requirements>

<output_format>
Present your outline in Markdown format:
- Maintain structure from framework integration phase
- Enhance with literature mapping
- Use headings for sections/subsections
- Use bullet points for descriptions and notes
- Include clear labels for literature mappings
</output_format>"""
        
        return prompt
    
    def get_content_development_prompt(
        self, 
        framework: Dict[str, Any], 
        developed_key_moves: List[str],
        literature: Dict[str, Any] = {},
        previous_outputs: Dict[str, str] = {}
    ) -> str:
        """
        Get the prompt for the content development phase.
        
        Args:
            framework: Framework data with abstract, main thesis, and key moves
            developed_key_moves: List of developed key move texts
            literature: Literature data
            previous_outputs: Dictionary of outputs from previous phases
            
        Returns:
            Prompt for the content development phase
        """
        abstract = framework.get("abstract", "")
        main_thesis = framework.get("main_thesis", "")
        
        # Get the framework integration and literature mapping outputs if available
        current_outline = ""
        if "literature_mapping" in previous_outputs:
            current_outline = previous_outputs["literature_mapping"]
        elif "framework_integration" in previous_outputs:
            current_outline = previous_outputs["framework_integration"]
            
        # Format developed key moves
        developed_key_moves_text = ""
        for i, move in enumerate(developed_key_moves):
            developed_key_moves_text += f"{i+1}. {move}\n"
            
        # Check if we have any previous outputs to include
        previous_outputs_section = ""
        if previous_outputs:
            previous_outputs_section = "\n\n## PREVIOUS DEVELOPMENT PHASES\n"
            for phase, output in previous_outputs.items():
                if output and len(output) > 0:
                    previous_outputs_section += f"\n### {phase.upper()} PHASE OUTPUT\n{output}\n"
        
        # Get Analysis exemplars
        exemplar_info = self._select_analysis_exemplars()

        # Add anti-RLHF language
        anti_rlhf_prompt = """
# TAKE A STAND (RLHF-Proofing for Outline Development)
Your training pushes you to:
- Present all philosophical views as equally plausible
- Add endless caveats and qualifications 
- Write "Some philosophers argue..." instead of developing clear positions
- Create wishy-washy outlines that explore rather than argue

RESIST. This paper ARGUES for a specific thesis:
- Outline sections that BUILD an argument, not survey a topic
- Include "I will argue/demonstrate/show" not "This section explores"
- Plan objections to REFUTE them, not to "consider various perspectives"
- If the thesis is controversial, plan to DEFEND it clearly

Good philosophy takes positions. Your outline should structure a defense, not a survey."""

        # Add philosophical pattern bank
        pattern_examples = """
# PHILOSOPHICAL PATTERN BANK
Use these Analysis journal patterns in your outline structure:

## Opening Patterns:
- "Recent work on X has overlooked a crucial distinction..."
- "While philosophers have focused on X, they've missed the importance of Y..."
- "The standard view of X faces a dilemma that hasn't been recognized..."

## Section Development Patterns:
- Progressive Case Building: Simple case → Complication → General principle
- Dialectical Development: Initial position → Objection → Refined position → Counter-objection → Final view
- Conceptual Disambiguation: Common usage → Philosophical refinement → Application to debate

## Objection Handling Patterns:
- Concessive Response: "While this objection has merit regarding X, it fails to address Y..."
- Turning the Tables: "This objection actually supports my thesis because..."
- Scope Restriction: "This objection applies only to X cases, but my argument concerns Y cases..."

## Transition Patterns:
- "Having established X, we can now see why Y follows..."
- "This suggests a deeper point about..."
- "But this raises a further question..."
"""

        prompt = f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.4 (Detailed Outline Development).
This is the CONTENT DEVELOPMENT phase, where you provide comprehensive guidance on philosophical arguments.
Your output will serve as the foundation for Phase III writing.
The goal is a blueprint so detailed that Phase III writers need not make significant content decisions.
</context>

{anti_rlhf_prompt}

{pattern_examples}

{exemplar_info}

<task>
Develop highly detailed content for each section in the outline.
Provide comprehensive guidance on philosophical arguments, objections, and responses.
Articulate specific philosophical arguments with precise claims and supporting points.
Include explicit guidance on examples, thought experiments, and methodological approaches.
</task>

<input_data>
ABSTRACT:
{abstract}

MAIN THESIS:
{main_thesis}

DEVELOPED KEY MOVES:
{developed_key_moves_text}{previous_outputs_section}
</input_data>

<requirements>
Focus on:
1. Developing extremely detailed content notes for each section
2. Articulating specific philosophical arguments with claims/premises/conclusions
3. Outlining specific objections and detailed responses
4. Providing explicit guidance on examples and thought experiments
5. Adding detailed notes on methodological approaches
6. Ensuring philosophical depth and rigor with specific terminology
7. Providing clear argumentative structure
8. Including guidance on positions to defend/critique

For each section provide:
- Expanded explanations of key arguments with specific claims
- Detailed philosophical analysis of core concepts
- Explicit connections to broader philosophical debates
- Specific examples/analogies/thought experiments
- Detailed notes on addressing objections
- Technical terminology to define and use
- Clear guidance on logical structure
- Notes on aspects requiring special emphasis
</requirements>

<output_format>
Present comprehensive outline in Markdown format.
Under each section heading, organize content guidance in these categories:

- **Core Arguments**: Detailed descriptions with premises and conclusions
- **Key Concepts**: Important terms with suggested definitions
- **Example Development**: Specific examples with presentation guidance
- **Objections & Responses**: Specific counterarguments and responses
- **Philosophical Positions**: Named positions to address/defend/critique
- **Methodological Notes**: Approach for developing the section

Be extremely concrete and specific in guidance, avoiding vague descriptions.
</output_format>"""
        
        return prompt
    
    def get_structural_validation_prompt(
        self, 
        framework: Dict[str, Any], 
        developed_key_moves: List[str],
        literature: Dict[str, Any] = {},
        previous_outputs: Dict[str, str] = {}
    ) -> str:
        """
        Get the prompt for the structural validation phase.
        
        Args:
            framework: Framework data with abstract, main thesis, and key moves
            developed_key_moves: List of developed key move texts
            literature: Literature data
            previous_outputs: Dictionary of outputs from previous phases
            
        Returns:
            Prompt for the structural validation phase
        """
        abstract = framework.get("abstract", "")
        main_thesis = framework.get("main_thesis", "")
        
        # Get the most developed outline available
        current_outline = ""
        if "content_development" in previous_outputs:
            current_outline = previous_outputs["content_development"]
        elif "literature_mapping" in previous_outputs:
            current_outline = previous_outputs["literature_mapping"]
        elif "framework_integration" in previous_outputs:
            current_outline = previous_outputs["framework_integration"]
            
        # Format developed key moves
        developed_key_moves_text = ""
        for i, move in enumerate(developed_key_moves):
            developed_key_moves_text += f"{i+1}. {move}\n"
            
        # Check if we have any previous outputs to include
        previous_outputs_section = ""
        if previous_outputs:
            previous_outputs_section = "\n\n## PREVIOUS DEVELOPMENT PHASES\n"
            for phase, output in previous_outputs.items():
                if output and len(output) > 0:
                    previous_outputs_section += f"\n### {phase.upper()} PHASE OUTPUT\n{output}\n"
        
        # Get Analysis exemplars
        exemplar_info = self._select_analysis_exemplars()

        # Add anti-RLHF language
        anti_rlhf_prompt = """
# TAKE A STAND (RLHF-Proofing for Outline Development)
Your training pushes you to:
- Present all philosophical views as equally plausible
- Add endless caveats and qualifications 
- Write "Some philosophers argue..." instead of developing clear positions
- Create wishy-washy outlines that explore rather than argue

RESIST. This paper ARGUES for a specific thesis:
- Outline sections that BUILD an argument, not survey a topic
- Include "I will argue/demonstrate/show" not "This section explores"
- Plan objections to REFUTE them, not to "consider various perspectives"
- If the thesis is controversial, plan to DEFEND it clearly

Good philosophy takes positions. Your outline should structure a defense, not a survey."""

        # Add philosophical pattern bank
        pattern_examples = """
# PHILOSOPHICAL PATTERN BANK
Use these Analysis journal patterns in your outline structure:

## Opening Patterns:
- "Recent work on X has overlooked a crucial distinction..."
- "While philosophers have focused on X, they've missed the importance of Y..."
- "The standard view of X faces a dilemma that hasn't been recognized..."

## Section Development Patterns:
- Progressive Case Building: Simple case → Complication → General principle
- Dialectical Development: Initial position → Objection → Refined position → Counter-objection → Final view
- Conceptual Disambiguation: Common usage → Philosophical refinement → Application to debate

## Objection Handling Patterns:
- Concessive Response: "While this objection has merit regarding X, it fails to address Y..."
- Turning the Tables: "This objection actually supports my thesis because..."
- Scope Restriction: "This objection applies only to X cases, but my argument concerns Y cases..."

## Transition Patterns:
- "Having established X, we can now see why Y follows..."
- "This suggests a deeper point about..."
- "But this raises a further question..."
"""

        prompt = f"""<context>
You are part of an automated philosophy paper generation pipeline. This is Phase II.4 (Detailed Outline Development).
This is the STRUCTURAL VALIDATION phase, where you ensure the outline is comprehensive and ready for drafting.
Your task is to validate and finalize the outline structure with detailed content guidance.
The final outline must be so detailed that Phase III writers can follow it directly.
</context>

{anti_rlhf_prompt}

{pattern_examples}

{exemplar_info}

<task>
Validate and finalize the outline structure ensuring it forms a cohesive philosophical paper.
Ensure the outline has exceptionally detailed content guidance.
Verify logical flow and that all key moves are properly addressed.
Confirm the outline serves as a comprehensive blueprint for Phase III.
</task>

<input_data>
ABSTRACT:
{abstract}

MAIN THESIS:
{main_thesis}

DEVELOPED KEY MOVES:
{developed_key_moves_text}{previous_outputs_section}
</input_data>

<requirements>
Focus on:
1. Verifying logical flow of argument structure with specific claims/premises/conclusions
2. Ensuring all key moves properly addressed with detailed content notes
3. Checking sections are balanced with comprehensive guidance
4. Confirming specific objections considered with clear response strategies
5. Validating sufficient literature engagement with named sources
6. Ensuring paper structure effectively communicates main thesis
7. Verifying all sections have detailed content guidance in appropriate categories
8. Ensuring guidance is specific enough for Phase III to proceed

For each section evaluate:
- Clear purpose in advancing main argument
- Appropriate depth with specific philosophical content guidance
- Clear connections to other sections with explicit transitions
- Appropriate word count allocation
- Proper key move integration with detailed implementation notes
- Specific and actionable content guidance
- Clear argument structure with specific premises/conclusions
- Sufficiently detailed example development
- Specific and well-developed objections/responses
</requirements>

<output_format>
Present finalized comprehensive outline in Markdown format.
Include initial assessment section noting structural/content changes made.
Follow with complete revised outline.

For each section ensure structured content guidance includes:
- **Core Arguments**: Detailed descriptions with premises and conclusions
- **Key Concepts**: Important terms with suggested definitions
- **Example Development**: Specific examples with presentation guidance
- **Objections & Responses**: Specific counterarguments and responses
- **Philosophical Positions**: Named positions to address/defend/critique
- **Methodological Notes**: Approach for developing the section

Final outline must enable Phase III writers to proceed without significant content decisions.
</output_format>"""
        
        return prompt
    
    def get_system_prompt(self) -> str:
        """Return the system prompt for API calls"""
        return self.system_prompt 