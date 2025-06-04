from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import json
from pathlib import Path

from src.phases.core.base_worker import BaseWorker, WorkerInput, WorkerOutput
from src.phases.phase_two.stages.stage_four.prompts.development.development_prompts import OutlineDevelopmentPrompts
from src.utils.api import APIHandler


@dataclass
class OutlineDevelopmentWorker(BaseWorker):
    """
    Worker for developing the detailed outline according to the development plan.
    
    Processes the outline according to the current development phase.
    Enhanced with Analysis PDF integration for structural guidance.
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.name = "detailed_outline_development"
        self.description = "Develops the detailed outline according to the development plan."
        self.prompts = OutlineDevelopmentPrompts()
        self.api_handler = APIHandler(config)  # Initialize API handler
        self.stage_name = "detailed_outline_development"  # For compatibility with BaseWorker
        self.selected_analysis_pdfs = []  # Store selected Analysis PDFs

    def _get_analysis_pdfs(self, pdf_count: int = 1) -> list:
        """Select Analysis PDFs for structural guidance"""
        analysis_dir = Path("Analysis_papers")
        if not analysis_dir.exists():
            print(f"⚠️ Analysis papers directory not found at {analysis_dir}")
            return []
        
        pdf_files = list(analysis_dir.glob("*.pdf"))
        if not pdf_files:
            print(f"⚠️ No PDF files found in {analysis_dir}")
            return []
        
        # Select PDFs with preference for structural variety
        selected_pdfs = pdf_files[:pdf_count]
        
        print(f"📑 Including {len(selected_pdfs)} Analysis paper(s) for {self.name} guidance:")
        for pdf in selected_pdfs:
            print(f"   • {pdf.name}")
        
        return selected_pdfs
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the outline development worker with Analysis PDF support.
        
        Args:
            input_data: Dictionary containing the input data for the worker
            
        Returns:
            Dictionary containing the output from the worker
        """
        print(f"\nRunning {self.name} worker...")
        
        # Process input
        worker_input = self.process_input(input_data)
        
        # Select Analysis PDFs for structural guidance
        development_phase = input_data.get("development_phase", "framework_integration")
        pdf_count = 1 if development_phase == "framework_integration" else 1  # Could vary by phase
        analysis_pdfs = self._get_analysis_pdfs(pdf_count=pdf_count)
        self.selected_analysis_pdfs = analysis_pdfs
        
        # Construct prompt
        prompt = self._construct_prompt(worker_input)
        
        # Call LLM with Analysis PDFs if available
        print(f"\nExecuting LLM call for {self.name}...")
        if self.selected_analysis_pdfs:
            response = self.api_handler.make_api_call(
                stage=self.stage_name,
                prompt=prompt,
                pdf_paths=self.selected_analysis_pdfs
            )
        else:
            response = self.api_handler.make_api_call(
                stage=self.stage_name,
                prompt=prompt
            )
        
        # Process output
        output = self._process_llm_response(response)
        print(f"Processed {self.name} output.")
        
        return output
    
    def process_input(self, input_data: Dict[str, Any]) -> WorkerInput:
        """Process the input data for the worker."""
        # Ensure required data is present
        required_states = ["framework", "outline", "developed_key_moves", "development_phase", "phase_index"]
        for key in required_states:
            if key not in input_data:
                raise ValueError(f"Missing required state: {key}")
        
        # Extract and prepare context
        context = {
            "framework": input_data["framework"],
            "outline": input_data["outline"],
            "developed_key_moves": input_data["developed_key_moves"],
            "literature": input_data.get("literature", {}),
            "development_plan": input_data.get("development_plan", {}),
            "development_phase": input_data["development_phase"],
            "phase_index": input_data["phase_index"],
            "previous_phase_outputs": input_data.get("previous_phase_outputs", {}),
        }
        
        # Debug information
        print(f"Development phase: {context['development_phase']}")
        print(f"Phase index: {context['phase_index']}")
        print(f"Previous phase outputs available: {list(context['previous_phase_outputs'].keys())}")
        
        # Prepare parameters
        parameters = {
            "temperature": self.config.get("temperature", 0.7),
            "top_p": self.config.get("top_p", 0.95),
            "max_tokens": self.config.get("max_tokens", 4000),
        }
        
        return WorkerInput(context=context, parameters=parameters)
    
    def _construct_prompt(self, input_data: WorkerInput) -> str:
        """
        Construct a prompt for the model based on the development phase.
        
        Args:
            input_data: Worker input data
            
        Returns:
            Prompt for the model
        """
        # Extract context
        framework = input_data.context["framework"]
        outline = input_data.context["outline"]
        developed_key_moves = input_data.context["developed_key_moves"]
        literature = input_data.context.get("literature", {})
        development_plan = input_data.context.get("development_plan", {})
        development_phase = input_data.context["development_phase"]
        previous_phase_outputs = input_data.context.get("previous_phase_outputs", {})
        
        # Debug logs
        print(f"Constructing prompt for development phase: {development_phase}")
        print(f"Framework type: {type(framework)}")
        print(f"Framework keys: {list(framework.keys()) if isinstance(framework, dict) else 'Not a dict'}")
        print(f"Developed key moves type: {type(developed_key_moves)}")
        print(f"Previous phase outputs keys: {list(previous_phase_outputs.keys())}")
        
        # Format the framework data to ensure we have the abstract, main thesis, and key moves
        formatted_framework = {}
        if isinstance(framework, dict):
            formatted_framework["abstract"] = framework.get("abstract", "No abstract available")
            formatted_framework["main_thesis"] = framework.get("main_thesis", "No main thesis available")
            formatted_framework["key_moves"] = framework.get("key_moves", [])
        else:
            # Try to parse as JSON if it's a string
            try:
                if isinstance(framework, str):
                    parsed_framework = json.loads(framework)
                    formatted_framework["abstract"] = parsed_framework.get("abstract", "No abstract available")
                    formatted_framework["main_thesis"] = parsed_framework.get("main_thesis", "No main thesis available")
                    formatted_framework["key_moves"] = parsed_framework.get("key_moves", [])
                else:
                    formatted_framework["abstract"] = "No abstract available"
                    formatted_framework["main_thesis"] = "No main thesis available"
                    formatted_framework["key_moves"] = []
            except:
                formatted_framework["abstract"] = "No abstract available"
                formatted_framework["main_thesis"] = "No main thesis available"
                formatted_framework["key_moves"] = []
        
        # Format developed key moves to ensure we have the text for each move
        formatted_key_moves = []
        if isinstance(developed_key_moves, list):
            for move in developed_key_moves:
                if isinstance(move, dict):
                    move_text = move.get("text", "")
                    if not move_text and "final_content" in move:
                        move_text = move.get("final_content", "")
                    formatted_key_moves.append(move_text if move_text else str(move))
                else:
                    formatted_key_moves.append(str(move))
        elif isinstance(developed_key_moves, dict):
            # If it's a dictionary with numbered keys
            for key, move in developed_key_moves.items():
                if isinstance(move, dict):
                    move_text = move.get("text", "")
                    if not move_text and "final_content" in move:
                        move_text = move.get("final_content", "")
                    formatted_key_moves.append(move_text if move_text else str(move))
                else:
                    formatted_key_moves.append(str(move))
        else:
            # If it's already a string, try to parse it
            try:
                if isinstance(developed_key_moves, str):
                    parsed_moves = json.loads(developed_key_moves)
                    if isinstance(parsed_moves, list):
                        for move in parsed_moves:
                            if isinstance(move, dict):
                                move_text = move.get("text", "")
                                if not move_text and "final_content" in move:
                                    move_text = move.get("final_content", "")
                                formatted_key_moves.append(move_text if move_text else str(move))
                            else:
                                formatted_key_moves.append(str(move))
                    elif isinstance(parsed_moves, dict):
                        for key, move in parsed_moves.items():
                            if isinstance(move, dict):
                                move_text = move.get("text", "")
                                if not move_text and "final_content" in move:
                                    move_text = move.get("final_content", "")
                                formatted_key_moves.append(move_text if move_text else str(move))
                            else:
                                formatted_key_moves.append(str(move))
            except:
                # If parsing fails, just use as is
                formatted_key_moves = [str(developed_key_moves)]
        
        # Get the previous phase outputs as a dictionary
        previous_outputs = {}
        for phase in previous_phase_outputs:
            previous_outputs[phase] = previous_phase_outputs[phase]
        
        # Log the formatted data
        print(f"Formatted framework abstract length: {len(formatted_framework['abstract'])}")
        print(f"Formatted framework main thesis length: {len(formatted_framework['main_thesis'])}")
        print(f"Formatted key moves count: {len(formatted_key_moves)}")
        print(f"Previous outputs phases: {list(previous_outputs.keys())}")
        
        # Get the prompt based on the development phase
        if development_phase == "framework_integration":
            return self.prompts.get_framework_integration_prompt(
                formatted_framework,
                formatted_key_moves,
                previous_outputs
            )
        elif development_phase == "literature_mapping":
            return self.prompts.get_literature_mapping_prompt(
                formatted_framework,
                formatted_key_moves,
                literature,
                previous_outputs
            )
        elif development_phase == "content_development":
            return self.prompts.get_content_development_prompt(
                formatted_framework,
                formatted_key_moves,
                literature,
                previous_outputs
            )
        elif development_phase == "structural_validation":
            return self.prompts.get_structural_validation_prompt(
                formatted_framework,
                formatted_key_moves,
                literature,
                previous_outputs
            )
        else:
            raise ValueError(f"Unknown development phase: {development_phase}")
    
    def _process_llm_response(self, response: str) -> Dict[str, Any]:
        """Process the LLM response to extract outline content."""
        return {
            "core_content": response.strip(),
        }
        
    def process_output(self, raw_output: str) -> WorkerOutput:
        """Process the LLM response to extract outline content."""
        output_data = self._process_llm_response(raw_output)
        return WorkerOutput(
            status="completed",
            modifications=output_data,
            notes={}
        )
        
    def validate_output(self, output: WorkerOutput) -> bool:
        """Validate the worker output."""
        if not output.modifications or not output.modifications.get("core_content"):
            return False
        return True 