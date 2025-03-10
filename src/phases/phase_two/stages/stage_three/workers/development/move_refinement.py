from typing import Dict, Any
from datetime import datetime

from src.phases.core.base_worker import WorkerInput, WorkerOutput
from src.phases.core.llm import LLM


class MoveRefinementWorker:
    """Worker for refining key move development based on critique."""

    def __init__(self, llm: LLM):
        """Initialize the worker with an LLM instance."""
        self._llm = llm
        self._state = {
            "iterations": 0
        }

    def process_input(self, input_data: WorkerInput) -> Dict[str, Any]:
        """Process input for the worker."""
        print("\nPreparing input for move refinement...")
        
        # Extract move development content
        move_development = input_data.context.get("current_move_development", {})
        move_critique = input_data.context.get("current_move_critique", {})
        
        if not move_development:
            print("ERROR: No move development provided for refinement!")
            return {"error": "Missing move development input"}
            
        if not move_critique:
            print("ERROR: No critique provided for refinement!")
            return {"error": "Missing critique input"}
        
        # Extract key information
        move_name = move_development.get("move_name", "Untitled Move")
        development_content = move_development.get("core_content", "")
        critique_content = move_critique.get("critique_content", "")
        
        if not development_content:
            print(f"WARNING: Empty development content for move: {move_name}")
            
        if not critique_content:
            print(f"WARNING: Empty critique content for move: {move_name}")
        
        print(f"Processing refinement for move: {move_name}")
        
        # Prepare the context for the LLM
        context = {
            "move_name": move_name,
            "development_content": development_content,
            "critique_content": critique_content,
            "iteration": self._state["iterations"] + 1
        }
        
        return context

    def generate_prompt(self, context: Dict[str, Any]) -> str:
        """Generate the prompt for the LLM."""
        move_name = context.get("move_name", "Untitled Move")
        development_content = context.get("development_content", "")
        critique_content = context.get("critique_content", "")
        iteration = context.get("iteration", 1)
        
        prompt = f"""You are a philosophical refinement expert. Your job is to revise and enhance a key philosophical move based on critique and feedback.

## Key Move: {move_name}

## Current Development:
{development_content}

## Critique:
{critique_content}

## Your Task

Refine and improve this philosophical move development based on the critique. You should:

1. Address all logical and structural issues raised in the critique
2. Improve clarity and precision in the exposition
3. Strengthen the key arguments and claims
4. Address potential objections proactively
5. Preserve the core philosophical contribution while enhancing its presentation

## Response Format
Provide a complete revised version of the move. This should be a standalone, polished philosophical argument that incorporates all improvements.

---
"""
        return prompt

    def process_output(self, raw_output: str) -> WorkerOutput:
        """Process the raw output from the worker."""
        print("\nProcessing move refinement output...")
        
        # Extract the core content from the raw output
        refined_content = raw_output.strip()
        
        # Create structured output
        modifications = {
            "core_content": refined_content,
            "full_content": refined_content,
            "refined_development": refined_content,
            "changes_made": ["Incorporated critique feedback", "Improved logical structure", "Enhanced clarity"],
            "timestamp": datetime.now().isoformat()
        }
        
        # Create the worker output with the correct parameters
        output = WorkerOutput(
            modifications=modifications,
            notes={
                "iteration": self._state["iterations"],
                "content_length": len(refined_content)
            },
            status="completed"
        )
        
        return output

    def validate_output(self, output: WorkerOutput) -> bool:
        """Verify output meets requirements."""
        print("\nValidating refinement output...")

        if not output.modifications:
            print("Failed: No modifications")
            return False

        refined_content = output.modifications.get("core_content", "")
        if not refined_content or not refined_content.strip():
            print("Failed: No content")
            return False

        # Debug output
        print(f"\nRefined content (first 200 chars): {refined_content[:200]}...")
        
        # Check if we have sufficient content length
        if len(refined_content.strip()) > 500:  # Require at least 500 characters
            print("Content length validation passed")
            return True
        else:
            print("Failed: Content too short")
            return False

    def __call__(self, input_data: WorkerInput) -> WorkerOutput:
        """Process input and generate output with the language model."""
        context = self.process_input(input_data)
        
        if "error" in context:
            print(f"Error preparing input: {context['error']}")
            return WorkerOutput(
                modifications={"error": context["error"]},
                status="error"
            )
        
        prompt = self.generate_prompt(context)
        response = self._llm.generate(prompt)
        
        # Update state - only increment iteration counter
        self._state["iterations"] += 1
        
        output = self.process_output(response)
        
        # Validate the output
        is_valid = self.validate_output(output)
        if not is_valid:
            print("Warning: Output failed validation, but continuing...")
        
        return output 