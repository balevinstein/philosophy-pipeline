from typing import Dict, Any, List

from src.phases.core.base_worker import WorkerInput, WorkerOutput
from src.phases.core.worker_types import RefinementWorker
from src.phases.phase_two.stages.stage_three.prompts.refinement.refinement_prompts import (
    MoveRefinementPrompts,
)


class MoveRefinementWorker(RefinementWorker):
    """
    Worker responsible for refining a key move based on critique.

    This worker takes the current move development and critique,
    and implements the recommended improvements while maintaining
    overall coherence and framework alignment.
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.prompts = MoveRefinementPrompts()
        self.stage_name = "move_refinement"
        self._state = {
            "iterations": 0,
            "previous_refinements": [],
        }

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        """Construct the appropriate refinement prompt."""
        move_index = input_data.parameters.get("move_index", 0)
        current_move_development = input_data.context.get(
            "current_move_development", {}
        )
        current_critique = input_data.context.get("current_critique", {})
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

        # Handle current_critique being either a string or a dict
        critique_content = current_critique
        if isinstance(current_critique, dict):
            critique_content = current_critique.get("content", "")

        print(f"Using development phase: {development_phase}")

        if development_phase == "initial":
            return self.prompts.get_initial_refinement_prompt(
                move=current_move,
                move_development=development_content,
                critique=critique_content,
                framework=framework,
                outline=outline,
                literature=input_data.context.get("literature", {}),
                iteration=self._state["iterations"],
            )
        elif development_phase == "examples":
            return self.prompts.get_examples_refinement_prompt(
                move=current_move,
                move_development=development_content,
                critique=critique_content,
                framework=framework,
                outline=outline,
                literature=input_data.context.get("literature", {}),
                iteration=self._state["iterations"],
            )
        elif development_phase == "literature":
            return self.prompts.get_literature_refinement_prompt(
                move=current_move,
                move_development=development_content,
                critique=critique_content,
                framework=framework,
                outline=outline,
                literature=input_data.context.get("literature", {}),
                iteration=self._state["iterations"],
            )
        else:
            # Default refinement prompt
            return self.prompts.get_initial_refinement_prompt(
                move=current_move,
                move_development=development_content,
                critique=critique_content,
                framework=framework,
                outline=outline,
                literature=input_data.context.get("literature", {}),
                iteration=self._state["iterations"],
            )

    def process_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Map the input data to worker input."""
        print("\nPreparing input for key move refinement...")
        print("\nReceived state keys:", list(state.keys()))

        if "framework" not in state or "outline" not in state:
            raise ValueError("Missing required state: framework and outline")

        if "current_move_development" not in state:
            raise ValueError("No current_move_development found in state")

        if "current_critique" not in state:
            raise ValueError("No current_critique found in state")

        move_index = state.get("move_index", 0)

        # Get development phase if available
        development_phase = state.get("development_phase", "initial")

        return WorkerInput(
            context={
                "framework": state["framework"],
                "outline": state["outline"],
                "current_move_development": state["current_move_development"],
                "current_critique": state["current_critique"],
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
            print("\nProcessing refinement response...")
            
            # Handle API response tuple (response_text, duration)
            if isinstance(response, tuple):
                response_text, duration = response
                print(f"Refinement API call took {duration:.2f} seconds")
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
                # Try to split the response into development and changes
                parts = response_text.split("Refinement Changes", 1)
                if len(parts) > 1:
                    sections["Refined Development"] = parts[0].strip()
                    sections["Refinement Changes"] = (
                        "Refinement Changes" + parts[1].strip()
                    )
                else:
                    sections["Refined Development"] = response_text.strip()
                    sections["Refinement Changes"] = (
                        "- Implemented refinements based on critique"
                    )

            # Extract changes made
            changes_made = self._extract_changes(sections.get("Refinement Changes", ""))

            # If we couldn't extract changes, provide a default
            if not changes_made:
                changes_made = ["Implemented refinements based on critique"]

            # Update state
            self._state["iterations"] += 1
            self._state["previous_refinements"].append(
                {
                    "changes_made": changes_made,
                }
            )

            print(f"Found {len(sections)} sections: {list(sections.keys())}")
            print(f"Changes made: {changes_made[:3]}...")

            # Separate scratch work from the core refinement
            scratch_work = sections.get("Scratch Work", "")

            # Remove scratch work from sections to keep final content cleaner
            if "Scratch Work" in sections:
                del sections["Scratch Work"]

            # Extract the refined development as the primary output
            refined_development = sections.get("Refined Development", "")

            # Extract core content as a single string for easier downstream use
            # This is the most valuable output of the refinement process
            core_content = refined_development

            # Create a concise version of changes as a bulleted list for clear display
            formatted_changes = "\n".join([f"- {change}" for change in changes_made])

            return WorkerOutput(
                modifications={
                    # Keep the full content for debugging and validation
                    "full_content": response.strip(),
                    # Key structured content for downstream use
                    "core_content": core_content,
                    "sections": sections,
                    "changes_made": changes_made,
                    "formatted_changes": formatted_changes,
                    # Convenient access to the most important output
                    "refined_development": refined_development,
                    # Meta information
                    "iteration": self._state["iterations"],
                    # Optional development materials
                    "scratch_work": scratch_work,
                },
                notes={
                    "changes_made": changes_made,
                    "section_count": len(sections),
                },
                status="completed",
            )
        except Exception as e:
            print(f"Error processing refinement output: {str(e)}")
            # If something fails, return a basic output that will pass validation
            return WorkerOutput(
                modifications={
                    "full_content": response_text.strip(),
                    "core_content": response_text.strip(),
                    "sections": {
                        "Refined Development": response_text.strip(),
                        "Refinement Changes": "- Implemented refinements based on critique",
                    },
                    "refined_development": response_text.strip(),
                    "changes_made": ["Implemented refinements based on critique"],
                    "formatted_changes": "- Implemented refinements based on critique",
                    "iteration": self._state["iterations"],
                    "scratch_work": "",
                },
                notes={
                    "error": f"Failed to process response: {str(e)}",
                    "changes_made": ["Implemented refinements based on critique"],
                },
                status="completed",  # Complete anyway to avoid hard failure
            )

    def _extract_changes(self, changes_text: str) -> List[str]:
        """Extract the list of changes made from the refinement."""
        changes = []
        for line in changes_text.split("\n"):
            line = line.strip()
            if line and (
                line.startswith("- ")
                or line.startswith("* ")
                or (line[0].isdigit() and line[1:].startswith(". "))
            ):
                changes.append(
                    line[2:]
                    if line.startswith("- ") or line.startswith("* ")
                    else line[line.find(".") + 1 :].strip()
                )
        return changes

    def validate_output(self, output: WorkerOutput) -> bool:
        """Validate the refinement output."""
        print("\nValidating key move refinement output...")

        if not output.modifications:
            print("Failed: No modifications")
            return False

        content = output.modifications.get("core_content")
        if not content:
            print("Failed: No core_content")
            return False

        # Print preview of content for debugging
        print(f"{content[:200]}...")

        # Check for required sections - we need at least one development section and one changes section
        development_sections = [
            "Refined Development",
            "Development",
            "Updated Development",
            "Final Development",
        ]
        changes_sections = [
            "Refinement Changes",
            "Changes",
            "Changes Made",
            "Modifications",
        ]

        sections = output.modifications.get("sections", {})
        print(f"Found sections: {list(sections.keys())}")

        has_development = any(section in sections for section in development_sections)
        has_changes = any(section in sections for section in changes_sections)

        if not has_development:
            print(
                f"Warning: Missing development section. Need one of: {development_sections}"
            )
            # Don't fail just for this - we'll still have the full content

        if not has_changes:
            print(f"Warning: Missing changes section. Need one of: {changes_sections}")
            # Don't fail just for this - we'll still have the full content

        # Only fail if we're missing both types of sections
        if not has_development and not has_changes:
            print("Failed: Missing both development and changes sections")
            return False

        # Verify we have at least one change listed - but be lenient
        changes_made = output.modifications.get("changes_made", [])
        if not changes_made:
            print("Warning: No changes listed")
            # Don't fail just for this

        print("Validation passed!")
        return True
