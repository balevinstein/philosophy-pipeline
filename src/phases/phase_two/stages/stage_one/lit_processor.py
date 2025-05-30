# src/stages/phase_two/stages/stage_one/lit_processor.py

from pathlib import Path
import json
import re
from typing import Dict, Any, List, Tuple
from src.utils.json_utils import JSONHandler
from ...base.worker import PhaseIIWorker, WorkerInput, WorkerOutput
from .prompts import InitialReadPrompts, ProjectSpecificPrompts, SynthesisPrompts


class InitialReader(PhaseIIWorker):
    """First read: Basic understanding and extraction with two-stage approach"""

    def __init__(self, config: Dict):
        super().__init__(config)
        self.prompts = InitialReadPrompts()
        self.json_handler = JSONHandler()

    def _construct_prompt(self, input_data: WorkerInput, stage: str = "full") -> str:
        """Construct prompt for initial paper reading"""
        if input_data.task_specific["status"] == "complete":
            return ""

        return self.prompts.get_prompt(
            paper_path=str(input_data.context["paper_path"]), 
            stage=stage
        )

    def prepare_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Prepare paper for initial reading"""
        paper_path = state["current_paper"]
        return WorkerInput(
            outline_state=state,
            context={"paper_path": paper_path},
            task_specific={"stage": "initial_read", "status": "processing"},
        )

    def process_output(self, response: str, stage: str = "full") -> WorkerOutput:
        """Process API response into structured output"""
        cleaned = self.json_handler.clean_json_string(response)
        content = json.loads(cleaned)

        # Handle both list and dictionary cases
        if isinstance(content, list):
            content = content[0] if content else {}

        if stage == "quotes":
            # For quote extraction stage, just return the quotes
            return WorkerOutput(
                modifications={"quotes": content.get("quotes", [])},
                notes={"quote_extraction_complete": True},
                status="quotes_extracted",
            )
        else:
            # For full analysis, return complete reading
            return WorkerOutput(
                modifications={"initial_reading": content},
                notes={
                    "paper_processed": content.get("paper_info", {}).get(
                        "title", "Unknown"
                    ),
                    "extraction_complete": True,
                },
                status="completed",
            )

    def run(self, state: Dict[str, Any]) -> WorkerOutput:
        """Execute two-stage initial reading with PDF"""
        input_data = self.prepare_input(state)
        
        # Stage 1: Extract quotes
        print("  Stage 1: Extracting key quotes...")
        quote_response = self.api_handler.make_api_call(
            stage="initialreader",
            prompt=self._construct_prompt(input_data, stage="quotes"),
            pdf_path=input_data.context["paper_path"],
            system_prompt=self.prompts.get_system_prompt()
        )
        quote_output = self.process_output(quote_response, stage="quotes")
        quotes = quote_output.modifications["quotes"]
        
        # Stage 2: Deep analysis using quotes
        print("  Stage 2: Conducting deep analysis...")
        # Format quotes for inclusion in the analysis prompt
        quotes_formatted = json.dumps(quotes, indent=2)
        analysis_prompt = self.prompts.get_prompt(
            paper_path=str(input_data.context["paper_path"]), 
            stage="analysis"
        ).replace("{quotes}", quotes_formatted)
        
        analysis_response = self.api_handler.make_api_call(
            stage="initialreader",
            prompt=analysis_prompt,
            pdf_path=input_data.context["paper_path"],
            system_prompt=self.prompts.get_system_prompt()
        )
        
        # Process the full analysis
        final_output = self.process_output(analysis_response, stage="full")
        
        # Add the extracted quotes to the final output
        if "initial_reading" in final_output.modifications:
            final_output.modifications["initial_reading"]["extracted_quotes"] = quotes
        
        return final_output


class ProjectSpecificReader(PhaseIIWorker):
    """Second read: Project-specific analysis"""

    def __init__(self, config: Dict):
        super().__init__(config)
        self.prompts = ProjectSpecificPrompts()
        self.json_handler = JSONHandler()

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        """Construct prompt for project-specific reading"""
        if input_data.task_specific["status"] == "complete":
            return ""

        return self.prompts.get_prompt(
            initial_reading=input_data.context["initial_reading"],
            final_selection=input_data.context["final_selection"],
        )

    def prepare_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Prepare for project-specific reading"""
        paper_path = state["current_paper"]
        initial_reading = state["initial_reading"].modifications["initial_reading"]
        final_selection = state["final_selection"]

        return WorkerInput(
            outline_state=state,
            context={
                "paper_path": paper_path,
                "initial_reading": initial_reading,
                "final_selection": final_selection,
            },
            task_specific={"stage": "project_specific", "status": "processing"},
        )

    def process_output(self, response: str) -> WorkerOutput:
        """Process API response into structured output"""
        cleaned = self.json_handler.clean_json_string(response)
        content = json.loads(cleaned)

        # Handle both list and dictionary cases
        if isinstance(content, list):
            content = content[0] if content else {}

        return WorkerOutput(
            modifications={"project_specific_reading": content},
            notes={
                "paper_processed": content.get("paper_info", {}).get(
                    "title", "Unknown"
                ),
                "engagement_type": content.get("engagement_assessment", {}).get(
                    "type", "Unknown"
                ),
            },
            status="completed",
        )

    def run(self, state: Dict[str, Any]) -> WorkerOutput:
        input_data = self.prepare_input(state)
        response = self.api_handler.make_api_call(
            stage="projectspecificreader", 
            prompt=self._construct_prompt(input_data),
            system_prompt=self.prompts.get_system_prompt()
        )
        return self.process_output(response)


