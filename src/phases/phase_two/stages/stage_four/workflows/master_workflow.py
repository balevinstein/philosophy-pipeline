from pathlib import Path
import json
import logging
from typing import Dict, Any, List
import datetime

from src.phases.core.workflow import Workflow
from src.phases.phase_two.stages.stage_four.workflows.detailed_outline_workflow import create_detailed_outline_workflow


def develop_detailed_outline(
    config: Dict[str, Any],
    output_dir: Path,
    framework: Dict[str, Any],
    outline: Dict[str, Any],
    developed_key_moves: List[Dict[str, Any]],
    literature: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Develop a comprehensive detailed outline integrating the fully developed key moves.
    
    This function takes the initial outline from II.2 and the developed key moves from II.3
    and creates a detailed outline ready for Phase III writing.
    
    Args:
        config: Configuration dictionary
        output_dir: Directory to save outputs
        framework: The abstract framework data
        outline: The initial outline data from Phase II.2
        developed_key_moves: The fully developed key moves from Phase II.3
        literature: The literature data
        
    Returns:
        Dict containing the detailed outline
    """
    logging.info("Beginning detailed outline development process")
    
    # Create the output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Create workflow for detailed outline development
    workflow_name = "detailed_outline"
    
    # Define development phases - we'll develop the outline in distinct phases
    # New four-phase approach for better cognitive distribution
    development_phases = [
        "framework_integration",  # Analyze abstract & key moves, create structure
        "literature_mapping",     # Map literature to sections
        "content_development",    # Develop content guidance for each section
        "structural_validation"   # Validate the complete outline
    ]
    
    # Dictionary to store the results of each phase
    phase_results = {}
    previous_phase_result = None
    refinement_history = []
    
    # Process each development phase sequentially
    for phase_idx, phase in enumerate(development_phases):
        logging.info(f"Processing development phase: {phase}")
        
        # Initial state for this phase
        initial_state = {
            "framework": framework,
            "outline": outline,  # Original outline from Phase II.2
            "developed_key_moves": developed_key_moves,  # Fully developed key moves from Phase II.3
            "literature": literature,
            "development_phase": phase,  # Current development phase
        }
        
        # Add the previous phase result if available
        if previous_phase_result is not None:
            # Handle different possible formats of previous_phase_result
            current_outline_content = extract_content_from_result(previous_phase_result)
            if current_outline_content:
                initial_state["current_outline_development"] = current_outline_content
                logging.info(f"Added previous phase result to state (content length: {len(current_outline_content) if isinstance(current_outline_content, str) else 'non-string'})")
            else:
                logging.warning(f"Could not extract usable content from previous phase result")
        
        # Determine the max cycles to use for this phase
        max_cycles_key = f"{phase}_max_cycles"
        max_cycles = config.get(max_cycles_key, config.get("outline_max_cycles", 3))
        
        # Create and execute the workflow for this phase
        workflow = create_detailed_outline_workflow(
            config=config,
            output_dir=output_dir,
            workflow_name=f"{workflow_name}_{phase}",
            max_cycles=max_cycles
        )
        
        # Execute the workflow and get the result, handling potential errors
        try:
            result = workflow.execute(initial_state)
            logging.info(f"Workflow execution complete for {phase} phase")
            
            # Extract the final result in a format suitable for saving and passing to next phase
            final_content = extract_content_from_result(result)
            
            # Record any critique/refinement history if available
            record_refinement_history(result, phase, refinement_history)
            
            # Save a simplified version of the result (just the final output) to JSON
            output_file = output_dir / f"{workflow_name}_{phase}_final.json"
            
            # Save just the essential content
            with open(output_file, "w") as f:
                json.dump({"content": final_content}, f, indent=2)
            
            # Store this phase's result
            phase_results[phase] = final_content
            
            # Update the previous phase result for the next phase
            previous_phase_result = result
            
            logging.info(f"Completed {phase} phase for detailed outline development")
            
        except Exception as e:
            logging.error(f"Error processing {phase} phase for detailed outline: {str(e)}")
            
            # Create a minimal result for this phase to allow continuing
            error_result = {
                "error": str(e),
                "phase": phase,
                "status": "failed",
            }
            
            # Save the error result
            error_file = output_dir / f"{workflow_name}_{phase}_error.json"
            with open(error_file, "w") as f:
                json.dump(error_result, f, indent=2)
            
            # Store this phase's error result
            phase_results[phase] = f"Error in {phase} phase: {str(e)}"
            
            # For later phases, we can continue with the previous phase's result
            if previous_phase_result:
                logging.warning(f"Continuing to next phase using previous result")
            else:
                logging.error(f"No previous result available, skipping remaining phases")
                break
    
    # Determine the best final outline content - prioritize the structural_validation phase
    final_outline = select_best_final_outline(phase_results)
    
    # Combine all phase results into a clean, structured format
    outline_result = {
        "framework_integration": phase_results.get("framework_integration", ""),
        "literature_mapping": phase_results.get("literature_mapping", ""),
        "content_development": phase_results.get("content_development", ""),
        "structural_validation": phase_results.get("structural_validation", ""),
        "final_outline": final_outline,
        "refinement_history": refinement_history
    }
    
    # Save the complete outline result
    outline_output_file = output_dir / f"{workflow_name}_complete.json"
    with open(outline_output_file, "w") as f:
        json.dump(outline_result, f, indent=2)
    
    # Also save the final outline as a standalone markdown file for easier reading
    final_outline_md = output_dir / "detailed_outline_final.md"
    with open(final_outline_md, "w") as f:
        f.write(final_outline)
    
    logging.info("Completed all phases for detailed outline development")
    
    return outline_result


def extract_content_from_result(result: Any) -> str:
    """
    Extract the meaningful content from a workflow result regardless of its format.
    
    Handles various possible result structures and formats to extract the most
    useful content for saving or passing to the next phase.
    
    Args:
        result: The workflow result, which could be a dict, string, or other format
        
    Returns:
        A string containing the extracted content
    """
    if isinstance(result, str):
        return result
        
    if not isinstance(result, dict):
        return str(result)
    
    # Try various possible locations for the content in a dictionary result
    if "current_outline_development" in result:
        development = result["current_outline_development"]
        if isinstance(development, dict):
            # Try to get content from the development dictionary
            if "refined_development" in development:
                return development["refined_development"]
            elif "core_content" in development:
                return development["core_content"]
            elif "content" in development:
                return development["content"]
            else:
                # As a last resort, convert the whole dict to a string
                return str(development)
        else:
            # If it's not a dict (likely a string), return it directly
            return str(development)
    
    # Check other common content locations
    if "refined_development" in result:
        return result["refined_development"]
    elif "core_content" in result:
        return result["core_content"]
    elif "full_content" in result:
        return result["full_content"]
    elif "content" in result:
        return result["content"]
    
    # Try to process sections if available
    if "sections" in result and isinstance(result["sections"], dict):
        sections = result["sections"]
        return "\n\n".join([f"# {section}\n{content}" for section, content in sections.items()])
    
    # If all else fails, convert the entire result to a string
    return str(result)


def record_refinement_history(result: Any, phase: str, history: List[Dict[str, Any]]) -> None:
    """
    Extract and record refinement history from a workflow result.
    
    Args:
        result: The workflow result
        phase: The current development phase
        history: The list to append history records to
    """
    if not isinstance(result, dict):
        return
        
    # Try to extract critique and refinement data
    critiques = result.get("critiques", [])
    refinements = result.get("refinements", [])
    
    # If we have direct critique/refinement data
    if critiques and refinements and len(critiques) == len(refinements):
        for cycle_idx, (critique, refinement) in enumerate(zip(critiques, refinements)):
            # Handle both dict and string critique/refinement objects
            if isinstance(critique, dict):
                assessment = critique.get("assessment", "UNKNOWN")
                recommendations = critique.get("recommendations", [])
            else:
                assessment = "UNKNOWN"
                recommendations = []

            if isinstance(refinement, dict):
                changes_made = refinement.get("changes_made", [])
            else:
                changes_made = []

            history.append({
                "phase": phase,
                "cycle": cycle_idx + 1,
                "assessment": assessment,
                "recommendations": recommendations,
                "changes_made": changes_made
            })
    else:
        # Try alternate formats
        for key in result:
            if isinstance(result[key], dict) and ("critique" in key.lower() or "assessment" in key.lower()):
                critique_data = result[key]
                history.append({
                    "phase": phase,
                    "cycle": len(history) + 1,
                    "assessment": critique_data.get("assessment", "UNKNOWN"),
                    "recommendations": critique_data.get("recommendations", [])
                })


def select_best_final_outline(phase_results: Dict[str, str]) -> str:
    """
    Select the best outline from the phase results to use as the final output.
    
    This function implements a preference order for our new four-phase approach,
    prioritizing the final structural_validation phase but falling back to earlier
    phases if needed.
    
    Args:
        phase_results: Dictionary mapping phase names to their results
        
    Returns:
        The selected outline content
    """
    # New preference order: structural_validation > content_development > literature_mapping > framework_integration
    for phase in ["structural_validation", "content_development", "literature_mapping", "framework_integration"]:
        result = phase_results.get(phase, "")
        
        # Skip empty results or error messages
        if result and not result.startswith("Error in"):
            # If the result starts with words asking for content, it probably failed
            lower_result = result.lower()
            if any(phrase in lower_result[:200] for phrase in ["i notice", "i don't have", "no outline", "missing"]):
                logging.warning(f"Skipping {phase} result that appears to be a request for more input")
                continue
                
            return result
    
    # If all phases had issues, use framework_integration as a fallback (or empty string if none available)
    return phase_results.get("framework_integration", "") 