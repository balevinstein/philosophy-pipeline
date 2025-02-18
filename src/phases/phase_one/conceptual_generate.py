# src/stages/conceptual_generate.py
import json
from typing import List, Dict, Any

from src.phases.phase_one.prompts.conceptual_generate import TopicGenerationPrompt
from .base import BaseStage


class ConceptualTopicGenerator(BaseStage):
    """Stage for generating conceptually-focused paper topics"""

    def __init__(self):
        super().__init__()
        self.config = self.api_handler.config
        self.num_topics = self.config["parameters"]["num_initial_topics"]
        self.prompt_manager = TopicGenerationPrompt()

    def _get_generation_prompt(self) -> str:
        """Get the prompt for conceptual topic generation"""
        return self.prompt_manager.get_prompt(self.num_topics)

    def run(self) -> List[Dict[str, Any]]:
        """Run the conceptual topic generation stage"""
        try:
            # Get response from API
            response_text = self.api_handler.make_api_call(
                stage="idea_generation", prompt=self._get_generation_prompt()
            )

            # Clean and parse response
            cleaned_content = self.json_handler.clean_json_string(response_text)
            topics = json.loads(cleaned_content)

            # Ensure we have a list
            if not isinstance(topics, list):
                topics = list(topics.values())

            # Print summary
            print(f"\nGenerated {len(topics)} topics:")
            for topic in topics:
                print(f"\n- {topic['title']}")
                print(
                    f"  Core contribution: {topic['core_contribution']['conceptual_issue'][:100]}..."
                )

            # Save results
            self.save_stage_output(topics)

            return topics

        except Exception as e:
            print(f"An error occurred during conceptual topic generation: {e}")
            return None

    def save_stage_output(self, topics: List[Dict[str, Any]]) -> None:
        """Save generated topics to file"""
        try:
            self.json_handler.save_json(
                topics, self.config["paths"]["generated_topics"]
            )
            print(f"\nResults saved to {self.config['paths']['generated_topics']}")
        except Exception as e:
            print(f"Error saving results: {e}")


if __name__ == "__main__":
    generator = ConceptualTopicGenerator()
    # generator.run()
