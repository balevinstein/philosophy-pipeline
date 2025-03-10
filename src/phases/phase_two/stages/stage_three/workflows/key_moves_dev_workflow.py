from pathlib import Path
from typing import Dict, Any

from src.phases.core.workflow import Workflow, WorkflowStep
from src.phases.phase_two.stages.stage_three.workers.critic.move_critic import MoveCriticWorker
from src.phases.phase_two.stages.stage_three.workers.development.move_development import MoveDevelopmentWorker
from src.phases.phase_two.stages.stage_three.workers.refinement.move_refinement import MoveRefinementWorker


def create_key_moves_dev_workflow(
    config: Dict[str, Any],
    output_dir: Path,
    workflow_name: str,
    max_cycles=3,
) -> Workflow:
    """Create workflow for developing a single key move in depth.
    
    This workflow processes one key move at a time, developing it in detail
    with arguments, examples, and literature connections.
    """
    # Define required and optional input mappings
    required_inputs = {
        "framework": "framework",
        "outline": "outline",
        "key_moves": "key_moves",
        "literature": "literature",
        "move_index": "move_index",
        "development_phase": "development_phase",  # Pass current phase to worker
    }
    
    # Optional inputs - these may not always be available (marked with ?)
    optional_inputs = {
        "current_move_development": "?current_move_development",  # Optional previous development
    }
    
    # For the initial development step, include optional inputs (will be ignored if not available)
    dev_input_mapping = required_inputs.copy()
    dev_input_mapping.update(optional_inputs)
    
    # For critique step, include optional inputs
    critique_input_mapping = required_inputs.copy()
    critique_input_mapping.update(optional_inputs)
    
    # For refinement step, include all inputs with proper optional markings
    refinement_input_mapping = required_inputs.copy()
    refinement_input_mapping.update(optional_inputs)
    refinement_input_mapping.update({
        "current_critique": "?current_critique",  # Optional critique 
        "critique_assessment": "?critique_assessment",  # Optional assessment
        "critique_recommendations": "?critique_recommendations",  # Optional recommendations
        "previous_versions": "?current_move_development",  # Optional previous versions
    })
    
    return Workflow(
        workflow_name=workflow_name,
        max_cycles=max_cycles,
        initial_step=WorkflowStep(
            worker=MoveDevelopmentWorker(config),
            input_mapping=dev_input_mapping,  # Include optional inputs
            output_mapping={
                "current_move_development": "core_content",  # Get the cleaned up content
                "output_versions": "core_content",
                "all_sections": "sections",  # Get structured sections
            },
            name="development",
        ),
        cycle_steps=[
            WorkflowStep(
                worker=MoveCriticWorker(config),
                input_mapping=critique_input_mapping,  # Include optional inputs
                output_mapping={
                    "current_critique": "core_content",  # Get the cleaned up critique
                    "critique_assessment": "assessment",  # Get the assessment
                    "critique_recommendations": "recommendations",  # Get the recommendations
                },
                name="critique",
            ),
            WorkflowStep(
                worker=MoveRefinementWorker(config),
                input_mapping=refinement_input_mapping,  # Include all inputs
                output_mapping={
                    "current_refinement": "core_content",  # Get the cleaned up refinement
                    "current_move_development": "refined_development",  # Get the final refined development
                    "output_versions": "core_content",
                    "changes_made": "changes_made",  # Get the list of changes
                },
                name="refinement",
            ),
        ],
        output_dir=output_dir,
    ) 