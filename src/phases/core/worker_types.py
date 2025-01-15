
### 2. Worker Types

```python
# src/phases/phase_two/core/worker_types.py

from .base_worker import BaseWorker, WorkerInput, WorkerOutput

class DevelopmentWorker(BaseWorker):
    """For content development tasks"""
    worker_type = "development"
    
    def execute(self, input_data: WorkerInput) -> WorkerOutput:
        # Development-specific implementation
        pass

class CriticWorker(BaseWorker):
    """For evaluation tasks"""
    worker_type = "critic"
    
    def execute(self, input_data: WorkerInput) -> WorkerOutput:
        # Critic-specific implementation
        pass

class RefinementWorker(BaseWorker):
    """For refinement tasks"""
    worker_type = "refinement"
    
    def execute(self, input_data: WorkerInput) -> WorkerOutput:
        # Refinement-specific implementation
        pass
```