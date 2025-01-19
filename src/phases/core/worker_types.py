from abc import abstractmethod
from .base_worker import BaseWorker


class DevelopmentWorker(BaseWorker):
    """For content development tasks"""

    worker_type = "development"


class CriticWorker(BaseWorker):
    """For critiquing tasks"""

    worker_type = "critic"

    @abstractmethod
    def extract_summary(self, summary_text: str) -> str:
        """Extract the summary from response"""

    # This is just run with validate output
    # @abstractmethod
    # def evaluate(self, content: Dict[str, Any]) -> Dict[str, Any]:
    #     """Extract the summary from response"""
    #     pass
    # if not self.validate_output(output):
    #         raise ValidationError("Worker output failed validation")
    #     return output


class RefinementWorker(BaseWorker):
    """For refinement tasks"""

    worker_type = "refinement"
