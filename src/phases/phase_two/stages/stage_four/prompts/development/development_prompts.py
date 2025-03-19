from typing import Dict, Any, Optional, List
import json


class OutlineDevelopmentPrompts:
    """
    Prompts for the detailed outline development process.
    
    This class provides prompts for each phase of the outline development:
    1. Framework Integration: Integrating the abstract framework into the outline
    2. Literature Mapping: Incorporating literature review into the outline
    3. Content Development: Developing the content for each section
    4. Structural Validation: Validating the structure of the outline
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
        
        prompt = f"""# DETAILED OUTLINE DEVELOPMENT: FRAMEWORK INTEGRATION PHASE

## ABSTRACT
{abstract}

## MAIN THESIS
{main_thesis}

## FRAMEWORK KEY MOVES
{framework_key_moves_text}

## DEVELOPED KEY MOVES
{developed_key_moves_text}{previous_outputs_section}

## INSTRUCTIONS
Your task is to develop a detailed outline for a philosophical paper that integrates the abstract framework into a logical section/subsection structure. This is the FRAMEWORK INTEGRATION phase, where you'll establish the structure and organization of the paper.

Focus on creating a comprehensive outline that:

1. Establishes a logical section/subsection structure for the paper
2. Explicitly maps key moves to specific sections
3. Allocates appropriate word counts for each section (target paper length: 8,000-10,000 words)
4. Creates a logical flow from introduction to conclusion
5. Ensures all key moves are addressed
6. Balances depth and breadth appropriately

The output should be a detailed outline with:

