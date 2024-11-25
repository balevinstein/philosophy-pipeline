# src/stages/evaluate.py

import json
from typing import Dict, Any
from .base import BaseStage
from ..prompts.evaluate import TopicEvaluationPrompt

class TopicEvaluator(BaseStage):
    """Stage for evaluating and culling generated topics"""
    
    def __init__(self):
        super().__init__()
        self.config = self.api_handler.config
        self.prompt_manager = TopicEvaluationPrompt()

    def load_stage_input(self) -> Dict[str, Any]:
        """Load generated topics"""
        return self.json_handler.load_json(self.config['paths']['generated_topics'])

    def _get_evaluation_prompt(self, topics: Dict[str, Any]) -> str:
        """Get the evaluation prompt with topics"""
        topics_json = json.dumps(topics, indent=4)
        return self.prompt_manager.get_prompt(topics_json)

    def run(self) -> Dict[str, Any]:
        """Run the evaluation stage with enhanced diagnostics"""
        try:
            topics = self.load_stage_input()
            print(f"\nProcessing {len(topics)} topics...")
            
            response_text = self.api_handler.make_api_call(
                stage='initial_critique',
                prompt=self._get_evaluation_prompt(topics)
            )
            print("\nAPI call successful, processing response...")
            
            cleaned_content = self.json_handler.clean_json_string(response_text)
            evaluation_result = json.loads(cleaned_content)
            print("\nJSON parsing successful.")
            
            self.save_stage_output(evaluation_result)
            
            # Results summary
            cats = evaluation_result['categorized_topics']
            print("\nEvaluation Summary:")
            for category in ['develop', 'possible', 'reject']:
                print(f"{category.title()}: {len(cats[category])} topics")
                for topic in cats[category]:
                    print(f"  - {topic['title']}")
            
            return evaluation_result
                
        except Exception as e:
            print(f"\nError details:\nType: {type(e)}\nMessage: {str(e)}")
            return None

    def save_stage_output(self, evaluation_result: Dict[str, Any]) -> None:
        """Save evaluation results"""
        try:
            self.json_handler.save_json(
                evaluation_result,
                self.config['paths']['topics_culled']
            )
            print(f"\nResults saved to {self.config['paths']['topics_culled']}")
        except Exception as e:
            print(f"Error saving results: {e}")

if __name__ == "__main__":
    evaluator = TopicEvaluator()
    results = evaluator.run()