"""
Pipeline-specific exceptions
"""

class PipelineError(Exception):
    """Base exception for pipeline errors"""
    pass

class PhaseError(PipelineError):
    """Exception raised when a phase fails to execute"""
    def __init__(self, phase_id: str, message: str, original_error: Exception = None):
        self.phase_id = phase_id
        self.original_error = original_error
        super().__init__(f"Phase {phase_id} failed: {message}")

class DependencyError(PipelineError):
    """Exception raised when phase dependencies are not satisfied"""
    def __init__(self, phase_id: str, missing_dependencies: list):
        self.phase_id = phase_id
        self.missing_dependencies = missing_dependencies
        super().__init__(
            f"Phase {phase_id} has unsatisfied dependencies: {', '.join(missing_dependencies)}"
        )

class InvalidPhaseError(PipelineError):
    """Exception raised when an invalid phase ID is specified"""
    def __init__(self, phase_id: str, available_phases: list = None):
        self.phase_id = phase_id
        self.available_phases = available_phases or []
        message = f"Invalid phase ID: {phase_id}"
        if available_phases:
            message += f". Available phases: {', '.join(available_phases)}"
        super().__init__(message)

class ConfigurationError(PipelineError):
    """Exception raised when configuration is invalid"""
    pass