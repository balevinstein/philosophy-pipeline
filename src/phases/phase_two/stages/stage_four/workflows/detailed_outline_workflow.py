from pathlib import Path
from typing import Dict, Any

from src.phases.core.workflow import Workflow, WorkflowStep
from src.phases.phase_two.stages.stage_four.workers.critic.outline_critic import OutlineCriticWorker
from src.phases.phase_two.stages.stage_four.workers.development.framework_integration import FrameworkIntegrationWorker
from src.phases.phase_two.stages.stage_four.workers.development.literature_mapping import LiteratureMappingWorker
from src.phases.phase_two.stages.stage_four.workers.development.content_development import ContentDevelopmentWorker
from src.phases.phase_two.stages.stage_four.workers.development.structural_validation import StructuralValidationWorker
from src.phases.phase_two.stages.stage_four.workers.refinement.outline_refinement import OutlineRefinementWorker


def create_detailed_outline_workflow(
    config: Dict[str, Any],
    output_dir: Path,
    workflow_name: str,
    max_cycles=3,
) -> Workflow:
    """Create workflow for developing a detailed outline.
    
    This workflow processes the initial outline and fully developed key moves
    to create a comprehensive, detailed outline ready for Phase III writing.
    
    The workflow is customized based on the development_phase in the workflow_name:
    - framework_integration: Creates the structural foundation
    - literature_mapping: Maps literature to sections
    - content_development: Develops specific content guidance
    - structural_validation: Validates and finalizes the outline
    """
    # Select the appropriate development worker based on the workflow name
    development_phase = workflow_name.split("_")[-1] if "_" in workflow_name else "framework_integration"
    
    if development_phase == "framework_integration":
        development_worker = FrameworkIntegrationWorker(config)
    elif development_phase == "literature_mapping":
        development_worker = LiteratureMappingWorker(config)
    elif development_phase == "content_development":
        development_worker = ContentDevelopmentWorker(config)
    elif development_phase == "structural_validation":
        development_worker = StructuralValidationWorker(config)
    else:
        # Default to framework integration if we don't recognize the phase
        development_worker = FrameworkIntegrationWorker(config)
        
    # Define required and optional input mappings
    required_inputs = {
        "framework": "framework",
        "outline": "outline",
        "developed_key_moves": "developed_key_moves",
        "literature": "literature",
        "development_phase": "development_phase",
    }
    
    # Optional inputs - these may not always be available (marked with ?)
    optional_inputs = {
        "current_outline_development": "?current_outline_development",  # Optional previous development
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
        "previous_versions": "?current_outline_development",  # Optional previous versions
    })
    
    return Workflow(
        workflow_name=workflow_name,
        max_cycles=max_cycles,
        initial_step=WorkflowStep(
            worker=development_worker,
            input_mapping=dev_input_mapping,  # Include optional inputs
            output_mapping={
                "current_outline_development": "core_content",  # Get the cleaned up content
                "output_versions": "core_content",
                "all_sections": "sections",  # Get structured sections
            },
            name="development",
        ),
        cycle_steps=[
            WorkflowStep(
                worker=OutlineCriticWorker(config),
                input_mapping=critique_input_mapping,  # Include optional inputs
                output_mapping={
                    "current_critique": "core_content",  # Get the cleaned up critique
                    "critique_assessment": "assessment",  # Get the assessment
                    "critique_recommendations": "recommendations",  # Get the recommendations
                },
                name="critique",
            ),
            WorkflowStep(
                worker=OutlineRefinementWorker(config),
                input_mapping=refinement_input_mapping,  # Include all inputs
                output_mapping={
                    "current_refinement": "core_content",  # Get the cleaned up refinement
                    "current_outline_development": "refined_development",  # Get the final refined development
                    "output_versions": "core_content",
                    "changes_made": "changes_made",  # Get the list of changes
                },
                name="refinement",
            ),
        ],
        output_dir=output_dir,
    ) 