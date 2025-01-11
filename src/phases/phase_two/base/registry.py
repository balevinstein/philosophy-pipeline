from typing import Type, Dict, List
from abc import ABC, abstractmethod

class WorkerRegistry:
    """Central registry for worker types"""
    _workers: Dict[str, Type['PhaseIIWorker']] = {}
    
    @classmethod
    def register(cls, worker_type: str):
        """Decorator to register a worker class"""
        def inner(worker_class: Type['PhaseIIWorker']):
            cls._workers[worker_type] = worker_class
            return worker_class
        return inner
    
    @classmethod
    def get_worker(cls, worker_type: str) -> Type['PhaseIIWorker']:
        """Get worker class by type"""
        return cls._workers.get(worker_type)
        
    @classmethod
    def list_workers(cls) -> List[str]:
        """List all registered worker types"""
        return list(cls._workers.keys())

class PhaseIIWorker(ABC):
    """Enhanced base class for workers"""
    
    @abstractmethod
    def get_required_inputs(self) -> Dict[str, str]:
        """Declare what inputs this worker needs"""
        pass
        
    @abstractmethod
    def get_provided_outputs(self) -> Dict[str, str]:
        """Declare what outputs this worker produces"""
        pass
    
    @abstractmethod
    def validate_inputs(self, inputs: Dict) -> bool:
        """Verify this worker has what it needs"""
        pass

# Example worker registration
@WorkerRegistry.register("iff_definition")
class IffDefinitionWorker(PhaseIIWorker):
    def get_required_inputs(self):
        return {
            "concept": "Term being defined",
            "context": "Relevant philosophical context"
        }
    
    def get_provided_outputs(self):
        return {
            "definition": "Formal iff definition",
            "clarifications": "Term clarifications"
        }

class StageManager:
    """Manages worker configuration for a stage"""
    
    def __init__(self, config: Dict):
        self.worker_sequence = self._build_sequence(config)
        
    def _build_sequence(self, config: Dict) -> List[PhaseIIWorker]:
        """Build worker sequence from configuration"""
        sequence = []
        for worker_config in config['workers']:
            worker_class = WorkerRegistry.get_worker(worker_config['type'])
            if worker_class:
                worker = worker_class(worker_config.get('config', {}))
                sequence.append(worker)
        return sequence
    
    def validate_workflow(self) -> bool:
        """Verify all workers' input needs are met"""
        available_outputs = set()
        for worker in self.worker_sequence:
            required = set(worker.get_required_inputs().keys())
            if not required.issubset(available_outputs):
                missing = required - available_outputs
                raise ValueError(f"Worker {worker.__class__.__name__} missing inputs: {missing}")
            available_outputs.update(worker.get_provided_outputs().keys())
        return True