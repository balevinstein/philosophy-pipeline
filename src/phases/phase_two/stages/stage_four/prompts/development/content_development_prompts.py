from typing import Dict, Any, Optional, List


class ContentDevelopmentPrompt:
    """Prompts for the content development phase of detailed outline development."""

    def get_prompt(
        self,
        framework: Dict[str, Any],
        initial_outline: Dict[str, Any],
        current_outline: Any,
        developed_key_moves: List[Dict[str, Any]],
        literature: Dict[str, Any],
    ) -> str:
        """
        Construct prompt for the content development phase.
        
        This focuses on developing specific content guidance for each section,
        drawing on fully developed key moves to specify arguments, examples, and
        counterarguments in a structured bullet point format.
        """
        # Get the main thesis and contribution from the framework
        main_thesis = framework.get("main_thesis", "")
        core_contribution = framework.get("core_contribution", "")
        
        # Get the initial outline sections
        initial_outline_content = initial_outline.get("outline", "")
        
        # Get the current outline development (from previous phases)
        current_outline_content = ""
        literature_mapping_content = ""
        
        if current_outline:
            if isinstance(current_outline, str):
                current_outline_content = current_outline
            elif isinstance(current_outline, dict):
                if "core_content" in current_outline:
                    current_outline_content = current_outline["core_content"]
                # Check for the literature mapping phase content
                if "literature_mapping" in current_outline:
                    literature_mapping_content = current_outline["literature_mapping"]
        
        # Prepare key moves content for inclusion in prompt
        key_moves_content = ""
        for i, move in enumerate(developed_key_moves):
            move_text = move.get("key_move_text", "")
            final_content = move.get("final_content", "")
            examples = move.get("development", {}).get("examples", "")
            if move_text and final_content:
                key_moves_content += f"\n\n## Key Move {i+1}: {move_text}\nArguments:\n{final_content[:300]}...\n"
                if examples:
                    key_moves_content += f"\nExamples:\n{examples[:300]}...\n"
                key_moves_content += "\n(content continues)"
            elif move_text:
                key_moves_content += f"\n\n## Key Move {i+1}: {move_text}\n(No developed content available)"
        
        prompt = f"""# Content Development Phase

## Phase II.4 Context
You are participating in Phase II.4 (Detailed Outline Development) of an AI-driven philosophy paper generation process, specifically working on the Content Development phase. Your task is to develop specific content guidance for each section of the outline, drawing on the fully developed key moves.

## Task Description
Using the outline structure from the framework integration phase and the literature mapping, develop structured bullet-point content guidance for each section. Specify what arguments should be made, which examples should be used, and how counterarguments should be addressed.

## Requirements
1. Draw on the fully developed key moves to specify what arguments should be made in each section
2. Identify which examples from key moves should be used in each section
3. Specify where and how counterarguments should be addressed
4. Provide clear signposting for the logical flow within each section
5. Ensure all aspects of key moves are properly incorporated

## THESIS ADHERENCE (Anti-Drift)
Your content guidance must support this thesis: "{main_thesis}"
- Frame arguments to build support for the thesis
- Choose examples that strengthen the thesis case
- Address counterarguments in ways that defend the thesis
- Ensure the logical flow leads readers toward accepting the thesis
- Do NOT create guidance that would undermine the thesis argument

## Expected Output Format
For each section, provide structured bullet points with the following categories:

```
Section X.X: [Title] ([Word Count])
Key Move(s): [Which key moves this section develops]

Primary Arguments:
• Argument 1: [Brief description]
• Argument 2: [Brief description]
• Argument 3: [Brief description]

Examples to Include:
• [Example 1 description and source]
• [Example 2 description and source]

Literature Engagement:
• Primary: [Main sources]
• Supporting: [Secondary sources]
• Contrasting: [Sources to critique]

Transition Focus:
• [How this section connects to the next]
```

## Outline Structure:
{current_outline_content if current_outline_content else "No outline structure available. Please use the initial outline."}

## Literature Mapping:
{literature_mapping_content if literature_mapping_content else "No literature mapping available. Please use your judgment to map literature."}

## Paper Framework Information

### Main Thesis:
{main_thesis}

### Core Contribution:
{core_contribution}

### Key Moves with Arguments and Examples:
{key_moves_content}

## Guidelines
- Create structured bullet points rather than paragraphs of prose
- Keep descriptions concise and focused on content guidance
- Be specific about which parts of key moves should be emphasized
- Explicitly note where examples from key moves should be used
- Ensure that arguments flow logically within each section
- Include guidance on how to handle potential counterarguments
- Make the connection between sections explicit in transition notes
- Maintain alignment with the main thesis throughout

## Important Note
Your content guidance will be used in the structural validation phase to create the final detailed outline. It must provide clear direction while allowing flexibility in how the content is expressed in the final paper.

Now, create comprehensive content guidance for each section of the philosophical paper outline."""
        
        return prompt 