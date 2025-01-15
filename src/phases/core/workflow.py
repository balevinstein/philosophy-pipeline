
### 3. Workflow System

```python
# src/phases/phase_two/core/workflow.py

from dataclasses import dataclass
from typing import List, Dict, Any
from .base_worker import BaseWorker, WorkerInput, WorkerOutput

@dataclass
class WorkflowStep:
    worker: BaseWorker
    input_mapping: Dict[str, str]  # Maps workflow state to worker input
    output_mapping: Dict[str, str] # Maps worker output to workflow state

class Workflow:
    """Manages execution of multiple workers"""
    
    def __init__(self, steps: List[WorkflowStep]):
        self.steps = steps
        self.state: Dict[str, Any] = {}
    
    def execute(self, initial_state: Dict[str, Any]) -> Dict[str, Any]:
        self.state = initial_state.copy()
        
        for step in self.steps:
            # Map workflow state to worker input
            input_data = WorkerInput(
                context=self._map_state(step.input_mapping),
                parameters={}
            )
            
            # Execute worker
            output = step.worker.execute(input_data)
            
            # Update workflow state with worker output
            self._update_state(step.output_mapping, output)
            
        return self.state
```