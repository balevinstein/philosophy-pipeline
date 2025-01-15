from typing import Dict, Any
from ....core.worker_types import DevelopmentWorker
from ....core.base_worker import WorkerInput, WorkerOutput
from ....prompts.abstract_prompts import AbstractPrompts

class AbstractDevelopmentWorker(DevelopmentWorker):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.prompts = AbstractPrompts()
        self._state = {
            "iterations": 0,
            "current_abstract": None
        }

    def _construct_prompt(self, input_data: WorkerInput) -> str:
        return self.prompts.get_development_prompt(
            lit_readings=input_data.context["literature"]["readings"],
            lit_synthesis=input_data.context["literature"]["synthesis"],
            lit_narrative=input_data.context["literature"]["narrative"],
            final_selection=input_data.context["final_selection"]
        )

    def _process_response(self, response: str) -> WorkerOutput:
        try:
            parsed = json.loads(response)
            self._state["iterations"] += 1
            self._state["current_abstract"] = parsed
            
            return WorkerOutput(
                result=parsed,
                metadata={
                    "iteration": self._state["iterations"],
                },
                status="completed"
            )
        except json.JSONDecodeError as e:
            return WorkerOutput(
                result={},
                metadata={"error": str(e)},
                status="failed"
            )

    def validate_output(self, output: WorkerOutput) -> bool:
        if output.status == "failed":
            return False
            
        required_fields = ["abstract", "framework"]
        return all(field in output.result for field in required_fields)