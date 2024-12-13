# src/stages/conceptual_evaluate.py

import json
from typing import Dict, Any, Optional
from .base import BaseStage
from ..prompts.conceptual_evaluate import TopicEvaluationPrompt

class ConceptualTopicEvaluator(BaseStage):
    """Stage for evaluating and culling generated philosophy paper topics"""
    
    def __init__(self):
        super().__init__()
        self.cull_min = self.config['parameters']['cull_min']
        self.cull_max = self.config['parameters']['cull_max']
        self.prompt_manager = TopicEvaluationPrompt(
            cull_min=self.cull_min,
            cull_max=self.cull_max
        )

    def _validate_selection_count(self, result: Dict[str, Any]) -> None:
        """Validate only the evaluation-specific requirements"""
        selected = result['selection_decision']['selected_topics']
        if not (self.cull_min <= len(selected) <= self.cull_max):
            raise ValueError(
                f"Selected topics count {len(selected)} outside bounds "
                f"({self.cull_min}-{self.cull_max})"
            )

    def _print_evaluation_summary(self, result: Dict[str, Any]) -> None:
        """Print human-readable summary of evaluation results"""
        print("\nEvaluation Summary:")
        
        print("\nSelected Topics (ranked):")
        selected = result['selection_decision']['selected_topics']
        for topic in sorted(selected, key=lambda x: x['rank']):
            print(f"\n{topic['rank']}. {topic['title']}")
            print(f"Rationale: {topic['selection_rationale']}")
            print("Comparative Advantages:")
            for adv in topic['comparative_advantages']:
                print(f"- {adv}")

        print("\nRejected Topics:")
        for topic in result['selection_decision']['rejected_topics']:
            print(f"\n- {topic['title']}")
            print(f"Rationale: {topic['rejection_rationale']}")

        print("\nNext Stage Guidance:")
        for priority in result['stage_guidance']['development_priorities']:
            print(f"- {priority}")

    def run(self) -> Optional[Dict[str, Any]]:
        """Run the evaluation stage"""
        # Load input (json_utils handles file operations and parsing)
        topics = self.json_handler.load_json(
            self.get_full_path('generated_topics')
        )
        print(f"\nEvaluating {len(topics)} topics...")
        
        # Make API call
        prompt = self.prompt_manager.get_prompt(json.dumps(topics, indent=2))
        response = self.api_handler.make_api_call(
            stage='topic_evaluation',
            prompt=prompt
        )
        
        # Parse and validate (json_utils handles JSON validation)
        result = json.loads(
            self.json_handler.clean_json_string(response)
        )
        
        # Only validate our specific requirements
        self._validate_selection_count(result)
        
        # Save and summarize
        self.json_handler.save_json(
            result,
            self.get_full_path('topics_culled')
        )
        self._print_evaluation_summary(result)
        
        return result

if __name__ == "__main__":
    evaluator = ConceptualTopicEvaluator()
    evaluator.run()