- Clear section headings and subheadings (using Markdown # for main sections, ## for subsections, etc.)
- Brief descriptions of the content for each section/subsection
- Word count allocations
- Explicit mapping of key moves to sections
- Notes on how sections will relate to each other
- Indications of which philosophical claims will be defended in each section

Ensure that your outline represents a scholarly philosophical paper structure, with appropriate introduction, literature review/background, main arguments, objections and responses, and conclusion sections.

## OUTPUT FORMAT
Present your output as a detailed outline in Markdown format. Use headings to indicate sections and subsections, bullet points for descriptions and notes, and clear labels for word counts and key move mappings.
"""
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
        
        prompt = f"""# DETAILED OUTLINE DEVELOPMENT: LITERATURE MAPPING PHASE

## ABSTRACT
{abstract}

## MAIN THESIS
{main_thesis}

## DEVELOPED KEY MOVES
{developed_key_moves_text}

## LITERATURE TO INCORPORATE
{literature_text}{previous_outputs_section}

## INSTRUCTIONS
Your task is to refine the outline by mapping relevant literature to specific sections. This is the LITERATURE MAPPING phase, where you'll incorporate scholarly context into the outline.

Focus on:

1. Identifying where each paper should be discussed in the outline
2. Adding subsections or notes for literature review components
3. Ensuring proper engagement with existing philosophical debates
4. Mapping specific arguments from papers to relevant sections
5. Adding context notes about how literature will be used (support, contrast, extend, etc.)
6. Ensuring balanced coverage of relevant literature

Maintain the structure from the framework integration phase, but enhance it with literature mapping. For each section, indicate:

- Which papers will be discussed
- How they relate to the arguments in that section
- What aspects of each paper are most relevant
- Any specific quotations or arguments that should be highlighted
- How the literature supports or challenges the key moves

## OUTPUT FORMAT
Present your output as a detailed outline in Markdown format. Use headings to indicate sections and subsections, bullet points for descriptions and notes, and clear labels for literature mappings.
"""
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
        
        prompt = f"""# DETAILED OUTLINE DEVELOPMENT: CONTENT DEVELOPMENT PHASE

## ABSTRACT
{abstract}

## MAIN THESIS
{main_thesis}

## DEVELOPED KEY MOVES
{developed_key_moves_text}{previous_outputs_section}

## INSTRUCTIONS
Your task is to develop highly detailed content for each section in the outline. This is the CONTENT DEVELOPMENT phase, where you'll provide comprehensive guidance on philosophical arguments, objections, and responses. Your output will serve as the foundation for Phase III writing.

Focus on:

1. Developing extremely detailed content notes for each section and subsection
2. Articulating the specific philosophical arguments to be made with precise claims and supporting points
3. Outlining specific objections and detailed responses with clear reasoning
4. Providing explicit guidance on examples and thought experiments, including how they should be presented
5. Adding detailed notes on methodological approaches for each section
6. Ensuring philosophical depth and rigor throughout with specific terminology and concepts
7. Providing clear argumentative structure with premises and conclusions
8. Including guidance on which positions to defend and which to critique

For each section, provide:

- Expanded explanations of key arguments with specific claims, premises, and conclusions
- Detailed philosophical analysis of core concepts with definitional guidance
- Explicit connections to broader philosophical debates with named positions
- Specific examples, analogies, or thought experiments with detailed descriptions
- Detailed notes on how objections will be addressed with specific counter-arguments
- Technical terminology to be defined and used with suggested definitions
- Clear guidance on the logical structure of each argument
- Notes on which aspects require special emphasis or elaboration

Maintain the structure from previous phases but add substantial content notes to make the outline extremely detailed and ready for drafting. The goal is to provide a comprehensive blueprint that Phase III writers can follow without needing to make significant content decisions.

## OUTPUT FORMAT
Present your output as a comprehensive outline in Markdown format. Use headings to indicate sections and subsections, followed by structured content guidance under each heading organized in these categories:

- **Core Arguments**: Detailed descriptions of specific arguments with premises and conclusions
- **Key Concepts**: Important terms to define with suggested definitions
- **Example Development**: Specific examples/analogies with guidance on presentation
- **Objections & Responses**: Specific counterarguments and detailed responses
- **Philosophical Positions**: Named positions to address, defend, or critique
- **Methodological Notes**: Approach to use in developing the section

Be extremely concrete and specific in your guidance, avoiding vague or general descriptions.
"""
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
        
        prompt = f"""# DETAILED OUTLINE DEVELOPMENT: STRUCTURAL VALIDATION PHASE

## ABSTRACT
{abstract}

## MAIN THESIS
{main_thesis}

## DEVELOPED KEY MOVES
{developed_key_moves_text}{previous_outputs_section}

## INSTRUCTIONS
Your task is to validate and finalize the outline structure, ensuring it forms a cohesive philosophical paper with exceptionally detailed content guidance. This is the STRUCTURAL VALIDATION phase, where you'll ensure the outline is comprehensive, balanced, well-structured, and ready for drafting in Phase III.

Focus on:

1. Verifying the logical flow of the argument structure and ensuring all arguments are presented with specific claims, premises, and conclusions
2. Ensuring all key moves are properly addressed with detailed content notes
3. Checking that sections are appropriately balanced and have comprehensive guidance
4. Confirming that specific objections are adequately considered with clear response strategies
5. Validating that the literature engagement is sufficient with named sources and positions
6. Making sure the paper structure will effectively communicate the main thesis
7. Verifying that all sections have detailed content guidance structured in appropriate categories 
8. Ensuring the guidance is specific enough that Phase III writers can proceed without making significant content decisions

For each section, evaluate:

- Whether it serves a clear purpose in advancing the main argument
- If it has appropriate depth and detail, with specific philosophical content guidance
- Whether connections to other sections are clear with explicit transitions
- If the word count allocation is appropriate
- Whether key moves are properly integrated with detailed implementation notes
- If the content guidance is specific and actionable, not vague or general
- Whether the argument structure is clearly articulated with specific premises and conclusions
- If example development is sufficiently detailed with clear implementation guidance
- Whether objections and responses are specific and well-developed

Then provide a revised, final outline that addresses any structural or content detail issues identified, ensuring it is a comprehensive blueprint for Phase III writing.

## OUTPUT FORMAT
Present your output as a finalized, comprehensive outline in Markdown format. Include an initial assessment section noting structural and content detail changes made, followed by the complete revised outline. 

For each section, ensure structured content guidance includes these explicit categories:
- **Core Arguments**: Detailed descriptions of specific arguments with premises and conclusions
- **Key Concepts**: Important terms to define with suggested definitions
- **Example Development**: Specific examples/analogies with guidance on presentation
- **Objections & Responses**: Specific counterarguments and detailed responses
- **Philosophical Positions**: Named positions to address, defend, or critique
- **Methodological Notes**: Approach to use in developing the section

The final outline must be so comprehensive and detailed that Phase III writers can follow it directly without needing to make significant content decisions on their own.
"""
        return prompt 