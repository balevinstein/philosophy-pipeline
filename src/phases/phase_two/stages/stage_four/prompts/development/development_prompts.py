from typing import Dict, Any, Optional, List
import json
import random
from pathlib import Path


class OutlineDevelopmentPrompts:
    """
    Streamlined prompts for the detailed outline development process.
    
    This class provides concise prompts for each phase of the outline development:
    1. Framework Integration: Integrating the abstract framework into the outline
    2. Literature Mapping: Incorporating literature review into the outline
    3. Content Development: Developing the content for each section
    4. Structural Validation: Validating the structure of the outline
    """
    
    def __init__(self):
        self.system_prompt = """You are an expert philosophy researcher developing a detailed paper outline."""
    
    def get_framework_integration_prompt(
        self, 
        framework: Dict[str, Any], 
        developed_key_moves: List[str],
        previous_outputs: Dict[str, str] = {}
    ) -> str:
        """Get the prompt for the framework integration phase."""
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

        prompt = f"""You are developing a detailed outline for a philosophy paper. This is the FRAMEWORK INTEGRATION phase.

TASK: Create a comprehensive outline that integrates the abstract framework into a logical structure.

REQUIREMENTS:
- Establish logical section/subsection structure
- Map key moves to specific sections  
- Allocate word counts per section (target: 8,000-10,000 words)
- Create logical flow from introduction to conclusion
- Include intro, main arguments, objections/responses, conclusion

INPUT DATA:
ABSTRACT: {abstract}

MAIN THESIS: {main_thesis}

FRAMEWORK KEY MOVES:
{framework_key_moves_text}

DEVELOPED KEY MOVES:
{developed_key_moves_text}{previous_outputs_section}

OUTPUT: Present outline in Markdown with clear headings, word counts, and key move mappings."""
        
        return prompt
    
    def get_literature_mapping_prompt(
        self, 
        framework: Dict[str, Any], 
        developed_key_moves: List[str],
        literature: Dict[str, Any] = {},
        previous_outputs: Dict[str, str] = {}
    ) -> str:
        """Get the prompt for the literature mapping phase."""
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

        prompt = f"""You are mapping literature to the paper outline. This is the LITERATURE MAPPING phase.

TASK: Map literature sources to specific sections of the outline.

REQUIREMENTS:
- Identify which sources support each section
- Map key arguments and evidence to outline structure
- Ensure literature integration supports key moves
- Balance depth of engagement with scope

INPUT DATA:
ABSTRACT: {abstract}

MAIN THESIS: {main_thesis}

FRAMEWORK INTEGRATION OUTPUT:
{framework_integration}

LITERATURE:
{literature_text}

DEVELOPED KEY MOVES:
{developed_key_moves_text}{previous_outputs_section}

OUTPUT: Present literature mapping showing which sources engage with each section."""
        
        return prompt
    
    def get_content_development_prompt(
        self, 
        framework: Dict[str, Any], 
        developed_key_moves: List[str],
        literature: Dict[str, Any] = {},
        previous_outputs: Dict[str, str] = {}
    ) -> str:
        """Get the prompt for the content development phase."""
        abstract = framework.get("abstract", "")
        main_thesis = framework.get("main_thesis", "")
        
        # Get the previous phase outputs if available
        framework_integration = ""
        literature_mapping = ""
        if "framework_integration" in previous_outputs:
            framework_integration = previous_outputs["framework_integration"]
        if "literature_mapping" in previous_outputs:
            literature_mapping = previous_outputs["literature_mapping"]
        
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

        prompt = f"""You are developing detailed content for the paper outline. This is the CONTENT DEVELOPMENT phase.

TASK: Develop specific content guidance for each section of the outline.

REQUIREMENTS:
- Provide detailed content directions for each section
- Include argument structures and key claims
- Map evidence and examples to sections
- Ensure content supports key moves
- Balance theoretical and practical elements

INPUT DATA:
ABSTRACT: {abstract}

MAIN THESIS: {main_thesis}

FRAMEWORK INTEGRATION OUTPUT:
{framework_integration}

LITERATURE MAPPING OUTPUT:
{literature_mapping}

DEVELOPED KEY MOVES:
{developed_key_moves_text}{previous_outputs_section}

OUTPUT: Present detailed content guidance for each section."""
        
        return prompt
    
    def get_structural_validation_prompt(
        self, 
        framework: Dict[str, Any], 
        developed_key_moves: List[str],
        literature: Dict[str, Any] = {},
        previous_outputs: Dict[str, str] = {}
    ) -> str:
        """Get the prompt for the structural validation phase."""
        abstract = framework.get("abstract", "")
        main_thesis = framework.get("main_thesis", "")
        
        # Get the previous phase outputs if available
        framework_integration = ""
        literature_mapping = ""
        content_development = ""
        if "framework_integration" in previous_outputs:
            framework_integration = previous_outputs["framework_integration"]
        if "literature_mapping" in previous_outputs:
            literature_mapping = previous_outputs["literature_mapping"]
        if "content_development" in previous_outputs:
            content_development = previous_outputs["content_development"]
        
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

        prompt = f"""You are validating the coherence and flow of the paper structure. This is the STRUCTURAL VALIDATION phase.

TASK: Review the complete outline for logical coherence and structural integrity.

REQUIREMENTS:
- Validate logical flow between sections
- Check that all key moves are addressed
- Ensure transitions are smooth and logical
- Verify word count distribution is appropriate
- Identify any structural gaps or redundancies

INPUT DATA:
ABSTRACT: {abstract}

MAIN THESIS: {main_thesis}

FRAMEWORK INTEGRATION OUTPUT:
{framework_integration}

LITERATURE MAPPING OUTPUT:
{literature_mapping}

CONTENT DEVELOPMENT OUTPUT:
{content_development}

DEVELOPED KEY MOVES:
{developed_key_moves_text}{previous_outputs_section}

OUTPUT: Present structural validation with recommendations for improvements."""
        
        return prompt
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for the worker."""
        return self.system_prompt 