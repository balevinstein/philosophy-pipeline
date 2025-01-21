class WorkerError(Exception):
    """Base exception for worker-related errors"""
    pass

class WorkflowError(Exception):
    """Base exception for workflow-related errors"""
    pass

class ValidationError(WorkerError):
    """Raised when worker output validation fails"""
    pass

class StateError(WorkerError):
    """Raised when worker state is invalid"""
    pass