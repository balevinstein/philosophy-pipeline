import json
from typing import Dict, Any

from src.phases.core.base_worker import WorkerInput, WorkerOutput
from src.phases.core.worker_types import RefinementWorker
from src.phases.phase_three.stages.stage_one.prompts.section_writing.section_writing_prompts import (
    SectionWritingPrompts,
)


class SectionRefinementWorker(RefinementWorker):
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.prompts = SectionWritingPrompts()
        self._state = {"iterations": 0, "refinement_history": []}
        self.stage_name = "section_refinement"

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        return self.construct_refinement_prompt(
            writing_context=input_data.context["writing_context"],
            section_index=input_data.parameters["section_index"],
            current_content=input_data.context["current_section_content"],
            critique=input_data.context["current_critique"],
            paper_overview=input_data.context["paper_overview"]
        )

    def construct_refinement_prompt(self, writing_context: Dict[str, Any], section_index: int,
                                  current_content: str, critique: str, paper_overview: Dict[str, Any]) -> str:
        """Generate prompt for refining a section based on critique"""
        
        section = writing_context["sections"][section_index]
        content_bank = writing_context["content_bank"]
        
        # Create section context
        previous_sections = []
        upcoming_sections = []
        
        for i, s in enumerate(writing_context["sections"]):
            if i < section_index:
                previous_sections.append(f"{i+1}. {s['section_name']}")
            elif i > section_index:
                upcoming_sections.append(f"{i+1}. {s['section_name']}")
        
        previous_context = "\n".join(previous_sections) if previous_sections else "None (this is the first section)"
        upcoming_context = "\n".join(upcoming_sections) if upcoming_sections else "None (this is the final section)"
        
        return f"""
You are refining a philosophy paper section based on detailed critic feedback. Your task is to improve the section while maintaining its core function and advancing the paper's thesis.

PAPER OVERVIEW:
Thesis: {paper_overview['thesis']}
Target Length: {paper_overview['target_words']} words total

SECTION TO REFINE:
Section {section_index + 1}: {section['section_name']}
Target Words: {section['word_target']}
Expected Content: {section['content_guidance']}

STRUCTURAL CONTEXT:
Previous Sections:
{previous_context}

Upcoming Sections:
{upcoming_context}

CURRENT SECTION CONTENT:
{current_content}

CRITIC FEEDBACK:
{critique}

CONTENT BANK AVAILABLE:
Arguments Ready for Use:
{json.dumps(content_bank['arguments'], indent=2)}

Examples Available:
{json.dumps(content_bank['examples'], indent=2)}

Citations Identified:
{json.dumps(content_bank['citations'], indent=2)}

REFINEMENT GUIDELINES:

1. ADDRESS CRITIC FEEDBACK
   - Directly respond to major issues identified by the critic
   - Improve minor issues where possible
   - Maintain positive elements that work well

2. MAINTAIN SECTION PURPOSE
   - Keep the section's role in advancing the main thesis
   - Preserve essential arguments and contributions
   - Ensure target word count is appropriate

3. IMPROVE INTEGRATION
   - Strengthen transitions to/from other sections
   - Enhance internal paragraph flow
   - Clarify the section's place in overall argument

4. ENHANCE PHILOSOPHICAL RIGOR
   - Strengthen argument structure and support
   - Improve conceptual clarity and precision
   - Add or improve citations as needed

OUTPUT REQUIREMENTS:
1. Response must be valid JSON with properly escaped strings
2. Use \\n for line breaks within strings 
3. Keep all text fields clear and well-formed
4. Include detailed notes about changes made

OUTPUT FORMAT:
{{
    "refined_section_content": "The complete refined section with all improvements",
    "word_count": actual_word_count_number,
    "changes_made": [
        "List of specific changes made in response to critique"
    ],
    "content_bank_usage": [
        "List of arguments/examples used from content bank"
    ],
    "refinement_notes": "Brief explanation of refinement approach and key improvements",
    "transition_points": {{
        "opening_connection": "How this refined section connects to previous content",
        "closing_transition": "How this refined section leads to the next section"
    }},
    "critic_response": {{
        "major_issues_addressed": [
            "How each major issue from critique was addressed"
        ],
        "minor_improvements": [
            "Minor refinements made based on feedback"
        ],
        "remaining_considerations": "Any critique points that couldn't be fully addressed and why"
    }}
}}

Focus on creating a substantially improved section that directly addresses the critic's feedback while maintaining philosophical rigor and clear integration with the overall paper structure.
"""

    def process_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Prepare input for section refinement"""
        if "current_section_content" not in state or "current_critique" not in state:
            raise ValueError("Missing required state: current_section_content and current_critique")
        
        section_index = state.get("section_index", 0)
        
        return WorkerInput(
            context={
                "writing_context": state["writing_context"],
                "current_section_content": state["current_section_content"],
                "current_critique": state["current_critique"],
                "paper_overview": state["writing_context"]["paper_overview"],
            },
            parameters={
                "section_index": section_index,
                "stage": "section_refinement",
                "iteration": self._state["iterations"],
            },
        )

    def process_output(self, response: str) -> WorkerOutput:
        """Process refinement response into structured output"""
        try:
            # Parse JSON response - handle escaping properly
            response_clean = response.replace("```json", "").replace("```", "").strip()
            refinement_data = json.loads(response_clean)
            
            # Update state
            self._state["iterations"] += 1
            self._state["refinement_history"].append({
                "refined_content": refinement_data.get("refined_section_content", ""),
                "changes_made": refinement_data.get("changes_made", []),
                "iteration": self._state["iterations"]
            })

            return WorkerOutput(
                modifications=refinement_data,
                notes={
                    "changes_count": len(refinement_data.get("changes_made", [])),
                    "word_count": refinement_data.get("word_count", 0),
                    "major_issues_addressed": len(refinement_data.get("critic_response", {}).get("major_issues_addressed", [])),
                    "iteration": self._state["iterations"],
                },
                status="completed",
            )

        except json.JSONDecodeError as e:
            print(f"\nJSON parsing failed in refinement. Error: {str(e)}")
            print(f"Response length: {len(response)}")
            print(f"First 200 chars: {response[:200]}")
            print(f"Last 200 chars: {response[-200:]}")
            
            return WorkerOutput(
                modifications={},
                notes={"error": f"Failed to parse refinement response: {str(e)}"},
                status="failed",
            )
        except Exception as e:
            return WorkerOutput(
                modifications={},
                notes={"error": f"Failed to process refinement response: {str(e)}"},
                status="failed",
            )

    def validate_output(self, output: WorkerOutput) -> bool:
        """Verify output meets requirements"""
        print("\nValidating section refinement...")

        if not output.modifications:
            print("Failed: No modifications returned")
            return False

        required_fields = {
            "refined_section_content",
            "word_count",
            "changes_made", 
            "content_bank_usage",
            "refinement_notes",
            "transition_points",
            "critic_response",
        }

        missing_fields = required_fields - set(output.modifications.keys())
        if missing_fields:
            print(f"Failed: Missing required fields: {missing_fields}")
            return False

        # Validate refined content exists and is substantial
        refined_content = output.modifications.get("refined_section_content", "")
        if not refined_content or len(refined_content.strip()) < 100:
            print("Failed: Refined content too short or missing")
            return False

        # Check word count
        word_count = output.modifications.get("word_count", 0)
        actual_word_count = len(refined_content.split())
        
        print(f"\nRefined section word count: {word_count} (reported) vs {actual_word_count} (actual)")
        
        # Allow some flexibility in word count reporting
        if abs(word_count - actual_word_count) > 50:
            print("Warning: Reported word count differs significantly from actual")

        # Validate changes were made
        changes_made = output.modifications.get("changes_made", [])
        if not changes_made:
            print("Warning: No changes reported - refinement may not have occurred")

        # Validate critic response structure
        critic_response = output.modifications.get("critic_response", {})
        if not isinstance(critic_response, dict):
            print("Failed: critic_response must be a dictionary")
            return False

        # Validate transition points structure
        transition_points = output.modifications.get("transition_points", {})
        if not isinstance(transition_points, dict):
            print("Failed: transition_points must be a dictionary")
            return False

        # Print summary for inspection
        print(f"\nRefinement Summary:")
        print(f"Content length: {len(refined_content)} characters")
        print(f"Word count: {actual_word_count} words")
        print(f"Changes made: {len(changes_made)} items")
        print(f"Content bank usage: {len(output.modifications.get('content_bank_usage', []))} items")
        
        print("Refinement validation passed!")
        return True 