class LiteratureSynthesizer(PhaseIIWorker):
    """Final stage: Synthesis across papers"""

    def __init__(self, config: Dict):
        super().__init__(config)
        self.prompts = SynthesisPrompts()
        self.json_handler = JSONHandler()

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        """Construct prompt for synthesis"""
        if input_data.task_specific["status"] == "complete":
            return ""

        return self.prompts.get_prompt(
            paper_readings=input_data.context["paper_readings"],
            final_selection=input_data.context["final_selection"],
        )

    def prepare_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Prepare for synthesis"""
        # Extract the actual readings from WorkerOutput objects
        paper_readings = {
            paper_id: {
                "initial": reading["initial"].modifications["initial_reading"],
                "project_specific": reading["project_specific"].modifications[
                    "project_specific_reading"
                ],
            }
            for paper_id, reading in state["paper_readings"].items()
        }

        return WorkerInput(
            outline_state=state,
            context={
                "paper_readings": paper_readings,
                "final_selection": state["final_selection"],
            },
            task_specific={"stage": "synthesis", "status": "processing"},
        )

    def process_output(self, response: str) -> WorkerOutput:
        """Process hybrid JSON/Markdown output"""
        try:
            # Split JSON and Markdown sections
            json_str, markdown_str = self._split_response(response)

            # Process JSON portion
            cleaned_json = self.json_handler.clean_json_string(json_str)
            content = json.loads(cleaned_json)

            # Handle list case
            if isinstance(content, list):
                content = content[0] if content else {}

            # More robust dictionary access
            structured_data = content.get("literature_overview", {})

            return WorkerOutput(
                modifications={
                    "literature_synthesis": {
                        "structured_data": content,
                        "narrative_analysis": markdown_str,
                    }
                },
                notes={
                    "papers_processed": len(structured_data.get("primary_papers", [])),
                    "synthesis_complete": True,
                },
                status="completed",
            )

        except Exception as e:
            print(f"Error processing synthesis output: {str(e)}")
            raise

    def _split_response(self, response: str) -> Tuple[str, str]:
        """Split response into JSON and Markdown portions"""
        # Look for the markdown output tag
        md_tag_start = response.find("<markdown_output>")
        if md_tag_start != -1:
            # Split at the markdown tag
            json_portion = response[:md_tag_start]
            md_portion = response[md_tag_start:]
            
            # Clean up the markdown portion
            md_portion = md_portion.replace("<markdown_output>", "")
            md_portion = md_portion.replace("</markdown_output>", "")
            
            # Extract JSON from its tags if present
            json_start = json_portion.find("{")
            if json_start == -1:
                raise ValueError("Could not find JSON content")
            json_text = json_portion[json_start:]
            
            # Find the last closing brace
            json_end = json_text.rfind("}")
            if json_end != -1:
                json_text = json_text[:json_end+1]
                
            return json_text.strip(), md_portion.strip()
        else:
            # Fallback to original method
            md_start = response.find("## ")
            if md_start == -1:
                json_start = response.find("{")
                if json_start == -1:
                    raise ValueError("Could not find JSON content")
                return response[json_start:], ""
            
            json_text = response[:md_start]
            json_start = json_text.find("{")
            if json_start == -1:
                raise ValueError("Could not find JSON content")
            json_text = json_text[json_start:]
            
            markdown_text = response[md_start:].strip()
            return json_text, markdown_text

    def _clean_markdown(self, markdown: str) -> str:
        """Basic markdown cleaning"""
        # Remove any front matter
        if markdown.startswith("---"):
            _, markdown = markdown.split("---", 2)[1:]

        # Ensure proper line breaks between sections
        markdown = re.sub(r"\n{3,}", "\n\n", markdown)

        return markdown.strip()

    def run(self, state: Dict[str, Any]) -> WorkerOutput:
        input_data = self.prepare_input(state)
        response = self.api_handler.make_api_call(
            stage="literaturesynthesizer", 
            prompt=self._construct_prompt(input_data),
            system_prompt=self.prompts.get_system_prompt()
        )
        return self.process_output(response)


class LiteratureManager:
    """Manages the complete literature processing workflow"""

    def __init__(self, config: Dict):
        self.config = config
        self.initial_reader = InitialReader(config)
        self.project_reader = ProjectSpecificReader(config)
        self.synthesizer = LiteratureSynthesizer(config)

    def process_papers(
        self, papers: List[Path], final_selection: Dict
    ) -> Dict[str, Any]:
        """Process all papers through all stages"""
        state = {"final_selection": final_selection, "paper_readings": {}}

        # First pass: Initial reading of all papers
        print("\n=== Stage 1: Initial Reading ===")
        for i, paper in enumerate(papers):
            print(f"\nProcessing paper {i+1}/{len(papers)}: {paper.name}")
            state["current_paper"] = paper
            reading = self.initial_reader.run(state)
            state["paper_readings"][paper.stem] = {"initial": reading}

        # Second pass: Project-specific reading
        print("\n=== Stage 2: Project-Specific Analysis ===")
        for i, paper in enumerate(papers):
            print(f"\nAnalyzing paper {i+1}/{len(papers)}: {paper.name}")
            state["current_paper"] = paper
            state["initial_reading"] = state["paper_readings"][paper.stem]["initial"]
            reading = self.project_reader.run(state)
            state["paper_readings"][paper.stem]["project_specific"] = reading

        # Final synthesis
        print("\n=== Stage 3: Literature Synthesis ===")
        synthesis = self.synthesizer.run(state)
        state["synthesis"] = synthesis

        return state
