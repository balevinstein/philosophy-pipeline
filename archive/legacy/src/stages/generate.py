# src/stages/generate.py
import json
from typing import List, Dict, Any
from .base import BaseStage
from ..prompts.generate import TopicGenerationPrompt

class TopicGenerator(BaseStage):
    """Stage for generating initial paper topics"""
    
    def __init__(self):
        super().__init__()
        self.config = self.api_handler.config
        self.num_topics = self.config['parameters']['num_initial_topics']
        self.prompt_manager = TopicGenerationPrompt()

    def _get_generation_prompt(self) -> str:
        """Get the prompt for topic generation"""
        return self.prompt_manager.get_prompt(self.num_topics)

    def convert_to_array(self, topics_obj: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Convert numbered topics to array if needed"""
        if isinstance(topics_obj, list):
            return topics_obj
        
        topics_array = []
        i = 1
        while f"topic{i}" in topics_obj:
            topics_array.append(topics_obj[f"topic{i}"])
            i += 1
        return topics_array

    def run(self) -> List[Dict[str, Any]]:
        """Run the topic generation stage"""
        try:
            # Get response from API
            response_text = self.api_handler.make_api_call(
                stage='idea_generation',
                prompt=self._get_generation_prompt()
            )
            
            # Clean and parse response
            cleaned_content = self.json_handler.clean_json_string(response_text)
            topics = json.loads(cleaned_content)
            topics_array = self.convert_to_array(topics)
            
            # Print summary
            print(f"\nSuccessfully generated {len(topics_array)} topics")
            
            # Save results
            self.save_stage_output(topics_array)
            
            return topics_array
            
        except Exception as e:
            print(f"An error occurred during topic generation: {e}")
            return None

    def save_stage_output(self, topics: List[Dict[str, Any]]) -> None:
        """Save generated topics to file"""
        try:
            self.json_handler.save_json(
                topics,
                self.config['paths']['generated_topics']
            )
            print(f"\nResults saved to {self.config['paths']['generated_topics']}")
        except Exception as e:
            print(f"Error saving results: {e}")

if __name__ == "__main__":
    generator = TopicGenerator()
    topics = generator.run()