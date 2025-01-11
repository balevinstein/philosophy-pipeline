from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass
from .worker import PhaseIIWorker, WorkerInput, WorkerOutput

class WorkerError(Exception):
    """Base class for framework worker errors"""
    pass

class ValidationError(WorkerError):
    """Raised when worker output fails validation"""
    pass

class StateError(WorkerError):
    """Raised when worker state is invalid"""
    pass

class FrameworkWorker(PhaseIIWorker):
    """Enhanced base class for complex Phase II workers"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self._state: Dict[str, Any] = {}
    
    @abstractmethod
    def validate_output(self, output: WorkerOutput) -> bool:
        """Required output validation"""
        pass
    
    @abstractmethod
    def get_state(self) -> Dict[str, Any]:
        """Required state management"""
        pass
    
    def update_state(self, new_state: Dict[str, Any]):
        """Update worker state"""
        self._state.update(new_state)
    
    def run(self, state: Dict[str, Any]) -> WorkerOutput:
        """Enhanced run with validation"""
        output = super().run(state)
        if not self.validate_output(output):
            raise ValidationError("Worker output failed validation")
        return output


class CriticWorker(FrameworkWorker):
    """Base class for critics"""
    
    @abstractmethod
    def evaluate(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate provided content"""
        pass
        
    def prepare_input(self, state: Dict[str, Any]) -> WorkerInput:
        """Prepare critic-specific input"""
        return WorkerInput(
            outline_state=state,
            context=self.get_state(),
            task_specific={"type": "evaluation"}
        )

class SynthesisWorker(FrameworkWorker):
    """Base class for synthesis/integration workers"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self._abstract: Optional[Dict[str, Any]] = None
    
    @property
    def abstract(self) -> Dict[str, Any]:
        """Get current abstract"""
        if self._abstract is None:
            raise StateError("Abstract not initialized")
        return self._abstract
    
    @abstract.setter
    def abstract(self, value: Dict[str, Any]):
        """Set abstract with validation"""
        if not self._validate_abstract(value):
            raise ValidationError("Invalid abstract format")
        self._abstract = value
    
    @abstractmethod
    def _validate_abstract(self, abstract: Dict[str, Any]) -> bool:
        """Validate abstract format"""
        pass