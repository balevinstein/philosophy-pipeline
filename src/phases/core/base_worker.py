from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional

from src.phases.phase_two.base.framework import ValidationError
from src.utils.api import APIHandler


@dataclass
class WorkerInput:
    context: Dict[str, Any]  # Context needed for prompt construction and LLM calls
    parameters: Dict[str, Any]  # Execution based details

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class WorkerOutput:
    status: str  # Status of the worker
    modifications: Dict[str, Any]  # Proposed changes to outline
    notes: Dict[str, Any]  # Worker's observations/suggestions

    def __getitem__(self, item):
        return getattr(self, item)


class BaseWorker(ABC):
    """Base class for all workers"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._state: Dict[str, Any] = {}
        self.api_handler = APIHandler(config)
        self.stage_name = str

    def get_state(self) -> Dict[str, Any]:
        """Get worker state"""
        return self._state.copy()

    @abstractmethod
    def _construct_prompt(self, input_data: WorkerInput) -> str:
        """Construct the prompt for the worker"""
        pass

    # map input
    @abstractmethod
    def process_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Map the input data to worker input"""
        pass

    @abstractmethod
    def process_output(self, response: str) -> WorkerOutput:
        """Map the output data to worker output"""
        pass

    @abstractmethod
    def validate_output(self, output: WorkerOutput) -> bool:
        """Validate worker output"""
        pass
        
    def get_system_prompt(self) -> Optional[str]:
        """Get system prompt if the worker has associated prompts with get_system_prompt method"""
        # Check if the worker has a prompts attribute with get_system_prompt method
        if hasattr(self, 'prompts') and hasattr(self.prompts, 'get_system_prompt'):
            return self.prompts.get_system_prompt()
        return None

    def execute(self, state: Dict[str, Any]) -> WorkerOutput:
        """Main execution method"""
        input_data = self.process_input(state)
        
        # Get system prompt if available
        system_prompt = self.get_system_prompt()
        
        response = self.api_handler.make_api_call(
            stage=self.stage_name, 
            prompt=self._construct_prompt(input_data),
            system_prompt=system_prompt
        )
        output = self.process_output(response)
        if not self.validate_output(output):
            print(response)
            raise ValidationError("Worker output failed validation: ", self.stage_name)
        return output
