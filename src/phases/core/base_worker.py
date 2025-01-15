
### 1. Core Worker Architecture

```python
# src/phases/phase_two/core/base_worker.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class WorkerInput:
    context: Dict[str, Any]
    parameters: Dict[str, Any]

@dataclass 
class WorkerOutput:
    result: Dict[str, Any]
    metadata: Dict[str, Any]
    status: str

class BaseWorker(ABC):
    """Base class for all workers"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._state: Dict[str, Any] = {}
    
    @abstractmethod
    def execute(self, input_data: WorkerInput) -> WorkerOutput:
        """Main execution method"""
        pass
    
    @abstractmethod
    def validate_output(self, output: WorkerOutput) -> bool:
        """Validate worker output"""
        pass
    
    def get_state(self) -> Dict[str, Any]:
        """Get worker state"""
        return self._state.copy()
```