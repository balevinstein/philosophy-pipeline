# src/stages/base.py
from typing import Dict, Any
import os
from ..utils.api import APIHandler
from ..utils.json_utils import JSONHandler

class BaseStage:
    def __init__(self):
        self.api_handler = APIHandler()
        self.json_handler = JSONHandler()
        self.config = self.api_handler.config
        print("\nDebug: Configuration loaded")
        print(f"Debug: Paths config: {self.config['paths']}")
        
    def get_full_path(self, path_key: str) -> str:
        """Constructs full path by combining base_dir with relative path"""
        base_dir = self.config['paths']['base_dir']
        relative_path = self.config['paths'][path_key]
        full_path = os.path.join(os.getcwd(), base_dir.strip('./'), relative_path)
        print(f"\nDebug: Constructing path for {path_key}")
        print(f"Debug: base_dir: {base_dir}")
        print(f"Debug: relative_path: {relative_path}")
        print(f"Debug: full_path: {full_path}")
        return full_path
        
    def load_stage_input(self) -> Dict[str, Any]:
        """Load input for this stage. Override in subclasses."""
        raise NotImplementedError
        
    def run(self) -> Dict[str, Any]:
        """Run this stage. Override in subclasses."""
        raise NotImplementedError
        
    def save_stage_output(self, output: Dict[str, Any]) -> None:
        """Save output from this stage. Override in subclasses."""
        raise NotImplementedError