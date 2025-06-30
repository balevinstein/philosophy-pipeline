from typing import Dict, Any, Optional, List


class FrameworkIntegrationPrompt:
    """Prompts for the framework integration phase of detailed outline development."""

    def get_prompt(
        self,
        framework: Dict[str, Any],
        initial_outline: Dict[str, Any],
        developed_key_moves: List[Dict[str, Any]],
        literature: Dict[str, Any],
    ) -> str:
        """
        Construct prompt for the framework integration phase.
        
        This focuses on creating a logical section/subsection structure that properly
        accommodates all key moves with explicit mapping and word count allocations.
        """
        # Get the main thesis and contribution from the framework
        main_thesis = framework.get("main_thesis", "")
        core_contribution = framework.get("core_contribution", "")
        
        # Get the initial outline sections
        initial_outline_content = initial_outline.get("outline", "")
        
        # Prepare key moves content for inclusion in prompt
        key_moves_content = ""
        for i, move in enumerate(developed_key_moves):
            move_text = move.get("key_move_text", "")
            move_content = move.get("final_content", "")
            if move_text and move_content:
                key_moves_content += f"\n\n## Key Move {i+1}: {move_text}\n{move_content[:500]}...\n(content continues)"
            elif move_text:
                key_moves_content += f"\n\n## Key Move {i+1}: {move_text}\n(No developed content available)"
        
        prompt = f"""# Framework Integration Phase

## Phase II.4 Context
You are participating in Phase II.4 (Detailed Outline Development) of an AI-driven philosophy paper generation process, specifically working on the Framework Integration phase. Your task is to create the foundational structure for a philosophical paper that properly supports the paper's thesis and accommodates all key argumentative moves.

## Task Description
Analyze the abstract framework and key moves provided below to create a logical section/subsection structure that will serve as the skeleton for the full paper. Your output should clearly show which sections develop which key moves and provide a logical progression from introduction through conclusion.

## Requirements
1. Create a section/subsection structure that accommodates all key moves
2. Explicitly map each key move to specific sections where they will be developed
3. Provide word count allocations that ensure appropriate development of each component
4. Ensure the structure supports the main thesis

## THESIS ADHERENCE (Anti-Drift)
Your structural decisions must support this thesis: "{main_thesis}"
- Organize sections to build toward and support the thesis
- Ensure the structure enables the thesis to be convincingly defended
- Do NOT create structures that would undermine or contradict the thesis
- The flow should make the thesis appear well-supported and logical

## Expected Output Format
Your output should be a structured outline with:
- Numbered sections (1, 2, 3, etc.) and subsections (1.1, 1.2, etc.)
- Word count allocations for each major section
- Explicit mapping showing which key move(s) each section develops
- Brief descriptions (1-2 sentences) of what each section will contain
- A logical flow from introduction through conclusion

## Paper Framework Information

### Main Thesis:
{main_thesis}

### Core Contribution:
{core_contribution}

### Key Moves:
{key_moves_content}

### Initial Outline (from Phase II.2):
{initial_outline_content}

## Guidelines
- The introduction section should preview all key moves
- Each key move should have sufficient space for proper development
- The conclusion should tie back to the thesis and synthesize the key moves
- The total paper length should be approximately 8,000-10,000 words
- Use your judgment to determine how many subsections each section needs
- Ensure that the outline structure naturally supports the development of arguments
- Consider transitions between sections for logical flow
- Explicitly note which key move(s) are developed in each section

## Important Note
This structure will be used in subsequent phases to guide content development, literature mapping, and the final outline. It must provide a comprehensive foundation that accommodates all key moves while maintaining logical coherence and philosophical rigor.

Now, create the foundational structure for this philosophical paper on forgotten evidence and epistemic justification."""
        
        return prompt 