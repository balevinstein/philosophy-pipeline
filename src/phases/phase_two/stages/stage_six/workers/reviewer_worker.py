from typing import Dict, Any, List
import logging
import json

from src.phases.core.worker_base import Worker
from src.phases.phase_two.stages.stage_six.prompts.reviewer_prompts import DialecticalReviewerPrompts
from src.utils.api import APIHandler
from src.utils.json_utils import JSONHandler

class DialecticalReviewerWorker(Worker):
    """
    A worker that acts as a hostile referee to review the entire paper plan.
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.prompts = DialecticalReviewerPrompts()
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
        Executes the dialectical review of the paper plan using an enhanced prompt.

        Args:
            enhanced_prompt (str): The prompt enhanced with Analysis-style guidance.
            text_paths (List[str]): A list of paths to text file exemplars.

        Returns:
            tuple[Dict[str, Any], float]: The referee report as a JSON object and the API call duration.
        """
        self.logger.info("Executing Dialectical Reviewer Worker.")
        
        system_prompt = self.prompts.get_system_prompt()

        response_text, duration = self.api_handler.make_api_call(
            stage="phase_2_5_review",
            prompt=enhanced_prompt,
            system_prompt=system_prompt,
            text_paths=text_paths
        )
        
        # Clean and parse the JSON response
        # First, remove control characters that commonly cause issues
        response_text = self._clean_control_characters(response_text)
        cleaned_response = self.json_handler.clean_json_string(response_text)
        parsed_response = json.loads(cleaned_response)
        
        self.logger.info("Dialectical Reviewer Worker completed.")
        return parsed_response, duration 