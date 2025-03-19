from typing import Dict, Any, Optional, List


class LiteratureMappingPrompt:
    """Prompts for the literature mapping phase of detailed outline development."""

    def get_prompt(
        self,
        framework: Dict[str, Any],
        initial_outline: Dict[str, Any],
        current_outline: Any,
        developed_key_moves: List[Dict[str, Any]],
        literature: Dict[str, Any],
    ) -> str:
        """
        Construct prompt for the literature mapping phase.
        
        This focuses on identifying which literature should be used in each section
        and how each source should be engaged.
        """
        # Get the main thesis and contribution from the framework
        main_thesis = framework.get("main_thesis", "")
        core_contribution = framework.get("core_contribution", "")
        
        # Get the initial outline sections
        initial_outline_content = initial_outline.get("outline", "")
        
        # Get the current outline development (from framework integration phase)
        current_outline_content = ""
        if current_outline:
            if isinstance(current_outline, str):
                current_outline_content = current_outline
            elif isinstance(current_outline, dict) and "core_content" in current_outline:
                current_outline_content = current_outline["core_content"]
        
        # Format literature information
        literature_content = ""
        if literature:
            if "summaries" in literature:
                for i, (source, summary) in enumerate(literature["summaries"].items()):
                    literature_content += f"\n\n### Source {i+1}: {source}\n{summary}"
            else:
                literature_content = str(literature)
        
        # Prepare key moves content for inclusion in prompt
        key_moves_content = ""
        for i, move in enumerate(developed_key_moves):
            move_text = move.get("key_move_text", "")
            literature_section = move.get("literature", "")
            if move_text and literature_section:
                key_moves_content += f"\n\n## Key Move {i+1}: {move_text}\nLiterature: {literature_section[:500]}...\n(content continues)"
            elif move_text:
                key_moves_content += f"\n\n## Key Move {i+1}: {move_text}\n(No literature content available)"
        
        prompt = f"""# Literature Mapping Phase

## Phase II.4 Context
You are participating in Phase II.4 (Detailed Outline Development) of an AI-driven philosophy paper generation process, specifically working on the Literature Mapping phase. Your task is to identify which literature should be used in each section of the outline and how it should be engaged.

## Task Description
Using the outline structure from the framework integration phase, map the literature from phase II.1 and the literature used in key moves to each section of the outline. For each section, specify which sources should be engaged and how they should be used (supporting, contrasting, extending, etc.).

## Requirements
1. Identify which pieces of literature should be engaged in each section
2. Specify how each source should be used (supporting, contrasting, extending, etc.)
3. Ensure comprehensive coverage of the literature identified in phase II.1
4. Identify any gaps in literature coverage that might need addressing
5. Prioritize literature engagement (primary vs supporting sources) for each section

## Expected Output Format
Your output should be organized by the outline sections with:
- Clear identification of which literature goes where
- Bullet points specifying how each source should be engaged
- Priority levels for sources within each section
- Brief notes on why each source is relevant to the section

## Outline Structure (from Framework Integration Phase):
{current_outline_content if current_outline_content else "No outline structure available. Please use the initial outline."}

## Initial Outline (from Phase II.2):
{initial_outline_content}

## Paper Framework Information

### Main Thesis:
{main_thesis}

### Core Contribution:
{core_contribution}

### Key Moves and Their Literature:
{key_moves_content}

## Literature Information:
{literature_content}

## Guidelines
- Focus on creating clear mappings between sections and relevant literature
- Specify exactly how each source should be engaged in each section
- Consider the argumentative purpose of each section when mapping literature
- Ensure that crucial sources are properly highlighted
- Use a structured bullet-point format for clarity
- Indicate where literature is being used to support arguments vs. where it's being critiqued
- Identify any potential gaps in literature coverage that should be addressed

## Important Note
Your literature mapping will guide content development and help ensure that philosophical arguments are properly supported by scholarly engagement. Be specific and thorough in your mappings.

Now, create a comprehensive literature mapping for the philosophical paper outline."""
        
        return prompt 