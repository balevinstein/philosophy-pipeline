# src/stages/development.py

import json
from typing import Dict, Any, List
from .base import BaseStage
from ..prompts.development import DevelopmentPrompts

class DevelopmentStage(BaseStage):
    """Stage for broad development of selected topics"""
    
    def __init__(self):
        super().__init__()
        self.config = self.api_handler.config
        self.prompt_manager = DevelopmentPrompts()
        
    def load_stage_input(self) -> Dict[str, Any]:
        """Load generated topics and culling results"""
        topics = self.json_handler.load_json(self.get_full_path('generated_topics'))
        culling = self.json_handler.load_json(self.get_full_path('topics_culled'))
        return {
            "topics": topics,
            "culling": culling
        }

    def run_topic_analysis(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run the initial topic analysis"""
        try:
            print("\nStarting detailed topic analysis...")
            
            # Prepare the analysis prompt
            topics_json = json.dumps(input_data["topics"], indent=2)
            culling_json = json.dumps(input_data["culling"], indent=2)
            
            # Make API call for topic analysis
            response_text = self.api_handler.make_api_call(
                stage='topic_analysis',
                prompt=self.prompt_manager.topic_analysis.get_prompt(
                    topics_json=topics_json,
                    culling_json=culling_json
                )
            )
            
            # Process response
            cleaned_content = self.json_handler.clean_json_string(response_text)
            analysis_result = json.loads(cleaned_content)
            
            # Save analysis results
            self.json_handler.save_json(
                analysis_result,
                self.config['paths']['topic_analysis']
            )
            
            # Print summary
            print("\nTopic Analysis Summary:")
            for topic in analysis_result["selected_topics"]:
                print(f"\n- {topic['title']}")
                print(f"  Core thesis: {topic['core_analysis']['central_thesis'][:100]}...")
            
            return analysis_result
            
        except Exception as e:
            print(f"\nError in topic analysis:\nType: {type(e)}\nMessage: {str(e)}")
            return None

    def run_abstract_development(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Develop abstracts for selected topics"""
        try:
            print("\nStarting abstract development...")
            
            # Prepare the abstract prompt
            analysis_json = json.dumps(analysis_result, indent=2)
            
            # Make API call for abstract development
            response_text = self.api_handler.make_api_call(
                stage='abstract_development',
                prompt=self.prompt_manager.abstract_development.get_prompt(
                    analysis_json=analysis_json
                )
            )
            
            # Process response
            cleaned_content = self.json_handler.clean_json_string(response_text)
            abstract_result = json.loads(cleaned_content)
            
            # Save abstract results
            self.json_handler.save_json(
                abstract_result,
                self.config['paths']['abstracts']
            )
            
            # Print summary
            print("\nAbstract Development Summary:")
            for topic in abstract_result["topic_abstracts"]:
                print(f"\n- {topic['title']}")
                print(f"  Abstract preview: {topic['abstract'][:100]}...")
            
            return abstract_result
            
        except Exception as e:
            print(f"\nError in abstract development:\nType: {type(e)}\nMessage: {str(e)}")
            return None

 
    def save_stage_output(self, output: Dict[str, Any]) -> None:
        """Save complete development results"""
        try:
            self.json_handler.save_json(
                output,
                self.get_full_path('final_selection')
            )
            print(f"\nDevelopment results saved to {self.get_full_path('final_selection')}")
        except Exception as e:
            print(f"Error saving development results: {e}")


    def run_structure_planning(self, abstract_result: Dict[str, Any]) -> Dict[str, Any]:
        """Run the structure planning phase"""
        try:
            print("\nStarting structure planning...")
            
            # Prepare the structure planning prompt
            abstracts_json = json.dumps(abstract_result, indent=2)
            
            # Make API call for structure planning
            response_text = self.api_handler.make_api_call(
                stage='structure_planning',
                prompt=self.prompt_manager.structure_planning.get_prompt(
                    abstracts_json=abstracts_json
                )
            )
            
            # Process response
            cleaned_content = self.json_handler.clean_json_string(response_text)
            structure_result = json.loads(cleaned_content)
            
            # Save structure results
            self.json_handler.save_json(
                structure_result,
                self.config['paths']['outlines']
            )
            
            # Print summary
            print("\nStructure Planning Summary:")
            paper = structure_result["paper_structure"]
            print(f"\n- {paper['title']}")
            print("  Sections:")
            for section in paper['sections']:
                print(f"    • {section['section_title']} ({section['target_length']} words)")
            
            return structure_result
            
        except Exception as e:
            print(f"\nError in structure planning:\nType: {type(e)}\nMessage: {str(e)}")
            return None

    def run_section_development(self, structure_result: Dict[str, Any]) -> Dict[str, Any]:
        """Run the section development phase"""
        try:
            print("\nStarting section development...")
            paper_sections = []
            previous_sections = ""
            
            paper = structure_result["paper_structure"]
            
            for section in paper['sections']:
                # Make API call for each section
                response_text = self.api_handler.make_api_call(
                    stage='section_development',
                    prompt=self.prompt_manager.section_development.get_prompt(
                        structure_json=json.dumps(paper, indent=2),
                        section_focus=section['section_title'],
                        previous_sections=previous_sections
                    )
                )
                
                # Add section content to previous sections for context
                previous_sections += f"\n\n{response_text}"
                paper_sections.append({
                    "section_title": section['section_title'],
                    "content": response_text
                })
            
            section_results = {
                paper['title']: paper_sections
            }
            
            # Save section results
            self.json_handler.save_json(
                {"section_developments": section_results},
                self.config['paths']['arguments']
            )
            
            print("\nSection Development Complete")
            return {"section_developments": section_results}
            
        except Exception as e:
            print(f"\nError in section development:\nType: {type(e)}\nMessage: {str(e)}")
            return None
    
    def run(self) -> Dict[str, Any]:
        """Run the full development stage"""
        try:
            # Load input data
            input_data = self.load_stage_input()
            print(f"\nLoaded input data - {len(input_data['topics'])} topics available")
            
            # Run topic analysis
            analysis_result = self.run_topic_analysis(input_data)
            if not analysis_result:
                return None
                
            # Run abstract development
            abstract_result = self.run_abstract_development(analysis_result)
            if not abstract_result:
                return None
            
            # Run structure planning
            structure_result = self.run_structure_planning(abstract_result)
            if not structure_result:
                return None
            
            # Run section development
            section_result = self.run_section_development(structure_result)
            if not section_result:
                return None
            
            return {
                "analysis": analysis_result,
                "abstracts": abstract_result,
                "structure": structure_result,
                "sections": section_result
            }
            
        except Exception as e:
            print(f"\nError in development stage:\nType: {type(e)}\nMessage: {str(e)}")
            return None

if __name__ == "__main__":
    developer = DevelopmentStage()
    results = developer.run()