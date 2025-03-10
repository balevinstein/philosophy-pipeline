from pathlib import Path
import json
import logging
from typing import Dict, Any, List
import datetime

from src.phases.core.workflow import Workflow
from src.phases.phase_two.stages.stage_three.workflows.key_moves_dev_workflow import create_key_moves_dev_workflow


def process_all_key_moves(
    config: Dict[str, Any],
    output_dir: Path,
    framework: Dict[str, Any],
    outline: Dict[str, Any],
    key_moves: Dict[str, Any],
    literature: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Process all key moves in sequence, developing each one in detail.
    
    This function creates and executes a separate workflow for each key move,
    running the development-critique-refinement cycle for each.
    
    Args:
        config: Configuration dictionary
        output_dir: Directory to save outputs
        framework: The abstract framework data
        outline: The outline data
        key_moves: The key moves data from Phase II.2
        literature: The literature data
        
    Returns:
        List of developed key moves
    """
    logging.info("Beginning key moves development process")
    
    # Create the output directory if it doesn't exist
    moves_output_dir = output_dir / "key_moves_development"
    moves_output_dir.mkdir(exist_ok=True)
    
    # Extract the list of key moves from the framework
    moves_list = framework.get("key_moves", [])
    if not moves_list:
        raise ValueError("No key moves found in framework")
    
    developed_moves = []
    
    # Process each key move sequentially
    for i, move in enumerate(moves_list):
        logging.info(f"Processing key move {i+1}/{len(moves_list)}: {move}")
        
        # Create a workflow for this specific move
        workflow_name = f"key_move_{i+1}"
        
        # Define development phases
        development_phases = ["initial", "examples", "literature"]
        
        # Dictionary to store the results of each phase
        phase_results = {}
        previous_phase_result = None
        refinement_history = []
        
        # Process each development phase sequentially
        for phase_idx, phase in enumerate(development_phases):
            logging.info(f"Processing development phase: {phase}")
            
            # For phases after initial, use the previous phase's result
            initial_state = {
                "framework": framework,
                "outline": outline,
                "key_moves": key_moves,  # Always pass the original key_moves
                "literature": literature,
                "move_index": i,  # Pass the index of the current move
                "development_phase": phase,  # Set the current development phase
            }
            
            # Add the previous phase result if available
            if previous_phase_result is not None:
                # Pass the previous phase's refined content as the current content
                if isinstance(previous_phase_result, dict) and "refined_development" in previous_phase_result:
                    initial_state["current_move_development"] = previous_phase_result["refined_development"]
                else:
                    logging.warning(f"Previous phase result doesn't contain expected structure: {type(previous_phase_result)}")
                    # Try to extract useful content anyway
                    if isinstance(previous_phase_result, dict):
                        # Try different possible locations of the content
                        for key in ["core_content", "refined_development", "full_content"]:
                            if key in previous_phase_result:
                                initial_state["current_move_development"] = previous_phase_result[key]
                                break
            
            # Create and execute the workflow for this phase
            workflow = create_key_moves_dev_workflow(
                config=config,
                output_dir=moves_output_dir,
                workflow_name=f"{workflow_name}_{phase}",
                max_cycles=config.get("key_move_max_cycles", 3)
            )
            
            # Execute the workflow and get the result, handling potential errors
            try:
                result = workflow.execute(initial_state)
                
                # Extract only the final refined output for this phase (the most important part)
                if isinstance(result, dict) and "current_move_development" in result:
                    # The result might contain the full cycle history - extract just the final refinement
                    final_refinement = result["current_move_development"]
                    
                    # Record any critique/refinement history if available
                    if "critiques" in result and "refinements" in result:
                        for cycle_idx, (critique, refinement) in enumerate(zip(result.get("critiques", []), result.get("refinements", []))):
                            refinement_history.append({
                                "phase": phase,
                                "cycle": cycle_idx + 1,
                                "assessment": critique.get("assessment", "UNKNOWN"),
                                "recommendations": critique.get("recommendations", []),
                                "changes_made": refinement.get("changes_made", [])
                            })
                else:
                    # If we don't have the expected structure, just use the whole result
                    final_refinement = result
                
                # Save a simplified version of the result (just the final output) to JSON
                output_file = moves_output_dir / f"{workflow_name}_{phase}_final.json"
                
                # Extract just the essential content if possible
                final_content = ""
                if isinstance(final_refinement, dict):
                    if "refined_development" in final_refinement:
                        final_content = final_refinement["refined_development"]
                    elif "core_content" in final_refinement:
                        final_content = final_refinement["core_content"]
                    else:
                        # Try to get sections and combine them
                        sections = final_refinement.get("sections", {})
                        if sections:
                            final_content = "\n\n".join([f"# {section}\n{content}" for section, content in sections.items()])
                        else:
                            # Last resort
                            final_content = str(final_refinement)
                else:
                    final_content = str(final_refinement)
                
                # Save just the essential content
                with open(output_file, "w") as f:
                    json.dump({"content": final_content}, f, indent=2)
                
                # Store this phase's result
                phase_results[phase] = final_content
                
                # Update the previous phase result for the next phase
                previous_phase_result = final_refinement
                
                logging.info(f"Completed {phase} phase for key move {i+1}")
                
            except Exception as e:
                logging.error(f"Error processing {phase} phase for key move {i+1}: {str(e)}")
                
                # Look for initial development content that might be available despite the error
                # This ensures we capture the developed content even if critique fails
                if phase == "initial" and initial_state.get("development_phase") == "initial":
                    try:
                        # Check if we can find the initial development output file
                        dev_output_path = moves_output_dir / f"{workflow_name}_{phase}.json"
                        if dev_output_path.exists():
                            with open(dev_output_path, "r") as f:
                                dev_data = json.load(f)
                                if "output" in dev_data and "modifications" in dev_data["output"]:
                                    mods = dev_data["output"]["modifications"]
                                    if "core_content" in mods:
                                        # We found the content! Use it instead of the error message
                                        content = mods["core_content"]
                                        logging.info(f"Recovered content from development phase despite critique error")
                                        phase_results[phase] = content
                                        previous_phase_result = {"core_content": content}
                    except Exception as recovery_error:
                        logging.error(f"Failed to recover content after error: {str(recovery_error)}")
                
                # If we couldn't recover content, use the error message
                if phase not in phase_results:
                    # Create a minimal result for this phase to allow continuing
                    error_result = {
                        "error": str(e),
                        "phase": phase,
                        "move_index": i,
                        "move": move,
                        "status": "failed",
                    }
                    
                    # Save the error result
                    error_file = moves_output_dir / f"{workflow_name}_{phase}_error.json"
                    with open(error_file, "w") as f:
                        json.dump(error_result, f, indent=2)
                    
                    # Store this phase's error result
                    phase_results[phase] = f"Error in {phase} phase: {str(e)}"
                
                # If this is the first phase and it failed, we can't continue with this move
                if phase == "initial" and phase not in phase_results:
                    logging.error(f"Initial phase failed for key move {i+1}, skipping remaining phases")
                    break
                
                # For later phases, we can continue with the previous phase's result
                if previous_phase_result:
                    logging.warning(f"Continuing to next phase using previous result")
                else:
                    logging.error(f"No previous result available, skipping remaining phases for key move {i+1}")
                    break
        
        # Combine all phase results for this move into a clean, structured format
        move_result = {
            "key_move_index": i,
            "key_move_text": move,
            "development": {
                "initial": phase_results.get("initial", ""),
                "examples": phase_results.get("examples", ""),
                "literature": phase_results.get("literature", ""),
            },
            "final_content": phase_results.get("literature", phase_results.get("examples", phase_results.get("initial", ""))),
            "refinement_history": refinement_history
        }
        
        # Save the complete move result
        move_output_file = moves_output_dir / f"{workflow_name}_complete.json"
        with open(move_output_file, "w") as f:
            json.dump(move_result, f, indent=2)
        
        developed_moves.append(move_result)
        
        logging.info(f"Completed all phases for key move {i+1}")
    
    # Create a combined output file with all developed moves - this is the primary output for Phase II.4
    # First check if we have actual content in the developed_moves or if we need to recover it
    for move_idx, move_result in enumerate(developed_moves):
        # Check if we have error messages instead of content
        if (isinstance(move_result["final_content"], str) and 
            move_result["final_content"].startswith("Error")):
            
            # Try to recover content from individual files
            try:
                # Check for individual output files
                move_name = f"key_move_{move_idx+1}"
                for phase in ["literature", "examples", "initial"]:  # Check in reverse order of preference
                    output_file = moves_output_dir / f"{move_name}_{phase}_final.json"
                    if output_file.exists():
                        with open(output_file) as f:
                            data = json.load(f)
                            if "content" in data and data["content"]:
                                # Found content, use it
                                move_result["final_content"] = data["content"]
                                move_result["development"][phase] = data["content"]
                                print(f"Recovered content for {move_name} from {phase} phase")
                                break
            except Exception as recovery_error:
                logging.error(f"Error recovering content for move {move_idx+1}: {str(recovery_error)}")
    
    combined_output = {
        "developed_moves": developed_moves,
        "metadata": {
            "framework_title": "Philosophy Paper Framework", # Generic title
            "main_thesis": framework.get("main_thesis", "") if isinstance(framework, dict) else "",
            "core_contribution": framework.get("core_contribution", "") if isinstance(framework, dict) else "",
            "processing_date": str(datetime.datetime.now()),
        }
    }
    
    combined_output_file = moves_output_dir / "all_developed_moves.json"
    with open(combined_output_file, "w") as f:
        json.dump(combined_output, f, indent=2)
    
    # Also create a simplified, plain text version for easier review
    combined_text = []
    combined_text.append(f"# Developed Key Moves\n")
    
    # Add thesis and contribution if available
    if isinstance(framework, dict):
        main_thesis = framework.get("main_thesis", "")
        core_contribution = framework.get("core_contribution", "")
        if main_thesis:
            combined_text.append(f"## Main Thesis\n{main_thesis}\n")
        if core_contribution:
            combined_text.append(f"## Core Contribution\n{core_contribution}\n")
    
    for move_idx, move_result in enumerate(developed_moves):
        combined_text.append(f"## Key Move {move_idx+1}: {move_result['key_move_text']}\n")
        combined_text.append(f"### Final Development\n{move_result['final_content']}\n\n")
    
    combined_text_file = moves_output_dir / "all_developed_moves.md"
    with open(combined_text_file, "w") as f:
        f.write("\n".join(combined_text))
    
    logging.info(f"Key moves development completed. Results saved to {combined_output_file} and {combined_text_file}")
    
    return developed_moves 