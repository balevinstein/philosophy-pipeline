import json
from typing import Dict, Any

from src.phases.core.base_worker import WorkerInput, WorkerOutput
from src.phases.core.worker_types import RefinementWorker
from src.phases.phase_two.stages.stage_two.prompts.abstract.abstract_prompts import (
    AbstractPrompts,
)


class AbstractRefinementWorker(RefinementWorker):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.prompts = AbstractPrompts()
        self._state = {"iterations": 0, "refinement_history": []}
        self.stage_name = "abstract_development"

    def _construct_prompt(self, input_data: WorkerInput) -> bool:
        return self.prompts.get_refinement_prompt(
            current_framework=input_data.context["current_framework"],
            critique=input_data.context["current_critique"],
            lit_synthesis=input_data.context.get("lit_synthesis"),
            previous_versions=input_data.context.get("previous_versions"),
        )

    def process_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Prepare input for refinement"""
        if "current_framework" not in state or "current_critique" not in state:
            raise ValueError(
                "Missing required state: current_framework and current_critique"
            )

        return WorkerInput(
            context={
                "current_framework": state["current_framework"],
                "current_critique": state["current_critique"],
                "lit_readings": state.get("literature", {}).get("readings"),
                "lit_synthesis": state.get("literature", {}).get("synthesis"),
                "lit_narrative": state.get("literature", {}).get("narrative"),
                "previous_versions": state.get("previous_versions"),
            },
            parameters={"outline_state": state, "iteration": self._state["iterations"]},
        )

    def process_output(self, response: str) -> WorkerOutput:
        """Process response into structured output"""
        try:
            # Split into sections
            sections = response.split("# ")
            scratch_work = ""
            refinement_decisions = ""
            framework_data = None

            for section in sections:
                if section.startswith("Scratch Work"):
                    scratch_work = section.replace("Scratch Work\n", "").strip()
                elif section.startswith("Refinement Decisions"):
                    refinement_decisions = section.replace(
                        "Refinement Decisions\n", ""
                    ).strip()
                elif section.startswith("Updated Framework Development"):
                    framework_json = section.replace(
                        "Updated Framework Development\n", ""
                    ).strip()
                    framework_data = json.loads(framework_json)

            if not framework_data:
                raise ValueError("Missing framework data")

            # Update state
            self._state["iterations"] += 1
            self._state["refinement_history"].append(
                {
                    "scratch_work": scratch_work,
                    "refinement_decisions": refinement_decisions,
                    "framework_data": framework_data,
                }
            )

            return WorkerOutput(
                modifications={
                    "content": response.strip(),
                    "framework_data": framework_data,
                    "scratch_work": scratch_work,
                    "refinement_decisions": refinement_decisions,
                    "iteration": self._state["iterations"],
                },
                notes={
                    "changes_made": framework_data.get("changes_made", []),
                    "validation_status": framework_data.get("validation_status", {}),
                    "iteration": self._state["iterations"],
                },
                status="completed",
            )

        except Exception as e:
            return WorkerOutput(
                modifications={},
                notes={"error": f"Failed to process response: {str(e)}"},
                status="failed",
            )

    def validate_output(self, output: WorkerOutput) -> bool:
        """Verify output meets requirements"""
        print("\nValidating refinement output...")

        if not output.modifications:
            print("Failed: No modifications")
            return False

        content = output.modifications.get("content")
        if not content:
            print("Failed: No content")
            return False

        # Check for required sections
        required_sections = [
            "# Scratch Work",
            "# Refinement Decisions",
            "# Updated Framework Development",
        ]
        missing_sections = [
            section for section in required_sections if section not in content
        ]
        if missing_sections:
            print(f"Failed: Missing sections: {missing_sections}")
            return False

        # Parse the framework data
        try:
            framework_section = content.split("# Updated Framework Development")[
                1
            ].strip()
            framework_data = json.loads(framework_section)

            # Verify required framework fields
            required_fields = {
                "abstract",
                "main_thesis",
                "core_contribution",
                "key_moves",
                "development_notes",
                "validation_status",
                "changes_made",
            }
            missing_fields = required_fields - set(framework_data.keys())
            if missing_fields:
                print(f"Failed: Missing framework fields: {missing_fields}")
                return False

            # Check abstract length
            words = len(framework_data["abstract"].split())
            if not 120 <= words <= 300:
                print(
                    f"Failed: Abstract length ({words} words) outside valid range (120-300)"
                )
                return False

            # Verify key moves exist and are non-empty
            if not framework_data["key_moves"] or not all(framework_data["key_moves"]):
                print("Failed: Missing or empty key moves")
                return False

            # Verify validation status fields
            required_validation = {
                "scope_appropriate",
                "clearly_articulated",
                "sufficiently_original",
                "feasibly_developable",
            }
            missing_validation = required_validation - set(
                framework_data["validation_status"].keys()
            )
            if missing_validation:
                print(f"Failed: Missing validation fields: {missing_validation}")
                return False

            # Verify changes_made exists and has content
            if not framework_data["changes_made"] or not all(
                framework_data["changes_made"]
            ):
                print("Failed: Missing or empty changes_made")
                return False

            print("Validation passed!")
            return True

        except json.JSONDecodeError as e:
            print(f"Failed: JSON decode error: {str(e)}")
            return False
        except Exception as e:
            print(f"Failed: Unexpected error: {str(e)}")
            return False
