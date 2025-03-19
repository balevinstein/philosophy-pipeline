import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime

from src.phases.core.base_workflow import BaseWorkflow
from src.phases.phase_two.stages.stage_four.workers.planner.outline_planning import OutlinePlanningWorker
from src.phases.phase_two.stages.stage_four.workers.planner.outline_development import OutlineDevelopmentWorker
from src.phases.phase_two.stages.stage_four.workers.critic.outline_critic import OutlineCriticWorker
from src.phases.phase_two.stages.stage_four.workers.refinement.outline_refinement import OutlineRefinementWorker


class DetailedOutlineDevelopmentWorkflow(BaseWorkflow):
    """
    Workflow for detailed outline development.
    
    This workflow implements the four-phase approach to outline development:
    1. Framework Integration: Integrating the abstract framework into the outline
    2. Literature Mapping: Incorporating literature review into the outline
    3. Content Development: Developing the content for each section
    4. Structural Validation: Validating the structure of the outline
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.name = "detailed_outline_development"
        self.description = "Develops a detailed outline for the paper, integrating framework, literature, and key moves."
        self.development_phases = [
            "framework_integration",
            "literature_mapping", 
            "content_development", 
            "structural_validation"
        ]
        self.iterations_per_phase = 2
        self.max_iterations = 12
        
        # Initialize workers
        self.planning_worker = OutlinePlanningWorker(config)
        self.development_worker = OutlineDevelopmentWorker(config)
        self.critic_worker = OutlineCriticWorker(config)
        self.refinement_worker = OutlineRefinementWorker(config)
        
        # Store phase outputs
        self._phase_outputs = {}
        self._phase_iterations = {}
        self._current_phase_index = 0
        
    def execute(self, input_data: Dict[str, Any]) -> str:
        """
        Execute the detailed outline development workflow using the four-phase approach.
        
        Args:
            input_data: Dictionary containing framework, outline, key moves, and literature
            
        Returns:
            String containing the final detailed outline
        """
        print(f"\nExecuting {self.name} workflow...")
        
        # Validate input data
        self._validate_input(input_data)
        
        # Plan the outline development
        planning_input = self._prepare_planning_input(input_data)
        planning_output = self.planning_worker.run(planning_input)
        
        # Extract the plan - planning_output is now the modifications dictionary directly
        development_plan = planning_output.get("development_plan", {})
        print(f"\nDevelopment plan: {json.dumps(development_plan, indent=2)}")
        
        # Initialize state with input data and plan
        state = {
            "framework": input_data["framework"],
            "outline": input_data["outline"],
            "developed_key_moves": input_data["developed_key_moves"],
            "literature": input_data.get("literature", {}),
            "development_plan": development_plan,
            "phase_outputs": {},
        }
        
        # Process each development phase
        for i, phase in enumerate(self.development_phases):
            print(f"\n{'='*10} PHASE: {phase.upper()} {'='*10}")
            self._current_phase_index = i
            
            # Update state with current phase
            state["development_phase"] = phase
            state["phase_index"] = i
            
            # Develop initial outline for this phase
            phase_output, phase_iterations = self._process_development_phase(state, phase)
            
            # Store phase output and iteration count
            self._phase_outputs[phase] = phase_output
            self._phase_iterations[phase] = phase_iterations
            
            # Update state for next phase
            state["phase_outputs"][phase] = phase_output
            
            # Debug print the stored phase output
            print(f"\nStored phase output for '{phase}' (first 100 chars): {phase_output[:100]}...")
            print(f"Updated phase_outputs with keys: {list(state['phase_outputs'].keys())}")
            
            # Update current outline development for next phase
            state["current_outline_development"] = phase_output
        
        # Determine best phase output for final result
        final_output = self._determine_best_phase_output()
        print(f"\nSelected final output from phase: {final_output[0]}")
        
        return final_output[1]
    
    def _process_development_phase(self, state: Dict[str, Any], phase: str) -> tuple[str, int]:
        """
        Process a single development phase.
        
        Args:
            state: Current workflow state
            phase: Current development phase
            
        Returns:
            Tuple of (phase_output, iterations_completed)
        """
        print(f"\nProcessing development phase: {phase}")
        
        # Get the number of iterations for this phase
        iterations = min(self.iterations_per_phase, self.max_iterations)
        
        # Initialize phase-specific state
        phase_state = state.copy()
        phase_state["iterations_remaining"] = iterations
        
        # Debug print phase_outputs before development
        print(f"Phase outputs before development: {list(state.get('phase_outputs', {}).keys())}")
        
        # Initial development for this phase
        development_input = self._prepare_development_input(phase_state)
        development_output = self.development_worker.run(development_input)
        
        # Update state with initial development - development_output is now the modifications dictionary
        initial_outline_content = development_output.get("core_content", "")
        phase_state["current_outline_development"] = initial_outline_content
        previous_versions = [initial_outline_content]
        phase_state["previous_versions"] = previous_versions
        
        # Debug print the initial development
        print(f"Initial development content (first 100 chars): {initial_outline_content[:100]}...")
        
        # Run critique-refinement iterations
        iteration = 0
        final_assessment = "NEEDS REFINEMENT"
        
        while (iteration < iterations and 
               final_assessment not in ["EXCELLENT", "VERY GOOD", "GOOD"] and 
               "current_outline_development" in phase_state and
               phase_state["current_outline_development"]):
            
            print(f"\nIteration {iteration + 1}/{iterations} for phase {phase}")
            
            # Run critique step
            print("\nRunning critique step...")
            critique_input = self._prepare_critique_input(phase_state)
            critique_output = self.critic_worker.run(critique_input)
            
            # Extract critique results - critique_output is now the modifications dictionary
            critique_content = critique_output.get("critique", "")
            assessment = critique_output.get("assessment", "NEEDS REFINEMENT")
            recommendations = critique_output.get("recommendations", [])
            
            print(f"Critique assessment: {assessment}")
            print(f"Recommendations count: {len(recommendations)}")
            
            # Update state with critique
            phase_state["current_critique"] = critique_content
            phase_state["critique_assessment"] = assessment
            phase_state["critique_recommendations"] = recommendations
            
            # Store final assessment for this iteration
            final_assessment = assessment
            
            # Run refinement step if needed
            if assessment not in ["EXCELLENT", "VERY GOOD"]:
                print("\nRunning refinement step...")
                refinement_input = self._prepare_refinement_input(phase_state)
                refinement_output = self.refinement_worker.run(refinement_input)
                
                # Update state with refinement - refinement_output is now the modifications dictionary
                refined_development = refinement_output.get("refined_development", "")
                phase_state["current_outline_development"] = refined_development
                
                # Store this version in history
                previous_versions.append(refined_development)
                phase_state["previous_versions"] = previous_versions
                
                # Log changes made
                changes = refinement_output.get("changes_made", [])
                print(f"Changes made: {changes[:3]}")
                
                # Debug print refined content
                print(f"Refined content (first 100 chars): {refined_development[:100]}...")
            else:
                print(f"Skipping refinement due to good assessment: {assessment}")
            
            # Increment iteration counter
            iteration += 1
        
        # Select the best version from this phase
        if previous_versions:
            best_output = self._select_best_output(previous_versions, phase)
            
            # Update the state's phase_outputs to include this phase's output
            state["phase_outputs"][phase] = best_output
            
            # Debug print the stored phase output
            print(f"Storing phase output for '{phase}' (length: {len(best_output)}, first 100 chars): {best_output[:100]}...")
            
            return best_output, iteration
        
        # Fallback if no versions available
        empty_output = "No content developed"
        state["phase_outputs"][phase] = empty_output
        return empty_output, iteration
    
    def _select_best_output(self, versions: List[str], phase: str) -> str:
        """
        Select the best output from all versions in this phase.
        Usually this is the latest version, but we might implement more
        sophisticated selection criteria in the future.
        """
        if not versions:
            return "No content developed"
        
        # For now, return the latest version
        return versions[-1]
    
    def _determine_best_phase_output(self) -> tuple[str, str]:
        """
        Determine the best phase output to use as the final result.
        
        Returns:
            Tuple of (phase_name, phase_output_content)
        """
        # If the full four-phase approach is complete, use the structural_validation phase 
        if "structural_validation" in self._phase_outputs and self._phase_outputs["structural_validation"]:
            return "structural_validation", self._phase_outputs["structural_validation"]
        
        # Otherwise, find the most complete phase output
        best_phase = None
        best_output = ""
        best_score = 0
        
        for phase, output in self._phase_outputs.items():
            if not output:
                continue
                
            # Simple scoring based on output length and structure
            score = len(output)
            
            # Bonus points for structural elements like sections, bullet points
            section_count = output.count("#")
            bullet_count = output.count("- ")
            score += section_count * 100 + bullet_count * 10
            
            if score > best_score:
                best_score = score
                best_phase = phase
                best_output = output
        
        # Fallback if nothing is found
        if not best_phase:
            # Use the last phase that has output
            for phase in reversed(self.development_phases):
                if phase in self._phase_outputs and self._phase_outputs[phase]:
                    return phase, self._phase_outputs[phase]
                    
            # Last resort fallback
            return "none", "No outline developed"
        
        return best_phase, best_output
    
    def _prepare_planning_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare input for the planning worker."""
        return {
            "framework": input_data["framework"],
            "outline": input_data["outline"],
            "developed_key_moves": input_data["developed_key_moves"],
            "literature": input_data.get("literature", {}),
            "development_phases": self.development_phases,
        }
    
    def _prepare_development_input(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare input for the development worker."""
        phase_outputs = state.get("phase_outputs", {})
        print(f"Preparing development input with phase_outputs keys: {list(phase_outputs.keys())}")
        
        # Log what's available for each potential phase
        for phase in self.development_phases:
            if phase in phase_outputs:
                print(f"  - '{phase}' output available (length: {len(phase_outputs[phase])})")
            else:
                print(f"  - '{phase}' output not available")
                
        return {
            "framework": state["framework"],
            "outline": state["outline"],
            "developed_key_moves": state["developed_key_moves"],
            "literature": state.get("literature", {}),
            "development_plan": state.get("development_plan", {}),
            "development_phase": state["development_phase"],
            "phase_index": state["phase_index"],
            "previous_phase_outputs": state.get("phase_outputs", {}),
        }
    
    def _prepare_critique_input(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare input for the critic worker."""
        return {
            "framework": state["framework"],
            "outline": state["outline"],
            "developed_key_moves": state["developed_key_moves"],
            "literature": state.get("literature", {}),
            "current_outline_development": state["current_outline_development"],
            "development_phase": state["development_phase"],
            "previous_versions": state.get("previous_versions", []),
        }
    
    def _prepare_refinement_input(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare input for the refinement worker."""
        return {
            "framework": state["framework"],
            "outline": state["outline"],
            "developed_key_moves": state["developed_key_moves"],
            "literature": state.get("literature", {}),
            "current_outline_development": state["current_outline_development"],
            "critique": state["current_critique"],
            "development_phase": state["development_phase"],
            "previous_versions": state.get("previous_versions", []),
        }
    
    def _validate_input(self, input_data: Dict[str, Any]) -> None:
        """Validate input data for the workflow."""
        required_keys = ["framework", "outline", "developed_key_moves"]
        for key in required_keys:
            if key not in input_data:
                raise ValueError(f"Missing required input: {key}")
    
    def get_phase_output(self, phase: str) -> Optional[str]:
        """Get the output for a specific phase."""
        return self._phase_outputs.get(phase)
    
    def get_phase_iterations(self) -> Dict[str, int]:
        """Get the number of iterations completed for each phase."""
        return self._phase_iterations
    
    def get_all_phase_outputs(self) -> Dict[str, str]:
        """Get all phase outputs."""
        return self._phase_outputs 