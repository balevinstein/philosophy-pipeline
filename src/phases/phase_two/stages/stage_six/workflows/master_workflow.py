import logging
import os
import json
from typing import Dict, Any
from pathlib import Path

# We will create these utils later
# from src.utils.general import load_json_file, save_json_file, load_text_file

from src.utils.json_utils import JSONHandler
from src.utils.file_utils import load_text_file
from src.utils.analysis_pdf_utils import enhance_development_prompt
from src.phases.phase_two.stages.stage_six.workers.reviewer_worker import DialecticalReviewerWorker
from src.phases.phase_two.stages.stage_six.workers.planner_worker import RevisionPlannerWorker

class PaperVisionReviewWorkflow:
    """
    Orchestrates the Paper Vision Review stage (Phase II.5), running the
    Dialectical Reviewer and the Revision Planner to produce a final,
    coherent writing plan.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.json_handler = JSONHandler()
        self.reviewer_worker = DialecticalReviewerWorker(config)
        self.planner_worker = RevisionPlannerWorker(config)

    def run(self) -> Dict[str, Any]:
        """
        Executes the full Paper Vision Review workflow.

        Returns:
            Dict[str, Any]: The final, coherent writing plan.
        """
        self.logger.info("Starting Paper Vision Review Workflow (Phase II.5).")

        # 1. Load inputs
        self.logger.info("Loading inputs for review.")
        
        # Use the current working directory as the project root.
        # This is more robust for scripts run from the project's base directory.
        project_root = Path.cwd()
        
        developed_moves_path = project_root / "outputs" / "key_moves_development" / "key_moves_development" / "all_developed_moves.json"
        detailed_outline_path = project_root / "outputs" / "detailed_outline" / "detailed_outline_final.md"
        abstract_framework_path = project_root / "outputs" / "framework_development" / "abstract_framework.json"
        injectable_examples_path = project_root / "outputs" / "curated_moves" / "injectable_examples.json"

        with open(developed_moves_path, 'r', encoding='utf-8') as f:
            developed_moves = json.load(f)
            
        detailed_outline = load_text_file(detailed_outline_path)

        with open(abstract_framework_path, 'r', encoding='utf-8') as f:
            abstract_framework = json.load(f)

        with open(injectable_examples_path, 'r', encoding='utf-8') as f:
            injectable_examples = json.load(f)

        main_thesis = abstract_framework.get("abstract_framework", {}).get("main_thesis", "Thesis not found.")
        core_contribution = abstract_framework.get("abstract_framework", {}).get("core_contribution", "Contribution not found.")

        # 2. Enhance prompt and run the Dialectical Reviewer
        self.logger.info("Enhancing prompts and running Dialectical Reviewer Worker.")
        
        base_review_prompt = self.reviewer_worker.prompts.get_review_prompt(
            detailed_outline,
            developed_moves,
            main_thesis,
            core_contribution,
            injectable_examples
        )

        # Enhance it with Analysis patterns
        enhanced_prompt, text_paths = enhance_development_prompt(
            base_review_prompt,
            phase="holistic review" # A new phase name for our stage
        )

        referee_report, reviewer_duration = self.reviewer_worker.execute(
            enhanced_prompt=enhanced_prompt,
            text_paths=text_paths
        )
        self.logger.info(f"Dialectical Reviewer completed in {reviewer_duration:.2f} seconds")

        # 3. Enhance prompt and run the Revision Planner
        self.logger.info("Enhancing prompts and running Revision Planner Worker.")

        base_planning_prompt = self.planner_worker.prompts.get_planning_prompt(
            detailed_outline,
            developed_moves,
            referee_report,
            injectable_examples
        )

        enhanced_planning_prompt, planner_text_paths = enhance_development_prompt(
            base_planning_prompt,
            phase="revision planning" # A new phase name
        )

        final_writing_plan, planner_duration = self.planner_worker.execute(
            enhanced_prompt=enhanced_planning_prompt,
            text_paths=planner_text_paths
        )
        self.logger.info(f"Revision Planner completed in {planner_duration:.2f} seconds")

        # 4. Save intermediate and final outputs
        output_dir = project_root / "outputs" / "paper_vision_review"
        os.makedirs(output_dir, exist_ok=True)
        
        # The json_handler's save_json expects a string path, so we convert the Path object
        self.json_handler.save_json(referee_report, str(output_dir / "referee_report.json"))
        self.json_handler.save_json(final_writing_plan, str(output_dir / "final_writing_plan.json"))
        
        print(f"Review artifacts saved to {output_dir}")

        self.logger.info("Paper Vision Review Workflow completed.")
        return final_writing_plan 

    def run_with_consolidated_context(self, consolidated_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the review workflow using consolidated context from Phase II.5.
        
        Args:
            consolidated_context: The consolidated context from Phase II.5
            
        Returns:
            Dict containing referee report and final writing plan
        """
        self.logger.info("Starting Paper Vision Review Workflow with consolidated context.")
        
        # Extract the raw outputs from consolidated context
        raw_outputs = consolidated_context.get("raw_outputs", {})
        
        # Extract necessary components
        developed_moves = raw_outputs.get("developed_moves", {}).get("developed_moves", [])
        detailed_outline_data = raw_outputs.get("detailed_outline", {})
        detailed_outline = detailed_outline_data.get("final_outline", "")
        abstract_framework = raw_outputs.get("abstract_framework", {}).get("abstract_framework", {})
        
        # Get main thesis and core contribution
        main_thesis = abstract_framework.get("main_thesis", "Thesis not found.")
        core_contribution = abstract_framework.get("core_contribution", "Contribution not found.")
        
        # Extract diagnostic analysis from consolidated context
        diagnostic_analysis = consolidated_context.get("diagnostic_analysis", {})
        
        # Load injectable examples
        project_root = Path.cwd()
        injectable_examples_path = project_root / "outputs" / "curated_moves" / "injectable_examples.json"
        
        try:
            with open(injectable_examples_path, 'r', encoding='utf-8') as f:
                injectable_examples = json.load(f)
        except FileNotFoundError:
            self.logger.warning("Injectable examples not found, using empty dict")
            injectable_examples = {}
        
        # Run the review workflow
        self.logger.info("Running Dialectical Reviewer Worker.")
        
        base_review_prompt = self.reviewer_worker.prompts.get_review_prompt(
            detailed_outline,
            developed_moves,
            main_thesis,
            core_contribution,
            injectable_examples,
            diagnostic_analysis  # Pass diagnostic analysis
        )
        
        # Enhance with Analysis patterns
        enhanced_prompt, text_paths = enhance_development_prompt(
            base_review_prompt,
            phase="holistic review"
        )
        
        referee_report, reviewer_duration = self.reviewer_worker.execute(
            enhanced_prompt=enhanced_prompt,
            text_paths=text_paths
        )
        self.logger.info(f"Dialectical Reviewer completed in {reviewer_duration:.2f} seconds")
        
        # Run the Revision Planner
        self.logger.info("Running Revision Planner Worker.")
        
        base_planning_prompt = self.planner_worker.prompts.get_planning_prompt(
            detailed_outline,
            developed_moves,
            referee_report,
            injectable_examples,
            diagnostic_analysis  # Pass diagnostic analysis
        )
        
        enhanced_planning_prompt, planner_text_paths = enhance_development_prompt(
            base_planning_prompt,
            phase="revision planning"
        )
        
        final_writing_plan, planner_duration = self.planner_worker.execute(
            enhanced_prompt=enhanced_planning_prompt,
            text_paths=planner_text_paths
        )
        self.logger.info(f"Revision Planner completed in {planner_duration:.2f} seconds")
        
        # Save outputs
        output_dir = project_root / "outputs" / "paper_vision_review"
        os.makedirs(output_dir, exist_ok=True)
        
        self.json_handler.save_json(referee_report, str(output_dir / "referee_report.json"))
        self.json_handler.save_json(final_writing_plan, str(output_dir / "final_writing_plan.json"))
        
        self.logger.info(f"Review artifacts saved to {output_dir}")
        
        return {
            "referee_report": referee_report,
            "final_writing_plan": final_writing_plan
        } 