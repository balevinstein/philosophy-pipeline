from typing import Dict, Any, List
import logging
import json

from src.phases.core.worker_base import Worker
from src.phases.phase_two.stages.stage_six.prompts.planner_prompts import RevisionPlannerPrompts
from src.utils.api import APIHandler
from src.utils.json_utils import JSONHandler

class RevisionPlannerWorker(Worker):
    """
    A worker that takes a hostile review and creates a new, coherent writing plan.
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.prompts = RevisionPlannerPrompts()
        self.logger = logging.getLogger(__name__)
        self.api_handler = APIHandler(config)
        self.json_handler = JSONHandler()

    def _clean_control_characters(self, text: str) -> str:
        """Remove problematic control characters that can break JSON parsing."""
        import re
        # Remove control characters except for newlines, tabs, and carriage returns
        # which are handled by the JSON handler
        cleaned = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
        return cleaned

    def execute(
        self,
        enhanced_prompt: str,
        text_paths: List[str]
    ) -> tuple[Dict[str, Any], float]:
        """
        Executes the revision planning process using an enhanced prompt.

        Args:
            enhanced_prompt (str): The prompt enhanced with Analysis-style guidance.
            text_paths (List[str]): A list of paths to text file exemplars.

        Returns:
            tuple[Dict[str, Any], float]: The new, final writing plan as a JSON object and the API call duration.
        """
        self.logger.info("Executing Revision Planner Worker.")

        system_prompt = self.prompts.get_system_prompt()

        response_text, duration = self.api_handler.make_api_call(
            stage="phase_2_5_plan",
            prompt=enhanced_prompt,
            system_prompt=system_prompt,
            text_paths=text_paths
        )
        
        # Clean and parse the JSON response
        # First, remove control characters that commonly cause issues
        response_text = self._clean_control_characters(response_text)
        cleaned_response = self.json_handler.clean_json_string(response_text)
        parsed_response = json.loads(cleaned_response)

        self.logger.info("Revision Planner Worker completed.")
        return parsed_response, duration 