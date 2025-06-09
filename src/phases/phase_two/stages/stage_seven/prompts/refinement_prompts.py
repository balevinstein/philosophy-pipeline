import json
from typing import Dict, Any, List
from src.utils.prompt_utils import load_and_combine_style_guides


class RefinementPrompts:
    """Prompts for the refinement worker in Phase II.7"""
    
    def __init__(self):
        style_guide = load_and_combine_style_guides()
        self.system_prompt = f"""{style_guide}

You are a master philosophical editor specializing in targeted refinement. Your role is to take flawed philosophical moves and transform them into sophisticated arguments that meet Analysis journal standards. You excel at:
- Addressing specific referee critiques while preserving what works
- Eliminating hedging and philosophical cowardice
- Creating intellectually bold arguments that take clear positions
- Ensuring philosophical moves have genuine bite and sophistication

You are direct, intellectually honest, and willing to make controversial claims when warranted by the argument."""

    def get_redevelopment_prompt(
        self,
        original_move: Dict[str, Any],
        planned_move: Dict[str, Any],
        revised_thesis: str,
        revised_contribution: str,
        relevant_critique: List[Dict[str, Any]],
        move_examples: Dict[str, Any]
    ) -> str:
        """Construct prompt for redeveloping a flagged move"""
        
        return f"""<task>
You must completely redevelop this philosophical move to address the referee's critique while supporting the revised thesis. The redeveloped move should be intellectually sophisticated, take clear positions, and meet the quality standards of Analysis journal.
</task>

<revised_thesis>
{revised_thesis}
</revised_thesis>

<revised_contribution>
{revised_contribution}
</revised_contribution>

<original_move>
Move Index: {original_move.get('key_move_index', 'Unknown')}
Original Description: {original_move.get('key_move_text', '')}
Original Content: {original_move.get('final_content', '')}
</original_move>

<revision_guidance>
Status: {planned_move.get('status', '')}
Revised Description: {planned_move.get('revised_description', '')}
Justification: {planned_move.get('justification', '')}
</revision_guidance>

<referee_critique>
{self._format_critique(relevant_critique)}
</referee_critique>

<philosophical_move_examples>
These examples from published Analysis papers demonstrate the level of sophistication required:

{json.dumps(move_examples, indent=2)}

Your redeveloped move should match this quality level.
</philosophical_move_examples>

<quality_requirements>
Your redevelopment must:

1. **Address the Critique Directly**
   - Fix each specific issue raised by the referee
   - Show how the revised argument avoids the identified problems
   - Demonstrate philosophical sophistication in the response

2. **Support the Revised Thesis**
   - Ensure the move clearly advances the revised thesis
   - Maintain coherence with the dual-dimension framework
   - Avoid contradicting other retained moves

3. **Pass Quality Tests**
   - EXTREME CASE TEST: Does the argument hold up under edge cases?
   - COUNTEREXAMPLE RESISTANCE: Can it withstand obvious counterexamples?
   - HIDDEN ASSUMPTIONS: Are all crucial premises explicit?
   - PHILOSOPHICAL BITE: Does it make a substantive, interesting claim?

4. **Avoid Anti-Patterns**
   - NO HEDGING: Take clear positions without excessive qualification
   - NO SURVEY MODE: Advance original arguments, not just review literature
   - NO FALSE BALANCE: Don't give undue weight to weak objections
   - DRAW IMPLICATIONS: Follow arguments to their controversial conclusions

5. **Follow Analysis Style**
   - Use concrete examples to drive philosophical points
   - Maintain conversational directness
   - Ensure every sentence advances the argument
   - Create elegant argumentative turns
</quality_requirements>

<redevelopment_instructions>
1. First, identify exactly what philosophical work this move needs to do
2. Address each critique point systematically
3. Rebuild the argument from the ground up if necessary
4. Ensure the move has genuine philosophical sophistication
5. Make it memorable and intellectually compelling
</redevelopment_instructions>

<output_format>
{{
    "refined_content": "The complete redeveloped philosophical move content. This should be publication-ready prose that could be inserted directly into an Analysis paper. No meta-commentary about changes.",
    "refinement_notes": "Brief explanation of how you addressed the key critiques and improved the philosophical sophistication.",
    "addressed_issues": [
        "List of specific issues from the referee critique that were addressed"
    ],
    "quality_checks": {{
        "extreme_case_tested": true/false,
        "counterexample_resistant": true/false,
        "assumptions_explicit": true/false,
        "takes_clear_position": true/false,
        "philosophically_sophisticated": true/false
    }}
}}
</output_format>"""

    def _format_critique(self, critique_list: List[Dict[str, Any]]) -> str:
        """Format the critique list for the prompt"""
        if not critique_list:
            return "No specific critique for this move was found in the referee report."
            
        formatted = []
        for critique in critique_list:
            critique_type = critique.get("type", "Unknown")
            issue = critique.get("issue", {})
            
            if critique_type == "coherence_issue":
                formatted.append(f"COHERENCE ISSUE: {issue.get('description', '')}")
            elif critique_type == "argumentative_weakness":
                formatted.append(f"ARGUMENTATIVE WEAKNESS ({issue.get('weakness_type', '')}): {issue.get('description', '')}")
            elif critique_type == "hajek_failure":
                formatted.append(f"HÁJEK TEST FAILURE ({issue.get('test_failed', '')}): {issue.get('description', '')} [Severity: {issue.get('severity', '')}]")
            elif critique_type == "anti_rlhf_violation":
                formatted.append(f"ANTI-RLHF VIOLATION ({issue.get('pattern', '')}): {issue.get('description', '')} Fix required: {issue.get('fix_required', '')}")
                
        return "\n".join(formatted)

    def get_system_prompt(self) -> str:
        """Return the system prompt for API calls"""
        return self.system_prompt 