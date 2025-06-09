from typing import Dict, Any

class Worker:
    """Base class for all workers in the philosophy pipeline."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initializes the Worker with a configuration dictionary.

        Args:
            config (Dict[str, Any]): The configuration for the worker.
        """
        self.config = config

    def execute(self, *args, **kwargs) -> Any:
        """
        The main execution method for the worker.
        This method should be overridden by subclasses.
        """
        raise NotImplementedError("Each worker must implement an execute method.") 