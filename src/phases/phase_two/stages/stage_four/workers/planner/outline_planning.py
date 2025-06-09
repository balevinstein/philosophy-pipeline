from typing import Dict, Any, List
import json
from datetime import datetime

from src.phases.core.base_worker import WorkerInput, WorkerOutput
from src.phases.core.worker_types import PlanningWorker
from src.utils.api import APIHandler


class OutlinePlanningWorker(PlanningWorker):
    """
    Worker responsible for planning the detailed outline development process.
    
    This worker creates a plan for developing the detailed outline using the four-phase approach:
    1. Framework Integration: Integrating the abstract framework into the outline
    2. Literature Mapping: Incorporating literature review into the outline
    3. Content Development: Developing the content for each section
    4. Structural Validation: Validating the structure of the outline
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.stage_name = "detailed_outline_planning"
        self._state = {
            "iterations": 0,
        }
        self.api_handler = APIHandler(config)

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the planning worker to create a development plan."""
        print(f"\nRunning {self.stage_name} worker...")
        
        # Process input data
        input_data = self.process_input(state)
        
        # Construct prompt
        prompt = self._construct_prompt(input_data)
        
        # Execute LLM call
        raw_output = self._execute_llm_call(prompt)
        
        # Process output
        output = self.process_output(raw_output)
        
        # Validate output
        if not self.validate_output(output):
            raise ValueError(f"Output validation failed for {self.stage_name}")
        
        return output.modifications

    def _execute_llm_call(self, prompt: str) -> str:
        """Execute the LLM call with the given prompt."""
        print(f"\nExecuting LLM call for {self.stage_name}...")
        
        # Use the API handler to make actual API calls
        # Check if there's a specific model config for this stage
        model_stage = "detailed_outline_planning"
        
        # If specific model config doesn't exist, fall back to a related one
        if model_stage not in self.api_handler.config.get("models", {}):
            model_stage = "abstract_development"  # Use a similar stage's config
            print(f"No specific model config for {self.stage_name}, using {model_stage} instead")
            
        # API handler returns (response_text, duration) tuple, we only need the response text
        response_text, _ = self.api_handler.make_api_call(model_stage, prompt)
        return response_text

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        """Construct the planning prompt."""
        framework = input_data.context.get("framework", {})
        outline = input_data.context.get("outline", {})
        developed_key_moves = input_data.context.get("developed_key_moves", [])
        literature = input_data.context.get("literature", {})
        development_phases = input_data.context.get("development_phases", [
            "framework_integration", 
            "literature_mapping", 
            "content_development", 
            "structural_validation"
        ])
        
        # Format the development phases
        phases_text = "\n".join([f"- Phase {i+1}: {phase.replace('_', ' ').title()}" for i, phase in enumerate(development_phases)])
        
        # Extract key information from inputs
        framework_name = framework.get("name", "")
        framework_description = framework.get("description", "")
        
        outline_title = outline.get("title", "")
        
        # Format key moves for inclusion in the prompt
        key_moves_text = ""
        
        # Check if developed_key_moves is a dictionary with 'developed_moves' key
        if isinstance(developed_key_moves, dict) and "developed_moves" in developed_key_moves:
            moves_list = developed_key_moves.get("developed_moves", [])
            for i, move in enumerate(moves_list):
                if isinstance(move, dict):
                    move_text = move.get("key_move_text", f"Key Move {i+1}")
                    key_moves_text += f"- **Key Move {i+1}**: {move_text}\n"
        # Check if it's already a list
        elif isinstance(developed_key_moves, list):
            for i, move in enumerate(developed_key_moves):
                if isinstance(move, dict):
                    # Try different possible key names for moves
                    move_name = move.get("name", move.get("key_move_text", f"Key Move {i+1}"))
                    move_description = move.get("description", move.get("final_content", ""))
                    key_moves_text += f"- **{move_name}**: {move_description[:100]}...\n"
                else:
                    # If it's a string or other type, just use it directly
                    key_moves_text += f"- **Key Move {i+1}**: {str(move)[:100]}...\n"
        else:
            # If it's a string (perhaps JSON that needs parsing) or some other type
            key_moves_text = f"- Key Moves: {str(developed_key_moves)[:200]}...\n"
            try:
                # Try to parse as JSON if it's a string
                if isinstance(developed_key_moves, str):
                    parsed_moves = json.loads(developed_key_moves)
                    if isinstance(parsed_moves, dict) and "developed_moves" in parsed_moves:
                        moves_list = parsed_moves.get("developed_moves", [])
                        key_moves_text = ""
                        for i, move in enumerate(moves_list):
                            if isinstance(move, dict):
                                move_text = move.get("key_move_text", f"Key Move {i+1}")
                                key_moves_text += f"- **Key Move {i+1}**: {move_text}\n"
            except:
                pass  # Keep the default text if parsing fails
        
        # Format literature for inclusion in the prompt
        literature_text = ""
        literature_sources = literature.get("sources", [])
        for i, source in enumerate(literature_sources[:5]):  # Limit to first 5 sources
            source_title = source.get("title", f"Source {i+1}")
            source_author = source.get("author", "")
            literature_text += f"- {source_title} (by {source_author})\n"
        
        if len(literature_sources) > 5:
            literature_text += f"- Plus {len(literature_sources) - 5} more sources...\n"
        
        # Construct the prompt
        prompt = f"""# Detailed Outline Development Planning

You are planning the development of a detailed outline for a philosophical paper titled "{outline_title}". 

## Development Approach

You will be using a four-phase approach to develop the detailed outline:

{phases_text}

## Available Inputs

You have the following inputs available:

1. **Abstract Framework**:
   - Name: {framework_name}
   - Description: {framework_description}

2. **Basic Outline Structure**:
   - Title: {outline_title}
   - Contains {len(outline.get("sections", []))} main sections

3. **Key Philosophical Moves**:
{key_moves_text}

4. **Literature**:
{literature_text}

## Your Task: Create a Development Plan

Your task is to create a plan for developing the detailed outline using the four-phase approach. For each phase:

1. Identify the specific goals and objectives
2. Determine what inputs will be most relevant
3. Outline the expected outputs
4. Identify potential challenges and strategies to address them

## Output Format

Produce a development plan with the following structure:

1. **Overall Strategy**: A brief overview of how you will approach the detailed outline development.

2. **Phase-by-Phase Plan**:
   - For each phase, provide:
     - Goals and objectives
     - Key inputs to focus on
     - Expected outputs
     - Potential challenges and strategies

3. **Integration Strategy**: How you will ensure the phases build upon each other.

4. **Success Criteria**: How you will evaluate the quality of the final detailed outline.

Ensure your plan is clear, comprehensive, and focused on producing a high-quality detailed outline for a philosophical paper.
"""
        
        return prompt

    def process_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Prepare input for outline planning."""
        print("\nPreparing input for outline planning...")
        print("\nReceived state keys:", list(state.keys()))

        # Validate required inputs
        if "framework" not in state or "outline" not in state:
            raise ValueError("Missing required state: framework, outline")
        
        # Get development phases if available
        development_phases = state.get("development_phases", [
            "framework_integration", 
            "literature_mapping", 
            "content_development", 
            "structural_validation"
        ])
        
        # Increment iterations counter
        self._state["iterations"] += 1
        
        return WorkerInput(
            context={
                "framework": state["framework"],
                "outline": state["outline"],
                "developed_key_moves": state.get("developed_key_moves", []),
                "literature": state.get("literature", {}),
                "development_phases": development_phases,
            },
            parameters={
                "phase": "outline_planning",
                "iteration": self._state["iterations"],
            },
        )

    def process_output(self, raw_output: str) -> WorkerOutput:
        """Process the raw output from the planning worker."""
        print("\nProcessing outline planning output...")
        
        # Extract the development plan from the raw output
        development_plan = self._extract_development_plan(raw_output)
        
        # Create structured output
        modifications = {
            "development_plan": development_plan,
            "raw_plan": raw_output.strip(),
            "timestamp": datetime.now().isoformat(),
        }
        
        # Create the worker output with the correct parameters
        output = WorkerOutput(
            modifications=modifications,
            notes={
                "plan_sections": list(development_plan.keys()),
            },
            status="completed"
        )
        
        return output

    def _extract_development_plan(self, content: str) -> Dict[str, Any]:
        """Extract the development plan from the raw output."""
        plan = {
            "overall_strategy": "",
            "phases": {},
            "integration_strategy": "",
            "success_criteria": "",
        }
        
        # Extract overall strategy
        if "Overall Strategy" in content:
            parts = content.split("Overall Strategy", 1)[1].split("##", 1)
            if parts:
                plan["overall_strategy"] = parts[0].strip()
        
        # Extract phase-by-phase plan
        if "Phase-by-Phase Plan" in content:
            phase_section = content.split("Phase-by-Phase Plan", 1)[1].split("##", 1)[0]
            
            # Look for each phase
            phases = ["framework_integration", "literature_mapping", "content_development", "structural_validation"]
            for phase in phases:
                phase_title = phase.replace("_", " ").title()
                if phase_title in phase_section:
                    phase_content = phase_section.split(phase_title, 1)[1].split(phases[(phases.index(phase) + 1) % len(phases)].replace("_", " ").title(), 1)[0]
                    plan["phases"][phase] = {
                        "goals": self._extract_subsection(phase_content, "Goals"),
                        "inputs": self._extract_subsection(phase_content, "Inputs"),
                        "outputs": self._extract_subsection(phase_content, "Outputs"),
                        "challenges": self._extract_subsection(phase_content, "Challenges"),
                    }
        
        # Extract integration strategy
        if "Integration Strategy" in content:
            parts = content.split("Integration Strategy", 1)[1].split("##", 1)
            if parts:
                plan["integration_strategy"] = parts[0].strip()
        
        # Extract success criteria
        if "Success Criteria" in content:
            parts = content.split("Success Criteria", 1)[1].split("##", 1)
            if parts:
                plan["success_criteria"] = parts[0].strip()
        
        return plan
    
    def _extract_subsection(self, content: str, subsection_name: str) -> str:
        """Extract a subsection from the content."""
        if subsection_name in content:
            parts = content.split(subsection_name, 1)[1].split("###", 1)
            return parts[0].strip()
        return ""

    def validate_output(self, output: WorkerOutput) -> bool:
        """Verify output meets requirements."""
        print("\nValidating outline planning output...")

        if not output.modifications:
            print("Failed: No modifications")
            return False

        # Check for development plan
        plan = output.modifications.get("development_plan")
        if not plan:
            print("Failed: No development plan")
            return False

        # Check for overall strategy
        if not plan.get("overall_strategy"):
            print("Warning: No overall strategy")

        # Check for phases
        phases = plan.get("phases", {})
        if not phases:
            print("Warning: No phases in plan")

        # Debug output
        print(f"\nDevelopment plan sections: {list(plan.keys())}")
        print(f"Phases in plan: {list(phases.keys())}")
        
        return True 