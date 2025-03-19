from typing import Dict, Any, List, Optional
import os
from pathlib import Path

class BaseWorkflow:
    """
    Base class for workflows that manage multiple phases of a process.
    
    This is a higher-level abstraction than the Workflow class, designed for
    complex multi-phase workflows that need to track state across phases.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the workflow with configuration."""
        self.config = config
        self.name = "base_workflow"
        self.description = "Base workflow"
        
    def execute(self, input_data: Dict[str, Any]) -> Any:
        """
        Execute the workflow.
        
        Args:
            input_data: The input data for the workflow
            
        Returns:
            The output of the workflow
        """
        raise NotImplementedError("Subclasses must implement execute()")
    
    def _validate_input(self, input_data: Dict[str, Any]) -> None:
        """
        Validate the input data.
        
        Args:
            input_data: The input data to validate
            
        Raises:
            ValueError: If the input data is invalid
        """
        raise NotImplementedError("Subclasses must implement _validate_input()") 