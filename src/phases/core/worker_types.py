from .base_worker import BaseWorker


class DevelopmentWorker(BaseWorker):
    """For content development tasks"""

    worker_type = "development"


class CriticWorker(BaseWorker):
    """For critiquing tasks"""

    worker_type = "critic"

    def _extract_summary(self, summary_text: str) -> str:
        """Extract summary assessment from text"""
        for assessment in ["MAJOR REVISION", "MINOR REFINEMENT", "MINIMAL CHANGES"]:
            if assessment in summary_text:
                return assessment
        return "UNKNOWN"


class RefinementWorker(BaseWorker):
    """For refinement tasks"""

    worker_type = "refinement"
