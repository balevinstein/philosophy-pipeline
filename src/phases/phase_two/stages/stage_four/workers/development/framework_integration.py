from typing import Dict, Any
from datetime import datetime
from pathlib import Path

from src.phases.core.base_worker import WorkerInput, WorkerOutput
from src.phases.core.worker_types import DevelopmentWorker
from src.phases.phase_two.stages.stage_four.prompts.development.framework_integration_prompts import (
    FrameworkIntegrationPrompt,
)
from src.phases.core.exceptions import ValidationError


class FrameworkIntegrationWorker(DevelopmentWorker):
    """
    Worker responsible for creating the foundational structure for a philosophical paper.
    
    This worker analyzes the abstract framework and key moves to create a logical
    section/subsection structure that properly accommodates all key moves, with
    explicit mapping of key moves to sections and appropriate word count allocations.
    
    Enhanced with Analysis PDF integration for structural guidance.
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.prompts = FrameworkIntegrationPrompt()
        self.stage_name = "framework_integration"
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
        
        print(f"📑 Including {len(selected_pdfs)} Analysis paper(s) for structural guidance:")
        for pdf in selected_pdfs:
            print(f"   • {pdf.name}")
        
        return selected_pdfs

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        """Construct the prompt for framework integration."""
        framework = input_data.context.get("framework", {})
        outline = input_data.context.get("outline", {})
        developed_key_moves = input_data.context.get("developed_key_moves", [])
        literature = input_data.context.get("literature", {})
        
        return self.prompts.get_prompt(
            framework=framework,
            initial_outline=outline,
            developed_key_moves=developed_key_moves,
            literature=literature,
        )

    def execute(self, state: Dict[str, Any]) -> WorkerOutput:
        """Execute with Analysis PDF support"""
        input_data = self.process_input(state)
        
        # Get system prompt if available
        system_prompt = self.get_system_prompt()
        
        # Construct prompt - PDFs already selected in process_input
        prompt = self._construct_prompt(input_data)
        
        # Make API call with Analysis PDFs if available
        if self.selected_analysis_pdfs:
            response, duration = self.api_handler.make_api_call(
                stage=self.stage_name,
                prompt=prompt,
                text_paths=self.selected_analysis_pdfs,
                system_prompt=system_prompt
            )
        else:
            response, duration = self.api_handler.make_api_call(
                stage=self.stage_name,
                prompt=prompt,
                system_prompt=system_prompt
            )
            
        output = self.process_output(response)
        if not self.validate_output(output):
            print(response)
            raise ValidationError("Worker output failed validation: ", self.stage_name)
        return output

    def process_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Prepare input for framework integration."""
        print("\nPreparing input for framework integration...")
        print("\nReceived state keys:", list(state.keys()))

        # Validate required inputs
        if "framework" not in state or "outline" not in state or "developed_key_moves" not in state:
            raise ValueError("Missing required state: framework, outline, developed_key_moves")
        
        # Select Analysis PDFs for structural guidance
        analysis_pdfs = self._get_analysis_pdfs(pdf_count=1)
        self.selected_analysis_pdfs = analysis_pdfs
        
        return WorkerInput(
            context={
                "framework": state["framework"],
                "outline": state["outline"],
                "developed_key_moves": state["developed_key_moves"],
                "literature": state.get("literature", {}),
            },
            parameters={
                "phase": "framework_integration",
            },
        )

    def process_output(self, raw_output: str) -> WorkerOutput:
        """Process the raw output from the worker."""
        print(f"\nProcessing framework integration output")
        
        # Extract the core content from the raw output
        core_content = raw_output.strip()
        
        # Attempt to split into sections if headings exist
        sections = {}
        current_section = None
        current_content = []
        section_markers = ["# ", "## "]  # Look for both H1 and H2 headings

        for line in raw_output.split("\n"):
            is_section_header = False
            for marker in section_markers:
                if line.startswith(marker):
                    if current_section:
                        sections[current_section] = "\n".join(current_content).strip()
                    current_section = line[len(marker):].strip()
                    current_content = []
                    is_section_header = True
                    break
            
            if not is_section_header and current_section is not None:
                current_content.append(line)

        if current_section:
            sections[current_section] = "\n".join(current_content).strip()
        
        # If we couldn't find any sections, use the entire content as one section
        if not sections:
            sections = {"Complete Outline Structure": core_content}
        
        # Create structured output
        modifications = {
            "core_content": core_content,
            "full_content": core_content,
            "timestamp": datetime.now().isoformat(),
            "sections": sections
        }
        
        # Create the worker output with the correct parameters
        output = WorkerOutput(
            modifications=modifications,
            notes={
                "section_count": len(sections)
            },
            status="completed"
        )
        
        return output

    def validate_output(self, output: WorkerOutput) -> bool:
        """Verify output meets requirements."""
        print("\nValidating framework integration output...")

        if not output.modifications:
            print("Failed: No modifications")
            return False

        content = output.modifications.get("core_content")
            
        if not content or not content.strip():
            print("Failed: No content")
            return False

        # Debug output
        print(f"\nOutput content (first 200 chars): {content[:200]}...")
        
        # Check for key structural elements
        required_elements = [
            # Check for section numbering
            lambda c: any(f"{i}." in c for i in range(1, 10)),
            # Check for key move references
            lambda c: "Key Move" in c or "key move" in c,
            # Check for word count allocations
            lambda c: any(kw in c.lower() for kw in ["word", "words", "count"])
        ]
        
        missing_elements = [i for i, check in enumerate(required_elements) if not check(content)]
        
        if missing_elements:
            print(f"Failed: Missing required elements {missing_elements}")
            return False
            
        # Check if we have sufficient content length
        if len(content.strip()) > 1000:  # Require at least 1000 characters for a complete structure
            print("Content length validation passed")
            return True
        else:
            print("Failed: Content too short")
            return False 