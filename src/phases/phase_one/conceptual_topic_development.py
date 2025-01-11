# src/stages/conceptual_topic_development.py

import json
from typing import Dict, Any, List, Optional

from src.prompts.conceptual_topic_development import TopicDevelopmentPrompt
from .base import BaseStage


class ConceptualTopicDeveloper(BaseStage):
    """Stage for deeper development of promising philosophy paper topics"""
    
    def __init__(self):
        super().__init__()
        self.prompt_manager = TopicDevelopmentPrompt()

    def _process_single_topic(self, topic: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single topic through all development phases"""
        print(f"\nProcessing topic: {topic['title']}")
        
        try:
            # Literature assessment phase
            print("Starting literature assessment...")
            lit_prompt = self.prompt_manager.get_literature_prompt(topic)
            lit_response = self.api_handler.make_api_call(
                stage='literature_assessment',
                prompt=lit_prompt
            )
            lit_results = json.loads(
                self.json_handler.clean_json_string(lit_response)
            )
            
            # Development testing phase
            print("Starting development testing...")
            dev_prompt = self.prompt_manager.get_development_prompt(
                topic, lit_results
            )
            dev_response = self.api_handler.make_api_call(
                stage='development_testing',
                prompt=dev_prompt
            )
            dev_results = json.loads(
                self.json_handler.clean_json_string(dev_response)
            )
            
            # Refinement phase
            print("Starting refinement phase...")
            ref_prompt = self.prompt_manager.get_refinement_prompt(
                topic, lit_results, dev_results
            )
            ref_response = self.api_handler.make_api_call(
                stage='topic_refinement',
                prompt=ref_prompt
            )
            ref_results = json.loads(
                self.json_handler.clean_json_string(ref_response)
            )
            
            # Assemble results
            results = {
                "title": topic['title'],
                "literature": lit_results,
                "development_testing": dev_results,
                "refinements": ref_results
            }
            
            # Print development summary for this topic
            self._print_topic_summary(results)
            
            return results
            
        except Exception as e:
            print(f"Error processing topic '{topic['title']}': {str(e)}")
            raise

    def run(self) -> Dict[str, Any]:
        """Run the topic development stage"""
        try:
            # Load selected topics from previous stage
            prev_results = self.json_handler.load_json(
                self.config['paths']['topics_culled']
            )
            selected_topics = prev_results['selection_decision']['selected_topics']
            
            print(f"\nDeveloping {len(selected_topics)} topics...")
            
            # Process each topic
            results = {}
            for topic in selected_topics:
                results[topic['title']] = self._process_single_topic(topic)
            
            # Save results
            self.json_handler.save_json(
                results,
                self.config['paths']['topic_development']
            )
            
            return results
            
        except Exception as e:
            print(f"Error in topic development stage: {str(e)}")
            raise

    def _print_topic_summary(self, topic_results: Dict[str, Any]) -> None:
        """Print human-readable summary of topic development"""
        print(f"\nDevelopment Summary for: {topic_results['title']}")
        
        # Literature summary
        print("\nLiterature Assessment:")
        lit = topic_results['literature']
        print(f"Overall confidence: {lit['literature_confidence']['overall_rating']}")
        print("Key papers:")
        for paper in lit['key_papers']:
            print(f"- {paper['title']}")
            print(f"  Confidence: {paper['confidence']}")
            print(f"  Memory type: {paper['memory_type']}")
        
        # Development summary
        print("\nDevelopment Testing:")
        dev = topic_results['development_testing']
        print("Sample argument tested:")
        print(f"- Key move: {dev['sample_argument']['key_move']}")
        print("Example case:")
        print(f"- {dev['example_case']['description']}")
        print("Number of objections identified:", len(dev['potential_objections']))
        
        # Refinement summary
        print("\nRefinements:")
        ref = topic_results['refinements']
        print("Thesis development:")
        print(f"- {ref['sharpened_thesis']}")
        print("\nRemaining challenges:", len(ref['remaining_challenges']['conceptual_issues']))

if __name__ == "__main__":
    developer = ConceptualTopicDeveloper()
    results = developer.run()