# src/stages/conceptual_final_select.py

import json
from typing import Dict, Any, Optional

from src.prompts.conceptual_final_select import FinalSelectionPrompt
from .base import BaseStage


class FinalTopicSelector(BaseStage):
    """Stage for final topic selection and Phase II setup"""
    
    def __init__(self):
        super().__init__()
        self.prompt_manager = FinalSelectionPrompt()

    def _make_selection_call(self, topics: Dict[str, Any]) -> Dict[str, Any]:
        """Make API call to select final topic"""
        print("\nStarting final topic selection...")
        
        prompt = self.prompt_manager.get_selection_prompt(
            json.dumps(topics, indent=2)
        )
        
        response = self.api_handler.make_api_call(
            stage='topic_selection',
            prompt=prompt
        )
        
        result = json.loads(
            self.json_handler.clean_json_string(response)
        )
        
        self._print_selection_summary(result)
        return result

    def _make_setup_call(self, selected_topic: Dict[str, Any]) -> Dict[str, Any]:
        """Make API call to prepare for Phase II"""
        print("\nPreparing Phase II setup...")
        
        prompt = self.prompt_manager.get_setup_prompt(
            json.dumps(selected_topic, indent=2)
        )
        
        response = self.api_handler.make_api_call(
            stage='phase_two_setup',
            prompt=prompt
        )
        
        result = json.loads(
            self.json_handler.clean_json_string(response)
        )
        
        self._print_setup_summary(result)
        return result

    def _get_selected_topic_data(
        self, topics: Dict[str, Any], selection: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get full data for selected topic"""
        chosen_title = selection['selection_analysis']['selection']['chosen_topic']
        if chosen_title not in topics:
            raise ValueError(f"Selected topic '{chosen_title}' not found in topic data")
        return topics[chosen_title]

    def run(self) -> Dict[str, Any]:
        """Run the final selection stage"""
        try:
            # Load topic development results
            topics = self.json_handler.load_json(
                self.config['paths']['topic_development']
            )
            print(f"\nLoaded {len(topics)} developed topics")
            
            # Make selection
            selection_result = self._make_selection_call(topics)
            
            # Get full data for selected topic
            selected_topic = self._get_selected_topic_data(
                topics, selection_result
            )
            
            # Make Phase II setup call
            setup_result = self._make_setup_call(selected_topic)
            
            # Combine results
            final_result = {
                "selection": selection_result,
                "phase_two_setup": setup_result
            }
            
            # Save results
            self.json_handler.save_json(
                final_result,
                self.config['paths']['final_selection']
            )
            
            return final_result
            
        except Exception as e:
            print(f"\nError in final selection stage: {str(e)}")
            raise

    def _print_selection_summary(self, result: Dict[str, Any]) -> None:
        """Print human-readable summary of selection"""
        print("\nSelection Decision:")
        selection = result['selection_analysis']['selection']
        print(f"\nChosen Topic: {selection['chosen_topic']}")
        print("\nRationale:", selection['rationale'])
        print("\nKey Strengths:")
        for strength in selection['key_strengths']:
            print(f"- {strength}")
        print("\nCritical Considerations:")
        for consideration in selection['critical_considerations']:
            print(f"- {consideration}")

    def _print_setup_summary(self, result: Dict[str, Any]) -> None:
        """Print human-readable summary of Phase II setup"""
        print("\nPhase II Setup Summary:")
        
        # Print thesis development
        thesis = result['phase_two_setup']['thesis_development']
        print("\nCore Thesis:", thesis['core_thesis'])
        
        # Print literature needs
        lit_needs = result['phase_two_setup']['literature_needs']
        
        # Print remembered papers
        if lit_needs.get('remembered_papers'):
            print("\nSpecifically Remembered Papers:")
            for paper in lit_needs['remembered_papers']:
                print(f"\nTitle: {paper['title']}")
                print(f"Authors: {', '.join(paper['authors'])}")
                print(f"Confidence in Title: {paper['confidence']['title_accuracy']}")
                print(f"Confidence in Content: {paper['confidence']['content_memory']}")
                print("Key Arguments Remembered:")
                for arg in paper['key_arguments']:
                    print(f"- {arg}")
                print(f"Relevance: {paper['relevance']}")
        else:
            print("\nNo specific papers remembered with confidence.")
            
        # Print search requirements
        if lit_needs.get('search_requirements'):
            print("\nLiterature Search Needs:")
            for req in lit_needs['search_requirements']:
                print(f"\nSearch Area: {req['area']}")
                print("Key Journals:")
                for journal in req['key_journals']:
                    print(f"- {journal}")
                print(f"Search Guidance: {req['search_guidance']}")
                print("Desired Findings:")
                for finding in req['desired_findings']:
                    print(f"- {finding}")
        
        # Print background knowledge
        if lit_needs.get('background_knowledge'):
            print("\nRequired Background Knowledge:")
            for knowledge in lit_needs['background_knowledge']:
                print(f"- {knowledge}")
        
        # Print special attention areas
        print("\nAreas Needing Special Attention:")
        areas = result['phase_two_setup']['development_guidance']['special_attention_areas']
        for area_name, area in areas.items():
            print(f"\n{area_name}:")
            print(f"Importance: {area['importance']}")
            print("Challenges:")
            for challenge in area['challenges']:
                print(f"- {challenge}")
            print("Considerations:")
            for consideration in area['considerations']:
                print(f"- {consideration}")

if __name__ == "__main__":
    selector = FinalTopicSelector()
    selector.run()