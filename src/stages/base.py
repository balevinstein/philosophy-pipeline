# src/stages/base.py
from typing import Dict, Any
from ..utils.api import APIHandler
from ..utils.json_utils import JSONHandler

class BaseStage:
    def __init__(self):
        self.api_handler = APIHandler()
        self.json_handler = JSONHandler()
        
    def load_stage_input(self) -> Dict[str, Any]:
        """Load input for this stage. Override in subclasses."""
        raise NotImplementedError
        
    def run(self) -> Dict[str, Any]:
        """Run this stage. Override in subclasses."""
        raise NotImplementedError
        
    def save_stage_output(self, output: Dict[str, Any]) -> None:
        """Save output from this stage. Override in subclasses."""
        raise NotImplementedError