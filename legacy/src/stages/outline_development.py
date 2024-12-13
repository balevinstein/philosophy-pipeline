import os
import traceback
from typing import Dict, Any, Optional, List
from datetime import datetime
import json
from .base import BaseStage
from ..prompts.outline_development import OutlineDevelopmentPrompts

class OutlineDevelopmentStage(BaseStage):
    """Stage for developing detailed paper outline"""

    def __init__(self):
        super().__init__()
        self.config = self.api_handler.config
        self.prompt_manager = OutlineDevelopmentPrompts()
        
        # Update to include all content-generating aspects
        self.development_aspects = [
            "argument_structure",
            "example_development",
            "formal_framework", 
            "objection_mapping",
            "integration"
        ]

        # Add initial structure for content types
        self.content_structure = {
            "examples": {
                "primary": {},
                "supporting": []
            },
            "formal_content": {
                "foundations": {},
                "development": []
            },
            "objections": {
                "major": [],
                "anticipated": []
            },
            "argument_structure": {
                "premises": [],
                "conclusions": [],
                "connections": []
            }
        }

    def load_stage_input(self) -> Dict[str, Any]:
        """Load selected topic and initial outline"""
        return self.json_handler.load_json(self.get_full_path('final_selection'))
    
    def save_stage_output(self, output: Dict[str, Any]) -> None:
        """Save stage outputs"""
        try:
            # Save development state as JSON using base class functionality
            self.json_handler.save_json(output, self.get_full_path('outline_development_state'))
            
            # Save markdown outline
            markdown_content = self.generate_outline_markdown(output["current_state"])
            outline_path = os.path.join(
                os.path.dirname(self.get_full_path('outline_development_state')),
                self.config['paths']['outline_development']
            )
            with open(outline_path, 'w') as f:
                f.write(markdown_content)
                
            print(f"\nDevelopment results saved")
            
        except Exception as e:
            print(f"Error saving development results: {e}")

    def generate_outline_markdown(self, state: Dict[str, Any]) -> str:
        """Generate markdown version of current outline"""
        try:
            outline = []
            
            # Add title and overview
            outline.append(f"# {state['title']}\n")
            outline.append("## Overview\n")
            outline.append(f"{state.get('core_thesis', '')}\n")
            
            # Add sections
            sections = state.get('sections', [])
            for i, section in enumerate(sections):
                outline.append(f"## {section['section_title']}\n")
                outline.append(f"Target length: {section.get('target_length', 'TBD')} words\n")
                
                # Key claims and moves
                if 'key_claims' in section:
                    outline.append("\n### Key Claims")
                    for claim in section['key_claims']:
                        outline.append(f"- {claim}")
                    outline.append("")
                
                if 'core_moves' in section:
                    outline.append("\n### Core Moves")
                    for move in section['core_moves']:
                        outline.append(f"- {move}")
                    outline.append("")

                if 'formal_definitions' in section:
                    outline.append("\n### Formal Definitions")
                    for definition in section['formal_definitions']:
                        outline.append(f"\n#### {definition.get('term', '')}")
                        outline.append(f"**Definition:** {definition.get('definition', '')}")
                        if definition.get('formal_notation'):
                            outline.append("\n**Formal Notation:**")
                            outline.append(f"```\n{definition['formal_notation']}\n```")
                        if definition.get('justification'):
                            outline.append(f"\n**Justification:** {definition['justification']}")
                    outline.append("")

                          # Add technical framework if present
                if 'technical_framework' in section:
                    outline.append("\n### Technical Framework")
                    framework = section['technical_framework']
                    
                    if framework.get('base_elements'):
                        outline.append("\n#### Base Elements")
                        for element in framework['base_elements']:
                            outline.append(f"- {element}")
                    
                    if framework.get('axioms'):
                        outline.append("\n#### Axioms")
                        for axiom in framework['axioms']:
                            outline.append(f"- {axiom}")
                    
                    if framework.get('key_properties'):
                        outline.append("\n#### Key Properties")
                        for prop in framework['key_properties']:
                            outline.append(f"- {prop}")
                    outline.append("")

                # Add formal development content
                if 'formal_development' in section:
                    outline.append("\n### Formal Development")
                    for dev in section['formal_development']:
                        outline.append(f"\n#### {dev.get('element_type', '').title()}")
                        outline.append(dev.get('content', ''))
                        if dev.get('formal_notation'):
                            outline.append("\n**Formal Notation:**")
                            outline.append(f"```\n{dev['formal_notation']}\n```")
                        if dev.get('supporting_notes'):
                            outline.append(f"\n**Notes:** {dev['supporting_notes']}")
                    outline.append("")

                
                # Technical elements
                if 'technical_requirements' in section:
                    outline.append("\n### Technical Requirements")
                    for req in section['technical_requirements']:
                        outline.append(f"- {req}")
                    outline.append("")

                # Literature engagement
                if 'literature_engagement' in section:
                    outline.append("\n### Literature Engagement")
                    for lit in section['literature_engagement']:
                        outline.append(f"- {lit}")
                    outline.append("")
                
                # Examples
                if 'examples' in section:
                    outline.append("\n### Examples")
                    if section['examples'].get('primary'):
                        outline.append("\n#### Primary Example")
                        primary = section['examples']['primary']
                        outline.append(primary.get('refined_version', primary.get('text', '')))
                        if primary.get('technical_notes'):
                            outline.append("\n**Technical Notes:**")
                            outline.append(primary['technical_notes'])
                    
                    if section['examples'].get('supporting'):
                        for idx, ex in enumerate(section['examples']['supporting'], 1):
                            purpose = ex.get('purpose', '')
                            outline.append(f"\n#### Supporting Example {idx}{f' ({purpose})' if purpose else ''}")
                            outline.append(ex.get('refined_version', ex.get('text', '')))
                            if ex.get('technical_notes'):
                                outline.append("\n**Technical Notes:**")
                                outline.append(ex['technical_notes'])
                    
                # Formal content
                if 'formal_content' in section:
                    outline.append("\n### Formal Content")
                    if 'foundations' in section['formal_content']:
                        outline.append("\n#### Foundations")
                        for key, content in section['formal_content']['foundations'].items():
                            if isinstance(content, dict):
                                outline.append(f"\n**{key.replace('_', ' ').title()}:**")
                                outline.append(content.get('refined_version', content.get('content', '')))
                                if content.get('technical_notes'):
                                    outline.append("\n**Technical Notes:**")
                                    outline.append(content['technical_notes'])
                    
                    if 'development' in section['formal_content']:
                        for dev in section['formal_content']['development']:
                            outline.append(f"\n#### {dev.get('type', '').replace('_', ' ').title()}")
                            outline.append(dev.get('refined_version', dev.get('content', '')))
                            if dev.get('technical_notes'):
                                outline.append("\n**Technical Notes:**")
                                outline.append(dev['technical_notes'])
                
                # Objections and responses
                if 'objections' in section:
                    outline.append("\n### Objections and Responses")
                    if section['objections'].get('major'):
                        for obj in section['objections']['major']:
                            outline.append("\n#### Objection")
                            outline.append(obj.get('objection_text', obj.get('objection', '')))
                            outline.append("\n#### Response")
                            outline.append(obj.get('response_text', obj.get('response', '')))
                            if obj.get('technical_support'):
                                outline.append("\n**Technical Support:**")
                                outline.append(obj['technical_support'])
                    
                    if section['objections'].get('anticipated'):
                        outline.append("\n#### Anticipated Concerns")
                        for concern in section['objections']['anticipated']:
                            outline.append(f"\n**Concern:** {concern.get('concern_text', '')}")
                            outline.append(f"\n**Resolution:** {concern.get('resolution_text', '')}")
                
                # Add transitions to next section
                if i < len(sections) - 1:  # If not the last section
                    for transition in state.get('transitions', []):
                        if (transition.get('from_section') == section['section_title'] and 
                            transition.get('to_section') == sections[i + 1]['section_title']):
                            outline.append("\n### Transition to Next Section")
                            outline.append(transition.get('transition_text', ''))
                
                # Add relevant cross references
                cross_refs = state.get('cross_references', [])
                section_refs = [ref for ref in cross_refs if 
                            ref.get('source', '').startswith(section['section_title']) or 
                            ref.get('target', '').startswith(section['section_title'])]
                if section_refs:
                    outline.append("\n### Cross References")
                    for ref in section_refs:
                        outline.append(f"\n**From {ref.get('source')} to {ref.get('target')}:**")
                        outline.append(ref.get('reference_text', ''))
                
                # Condensed development summary
                if 'development_notes' in section:
                    outline.append("\n### Development Notes")
                    outline.append("Key verifications:")
                    for aspect, notes in section['development_notes'].items():
                        if isinstance(notes, dict) and 'verification' in notes:
                            v = notes['verification']
                            outline.append(f"\n**{aspect.replace('_', ' ').title()}:**")
                            if v.get('technical_accuracy'):
                                outline.append(f"- Technical: {v['technical_accuracy']}")
                            if v.get('philosophical_contribution'):
                                outline.append(f"- Philosophical: {v['philosophical_contribution']}")
                
                outline.append("\n")

                if 'verification' in section:
                    outline.append("\n### Verification Notes")
                    verify = section['verification']
                    if verify.get('technical_accuracy'):
                        outline.append(f"\n**Technical Accuracy:** {verify['technical_accuracy']}")
                    if verify.get('clarity_achieved'):
                        outline.append(f"\n**Clarity:** {verify['clarity_achieved']}")
                    if verify.get('philosophical_connection'):
                        outline.append(f"\n**Philosophical Connection:** {verify['philosophical_connection']}")
                    outline.append("")

                
            return "\n".join(outline)
                    
        except Exception as e:
            print(f"Error generating markdown: {e}")
            return "Error generating outline markdown"
        
    def update_outline_state(self, current_state: Dict[str, Any], development_result: Dict[str, Any]) -> Dict[str, Any]:
        """Update outline state with development results"""
        try:
            print("\nUpdating outline state...")
            new_state = current_state.copy()
            aspect = development_result['aspect']

            # Add error recovery for JSON parsing
            if 'improvement' in development_result:
                if isinstance(development_result['improvement'], str):
                    try:
                        improvement = json.loads(development_result['improvement'])
                    except json.JSONDecodeError:
                        print("Warning: Failed to parse improvement JSON, attempting cleanup")
                        cleaned = self.json_handler.clean_json_string(development_result['improvement'])
                        try:
                            improvement = json.loads(cleaned)
                        except json.JSONDecodeError:
                            print("Error: Could not parse improvement JSON even after cleanup")
                            improvement = {"content": {}}
                else:
                    improvement = development_result['improvement']
            
            # Initialize development_notes if it doesn't exist
            if 'development_notes' not in new_state:
                new_state['development_notes'] = {}
            
            # Parse improvement content
            try:
                if isinstance(development_result['improvement'], str):
                    improvement = json.loads(development_result['improvement'])
                else:
                    improvement = development_result['improvement']
                    
                if 'content' in improvement:
                    content = improvement['content']
                    
                    # Update sections with text content
                    if 'text' in content:
                        for text_item in content['text']:
                            section_title = text_item.get('section')
                            if section_title:
                                for section in new_state['sections']:
                                    if section['section_title'] == section_title:
                                        if 'content' not in section:
                                            section['content'] = {}
                                        section['content']['text'] = text_item.get('content', '')
                                        if 'formal_notation' in text_item:
                                            section['content']['formal_notation'] = text_item['formal_notation']

            except (json.JSONDecodeError, KeyError) as e:
                print(f"\nError processing improvement content: {e}")
                
            # Handle refinement process and verification
            try:
                if 'refinement' in development_result:
                    if isinstance(development_result['refinement'], str):
                        refinement = json.loads(development_result['refinement'])
                    else:
                        refinement = development_result['refinement']
                    
                    if aspect not in new_state['development_notes']:
                        new_state['development_notes'][aspect] = {}
                        
                    if 'refinement_process' in refinement:
                        new_state['development_notes'][aspect].update({
                            'technical_resolution': refinement['refinement_process'].get('technical_resolution', ''),
                            'philosophical_resolution': refinement['refinement_process'].get('philosophical_resolution', ''),
                            'integration_strategy': refinement['refinement_process'].get('integration_strategy', '')
                        })
                    
                    if 'verification' in refinement:
                        new_state['development_notes'][aspect]['verification'] = refinement['verification']
                    
            except (json.JSONDecodeError, KeyError) as e:
                print(f"\nError processing refinement: {e}")

            return new_state
                    
        except Exception as e:
            print(f"Error updating outline state: {e}")
            print(f"Traceback: {traceback.format_exc()}")
            return current_state
        
 
                


    def is_improvement_significant(self, old_state: Dict, new_state: Dict) -> bool:
        """Determine if the improvement is significant enough to continue"""
        try:
            # Check for substantive changes in key areas
            changes = {
                'content': False,
                'structure': False,
                'technical': False
            }
            
            # Compare sections
            old_sections = old_state.get('sections', [])
            new_sections = new_state.get('sections', [])
            
            if len(old_sections) != len(new_sections):
                return True
                
            for old_section, new_section in zip(old_sections, new_sections):
                # Check content changes
                if old_section.get('content') != new_section.get('content'):
                    changes['content'] = True
                    
                # Check structural changes
                if (old_section.get('key_claims') != new_section.get('key_claims') or
                    old_section.get('core_moves') != new_section.get('core_moves')):
                    changes['structure'] = True
                    
                # Check technical changes
                if old_section.get('technical_requirements') != new_section.get('technical_requirements'):
                    changes['technical'] = True
                    
            # Consider improvement significant if any substantial changes occurred
            return any(changes.values())
            
        except Exception as e:
            print(f"Error checking improvement significance: {e}")
            return False

    
    def develop_aspect(self, current_state: Dict[str, Any], aspect: str) -> Dict[str, Any]:
        """Run development cycle for a specific aspect with specialized processing"""
        try:
            print(f"\n=== Starting {aspect} development ===")
            
            # Different handling based on aspect
            if aspect in ['formal_framework', 'argument_structure']:
                print("\nInitiating formal development...")
                improvement_response = self.api_handler.make_api_call(
                    stage='formal_development',
                    prompt=self.prompt_manager.get_formal_development_prompt(
                        current_state=json.dumps(current_state, indent=2),
                        focus_aspect=aspect
                    )
                )
                
                if not improvement_response:
                    print("WARNING: Received empty improvement response")
                    return None
                    
                print("\nResponse received, length:", len(improvement_response))
                print("Response preview:", improvement_response[:200])

                print("\nChecking clarity...")
                clarity_critique = self.api_handler.make_api_call(
                    stage='clarity_verification',
                    prompt=self.prompt_manager.get_clarity_critique_prompt(
                        proposed_changes=improvement_response,
                        focus_aspect=aspect
                    )
                )

                print("\nRefining formal content...")
                refined_response = self.api_handler.make_api_call(
                    stage='formal_refinement',
                    prompt=self.prompt_manager.get_formal_refinement_prompt(
                        original_development=improvement_response,
                        clarity_feedback=clarity_critique,
                        focus_aspect=aspect
                    )
                )

            elif aspect == 'example_development':
                print("\nGenerating initial examples...")
                improvement_response = self.api_handler.make_api_call(
                    stage='outline_improvement',
                    prompt=self.prompt_manager.get_example_development_prompt(
                        current_state=json.dumps(current_state, indent=2)
                    )
                )
                
                print("\nEnhancing examples with technical detail...")
                clarity_critique = self.api_handler.make_api_call(
                    stage='example_enhancement',
                    prompt=self.prompt_manager.get_example_enhancement_prompt(
                        initial_examples=improvement_response,
                        current_state=json.dumps(current_state, indent=2)
                    )
                )
                
                print("\nFinalizing examples...")
                refined_response = self.api_handler.make_api_call(
                    stage='outline_refinement',
                    prompt=self.prompt_manager.get_refinement_prompt(
                        original_changes=improvement_response,
                        critique=clarity_critique,
                        focus_aspect=aspect
                    )
                )

            else:
                print("\nRunning standard development process...")
                improvement_response = self.api_handler.make_api_call(
                    stage='outline_improvement',
                    prompt=self.prompt_manager.get_development_prompt(
                        current_state=json.dumps(current_state, indent=2),
                        focus_aspect=aspect
                    )
                )
                
                print("\nConducting critique...")
                clarity_critique = self.api_handler.make_api_call(
                    stage='outline_critique',
                    prompt=self.prompt_manager.get_critique_prompt(
                        proposed_changes=improvement_response,
                        focus_aspect=aspect
                    )
                )
                
                print("\nRefining content...")
                refined_response = self.api_handler.make_api_call(
                    stage='outline_refinement',
                    prompt=self.prompt_manager.get_refinement_prompt(
                        original_changes=improvement_response,
                        critique=clarity_critique,
                        focus_aspect=aspect
                    )
                )

            print("\nCleaning and validating responses...")
            cleaned_improvement = self.json_handler.clean_json_string(improvement_response)
            cleaned_critique = self.json_handler.clean_json_string(clarity_critique)
            cleaned_refinement = self.json_handler.clean_json_string(refined_response)

            # Validate and clean responses if needed
            responses_to_check = {
                'improvement_response': cleaned_improvement,
                'clarity_critique': cleaned_critique,
                'refined_response': cleaned_refinement
            }
            
            for key, response in responses_to_check.items():
                if response:
                    try:
                        json.loads(response if isinstance(response, str) else json.dumps(response))
                    except json.JSONDecodeError:
                        print(f"Warning: Invalid JSON in {key}, attempting cleanup")
                        responses_to_check[key] = self.json_handler.clean_json_string(
                            response if isinstance(response, str) else json.dumps(response)
                        )
            
            return {
                "aspect": aspect,
                "improvement": responses_to_check['improvement_response'],
                "critique": responses_to_check['clarity_critique'],
                "refinement": responses_to_check['refined_response']
            }


        except Exception as e:
            print(f"\nError in {aspect} development:")
            print(f"Type: {type(e)}")
            print(f"Message: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            return None
    
    def run(self) -> Dict[str, Any]:
        """Run the outline development stage"""
        try:
            input_data = self.load_stage_input()
            final_selection = input_data.get('final_selection', {})
            selected_paper = final_selection.get('selected_paper', {})
            title = selected_paper.get('title', 'Unknown Paper')
            print(f"\nStarting outline development for: {title}")
            
            current_state = input_data.get('structure', {}).get('paper_structures', [])[0]
            development_history = []
            
            # Run development cycles
            for cycle in range(self.config['parameters']['outline_development_cycles']):
                print(f"\nStarting development cycle {cycle + 1}")
                
                # Go through each aspect
                for aspect in self.development_aspects:
                    print(f"\nFocusing on: {aspect}")
                    
                    # Run development for this aspect
                    development_result = self.develop_aspect(current_state, aspect)
                    if not development_result:
                        continue
                    
                    # Update state and track development
                    current_state = self.update_outline_state(
                        current_state, 
                        development_result
                    )
                    
                    development_history.append({
                        "cycle": cycle + 1,
                        "timestamp": datetime.now().isoformat(),
                        **development_result
                    })
                
                # Save state for this cycle
                cycle_output = {
                    "current_state": current_state,
                    "development_history": development_history
                }
                self.save_stage_output(cycle_output)
                
            return current_state
                
        except Exception as e:
            print(f"\nError in outline development:\nType: {type(e)}\nMessage: {str(e)}")
            return None

if __name__ == "__main__":
    developer = OutlineDevelopmentStage()
    developer.run()