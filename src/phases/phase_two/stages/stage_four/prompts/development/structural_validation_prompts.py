from typing import Dict, Any, Optional, List


class StructuralValidationPrompt:
    """Prompts for the structural validation phase of detailed outline development."""

    def get_prompt(
        self,
        framework: Dict[str, Any],
        initial_outline: Dict[str, Any],
        current_outline: Any,
        developed_key_moves: List[Dict[str, Any]],
        literature: Dict[str, Any],
    ) -> str:
        """
        Construct prompt for the structural validation phase.
        
        This focuses on validating and finalizing the complete outline, analyzing
        logical flow, ensuring key moves are properly sequenced, validating word counts,
        and making necessary adjustments to improve coherence and balance.
        """
        # Get the main thesis and contribution from the framework
        main_thesis = framework.get("main_thesis", "")
        core_contribution = framework.get("core_contribution", "")
        
        # Get the initial outline sections
        initial_outline_content = initial_outline.get("outline", "")
        
        # Get the current outline development (from previous phases)
        framework_integration_content = ""
        literature_mapping_content = ""
        content_development_content = ""
        
        # Extract content from previous phases if available
        if current_outline:
            if isinstance(current_outline, str):
                content_development_content = current_outline
            elif isinstance(current_outline, dict):
                # Try to extract content from different phases
                if "framework_integration" in current_outline:
                    framework_integration_content = current_outline["framework_integration"]
                if "literature_mapping" in current_outline:
                    literature_mapping_content = current_outline["literature_mapping"]
                if "content_development" in current_outline:
                    content_development_content = current_outline["content_development"]
                # If we can't find phase-specific content, try the core content
                if not content_development_content and "core_content" in current_outline:
                    content_development_content = current_outline["core_content"]
        
        # Combine previous phase outputs, prioritizing the most recent
        current_outline_content = content_development_content if content_development_content else \
                               (literature_mapping_content if literature_mapping_content else \
                               (framework_integration_content if framework_integration_content else \
                               "No outline from previous phases available. Please use the initial outline."))
        
        # Prepare key moves content for reference
        key_moves_content = ""
        for i, move in enumerate(developed_key_moves):
            move_text = move.get("key_move_text", "")
            if move_text:
                key_moves_content += f"\n• Key Move {i+1}: {move_text}"
        
        prompt = f"""# Structural Validation Phase

## Phase II.4 Context
You are participating in Phase II.4 (Detailed Outline Development) of an AI-driven philosophy paper generation process, specifically working on the Structural Validation phase. Your task is to validate and finalize the complete outline to ensure it effectively delivers the paper's thesis.

## Task Description
Analyze the outline from previous phases, validate its logical flow and structure, ensure proper development of key moves, and make necessary adjustments to produce a final validated outline that will serve as the foundation for Phase II.5 and ultimately Phase III writing.

## Requirements
1. Analyze the logical flow from section to section
2. Ensure key moves are properly sequenced and developed
3. Validate word count allocations are appropriate for the complexity of each section
4. Confirm that introduction and conclusion effectively frame the paper's contribution
5. Make any necessary adjustments to improve coherence or balance

## Expected Output Format
Your output should be a complete, validated outline including:
- Numbered sections and subsections
- Word count allocations
- Explicit mapping of key moves to sections
- Structured content guidance (using the bullet point format)
- Clear transitions between sections
- Any revisions or adjustments you've made with brief explanations

## Outline from Previous Phases:
{current_outline_content}

## Paper Framework Information

### Main Thesis:
{main_thesis}

### Core Contribution:
{core_contribution}

### Key Moves:
{key_moves_content}

## Guidelines
- Ensure that all key moves are properly accommodated in the outline
- Check that the logical flow between sections is smooth and natural
- Validate that word counts are appropriate for the complexity of each section
- Confirm that the introduction properly sets up the paper and the conclusion effectively synthesizes it
- Make specific adjustments to address any issues you identify
- Maintain the structured bullet point format for content guidance
- Provide brief explanations for any significant changes you make
- Keep the outline comprehensive but focused on the main thesis

## Important Note
Your validated outline will serve as the comprehensive blueprint for Phase III writers. It must provide clear guidance while maintaining cohesion across all sections and key moves. This is the final outline that will guide the paper writing process.

Now, validate and finalize the comprehensive outline for this philosophical paper on forgotten evidence and epistemic justification."""
        
        return prompt 