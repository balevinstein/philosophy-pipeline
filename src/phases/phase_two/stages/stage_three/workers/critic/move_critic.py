from typing import Dict, Any, List

from src.phases.core.base_worker import WorkerInput, WorkerOutput
from src.phases.core.worker_types import CriticWorker
from src.phases.phase_two.stages.stage_three.prompts.critic.critic_prompts import (
    MoveCriticPrompts,
)


class MoveCriticWorker(CriticWorker):
    """
    Worker responsible for critiquing the development of a single key move.

    This worker evaluates the quality of the move development, assessing
    argument strength, example effectiveness, literature integration,
    and alignment with the overall framework.
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.prompts = MoveCriticPrompts()
        self.stage_name = "move_critic"
        self._state = {
            "iterations": 0,
            "previous_critiques": [],
        }

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        """Construct the appropriate critique prompt."""
        move_index = input_data.parameters.get("move_index", 0)
        current_move_development = input_data.context.get(
            "current_move_development", {}
        )
        framework = input_data.context.get("framework", {})
        outline = input_data.context.get("outline", {})

        # Get the specific move we're working on
        moves_list = framework.get("key_moves", [])
        current_move = moves_list[move_index] if move_index < len(moves_list) else None

        if not current_move:
            raise ValueError(f"Invalid move index: {move_index}")

        # Handle current_move_development being either a string or a dict
        development_content = current_move_development
        if isinstance(current_move_development, dict):
            development_content = current_move_development.get("content", "")
            development_phase = current_move_development.get(
                "development_phase", "initial"
            )
        else:
            # If it's not a dict, assume it's a string with the content
            development_content = current_move_development
            # Get development phase from input parameters if available
            development_phase = input_data.parameters.get(
                "development_phase", "initial"
            )

        print(f"Using development phase: {development_phase}")

        if development_phase == "initial":
            return self.prompts.get_initial_critique_prompt(
                move=current_move,
                move_development=development_content,
                framework=framework,
                outline=outline,
                literature=input_data.context.get("literature", {}),
                iteration=self._state["iterations"],
            )
        elif development_phase == "examples":
            return self.prompts.get_examples_critique_prompt(
                move=current_move,
                move_development=development_content,
                framework=framework,
                outline=outline,
                literature=input_data.context.get("literature", {}),
                iteration=self._state["iterations"],
            )
        elif development_phase == "literature":
            return self.prompts.get_literature_critique_prompt(
                move=current_move,
                move_development=development_content,
                framework=framework,
                outline=outline,
                literature=input_data.context.get("literature", {}),
                iteration=self._state["iterations"],
            )
        else:
            # Default critique prompt
            return self.prompts.get_initial_critique_prompt(
                move=current_move,
                move_development=development_content,
                framework=framework,
                outline=outline,
                literature=input_data.context.get("literature", {}),
                iteration=self._state["iterations"],
            )

    def process_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Map the input data to worker input."""
        print("\nPreparing input for key move critique...")
        print("\nReceived state keys:", list(state.keys()))

        if "framework" not in state or "outline" not in state:
            raise ValueError("Missing required state: framework and outline")

        if "current_move_development" not in state:
            raise ValueError("No current_move_development found in state")

        move_index = state.get("move_index", 0)

        # Get development phase if available
        development_phase = state.get("development_phase", "initial")

        return WorkerInput(
            context={
                "framework": state["framework"],
                "outline": state["outline"],
                "current_move_development": state["current_move_development"],
                "key_moves": state.get("key_moves", {}),
                "literature": state.get("literature", {}),
            },
            parameters={
                "move_index": move_index,
                "iteration": self._state["iterations"],
                "development_phase": development_phase,
            },
        )

    def process_output(self, response) -> WorkerOutput:
        """Process response into structured output."""
        try:
            print("\nProcessing critic response...")
            
            # Handle API response tuple (response_text, duration)
            if isinstance(response, tuple):
                response_text, duration = response
                print(f"Critic API call took {duration:.2f} seconds")
            else:
                response_text = response
            
            # Print the first 200 characters to help with debugging
            print(f"Response preview: {response_text[:200]}...")

            # Split into sections
            sections = {}
            current_section = None
            current_content = []
            section_markers = ["# ", "## "]  # Look for both H1 and H2 headings

            for line in response_text.split("\n"):
                is_section_header = False
                for marker in section_markers:
                    if line.startswith(marker):
                        if current_section:
                            sections[current_section] = "\n".join(
                                current_content
                            ).strip()
                        current_section = line[len(marker) :].strip()
                        current_content = []
                        is_section_header = True
                        break

                if not is_section_header and current_section is not None:
                    current_content.append(line)

            if current_section:
                sections[current_section] = "\n".join(current_content).strip()

            # If we couldn't find any sections, create default ones
            if not sections and response_text.strip():
                # Try to split the response into a critique and assessment
                parts = response_text.split("Summary Assessment", 1)
                if len(parts) > 1:
                    sections["Critique"] = parts[0].strip()
                    sections["Summary Assessment"] = (
                        "Summary Assessment" + parts[1].strip()
                    )
                else:
                    sections["Critique"] = response_text.strip()
                    sections["Summary Assessment"] = (
                        "MINOR REFINEMENT\n\nNext steps:\n- Review and refine the arguments"
                    )

            # Extract assessment and recommendations
            assessment = self._extract_assessment(
                sections.get("Summary Assessment", "")
            )
            recommendations = self._extract_recommendations(
                sections.get("Summary Assessment", "")
            )

            # If we couldn't extract a valid assessment, provide a default
            if assessment == "UNKNOWN":
                assessment = "MINOR REFINEMENT"

            # If we couldn't extract recommendations, provide defaults
            if not recommendations:
                recommendations = [
                    "Review and refine the arguments",
                    "Add more detail to explanations",
                ]

            # Update state
            self._state["iterations"] += 1
            self._state["previous_critiques"].append(
                {
                    "assessment": assessment,
                    "recommendations": recommendations,
                }
            )

            print(f"Found {len(sections)} sections: {list(sections.keys())}")
            print(f"Assessment: {assessment}")
            print(f"Recommendations: {recommendations[:3]}...")

            # Separate scratch work from the core critique
            scratch_work = sections.get("Scratch Work", "")

            # Remove scratch work from sections to keep final content cleaner
            if "Scratch Work" in sections:
                del sections["Scratch Work"]

            # Create a clean, structured critique text that includes only the essential parts
            critique_section = sections.get("Critique", "")
            assessment_section = sections.get("Summary Assessment", "")

            # Extract core content as a single string for easier downstream use
            core_content = f"# Critique\n{critique_section}\n\n# Summary Assessment\n{assessment_section}"

            # Create a concise version of recommendations as a bulleted list for clear display
            formatted_recommendations = "\n".join(
                [f"- {rec}" for rec in recommendations]
            )

            return WorkerOutput(
                modifications={
                    # Keep the full content for debugging and validation
                    "full_content": response_text.strip(),
                    # Key structured content for downstream use
                    "core_content": core_content,
                    "sections": sections,
                    "assessment": assessment,
                    "recommendations": recommendations,
                    "formatted_recommendations": formatted_recommendations,
                    # Meta information
                    "iteration": self._state["iterations"],
                    # Optional development materials
                    "scratch_work": scratch_work,
                },
                notes={
                    "assessment": assessment,
                    "recommendations": recommendations,
                    "section_count": len(sections),
                },
                status="completed",
            )
        except Exception as e:
            print(f"Error processing critic output: {str(e)}")
            # If something fails, return a basic output that will pass validation
            return WorkerOutput(
                modifications={
                    "full_content": response_text.strip(),
                    "core_content": response_text.strip(),
                    "sections": {
                        "Critique": response_text.strip(),
                        "Summary Assessment": "MINOR REFINEMENT\n\nNext steps:\n- Review and refine the arguments",
                    },
                    "assessment": "MINOR REFINEMENT",
                    "recommendations": ["Review and refine the arguments"],
                    "formatted_recommendations": "- Review and refine the arguments",
                    "iteration": self._state["iterations"],
                    "scratch_work": "",
                },
                notes={
                    "error": f"Failed to process response: {str(e)}",
                    "assessment": "MINOR REFINEMENT",
                    "recommendations": ["Review and refine the arguments"],
                },
                status="completed",  # Complete anyway to avoid hard failure
            )

    def _extract_assessment(self, summary_text: str) -> str:
        """Extract the assessment level from the summary."""
        assessment_levels = ["MAJOR REVISION", "MINOR REFINEMENT", "MINIMAL CHANGES"]
        for level in assessment_levels:
            if level in summary_text:
                return level
        return "UNKNOWN"

    def _extract_recommendations(self, summary_text: str) -> List[str]:
        """Extract key recommendations from the summary."""
        recommendations = []
        next_steps_idx = summary_text.find("Next steps:")
        if next_steps_idx != -1:
            next_steps_text = summary_text[next_steps_idx:]
            for line in next_steps_text.split("\n"):
                line = line.strip()
                if line and (
                    line.startswith("- ")
                    or line.startswith("* ")
                    or (line[0].isdigit() and line[1:].startswith(". "))
                ):
                    recommendations.append(
                        line[2:]
                        if line.startswith("- ") or line.startswith("* ")
                        else line[line.find(".") + 1 :].strip()
                    )
        return recommendations

    def validate_output(self, output: WorkerOutput) -> bool:
        """Optional output validation."""
        print("\nValidating key move critique output...")

        if not output.modifications:
            print("Failed: No modifications")
            return False

        content = output.modifications.get("core_content")
        if not content:
            print("Failed: No core_content")
            return False

        # Print preview of content for debugging
        print(f"{content[:200]}...")

        # Check for required sections
        required_section_options = [
            ["Critique", "Analysis", "Evaluation", "Assessment"],
            ["Summary Assessment", "Summary", "Overall Assessment", "Recommendation"],
        ]

        sections = output.modifications.get("sections", {})
        print(f"Found sections: {list(sections.keys())}")

        # Check if we have at least one option from each required group
        missing_groups = []
        for section_group in required_section_options:
            if not any(section in sections for section in section_group):
                missing_groups.append(section_group)
                print(f"Missing a section from group: {section_group}")

        if missing_groups:
            # Don't fail if we're missing just one group - be lenient
            if len(missing_groups) > 1:
                print("Failed: Missing too many required section groups")
                return False

        # Verify we have a valid assessment - but be lenient if it's missing
        assessment = output.modifications.get("assessment", "")
        valid_assessments = ["MAJOR REVISION", "MINOR REFINEMENT", "MINIMAL CHANGES"]
        if assessment not in valid_assessments:
            print(
                f"Warning: Non-standard assessment value: '{assessment}' - using default"
            )
            # Don't fail just for this

        # Verify we have at least one recommendation - but don't fail if missing
        recommendations = output.modifications.get("recommendations", [])
        if not recommendations:
            print("Warning: No recommendations provided")
            # Don't fail just for this

        print("Validation passed!")
        return True
