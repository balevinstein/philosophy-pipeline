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
            
            # Initialize development_notes if it doesn't exist
            if 'development_notes' not in new_state:
                new_state['development_notes'] = {}
            if aspect not in new_state['development_notes']:
                new_state['development_notes'][aspect] = {}
                
            try:
                refined_str = self.json_handler.clean_json_string(development_result['refinement'])
                refinement = json.loads(refined_str)
            except json.JSONDecodeError as e:
                print(f"\nJSON decode error: {e}")
                print(f"\nFull refinement response:\n{development_result['refinement']}")
                return current_state

            # After getting refinement, initialize section notes
            for section in new_state['sections']:
                if 'development_notes' not in section:
                    section['development_notes'] = {}
                if aspect not in section['development_notes']:
                    section['development_notes'][aspect] = {}
                
                # Move relevant notes into section
                section['development_notes'][aspect].update({
                    'technical_resolution': refinement.get('refinement_process', {}).get('technical_resolution', ''),
                    'philosophical_resolution': refinement.get('refinement_process', {}).get('philosophical_resolution', ''),
                    'integration_strategy': refinement.get('refinement_process', {}).get('integration_strategy', ''),
                    'verification': refinement.get('verification', {})
                })
    
            
            # Look for content in the refinement structure we're actually getting
            if 'refined_content' in refinement:
                for content in refinement['refined_content']:
                    content_type = content.get('content_type', '')
                    # Determine target section based on content type or explicit target
                    section_title = content.get('target_section')
                    if not section_title:
                        # Default section mappings based on content type
                        section_mappings = {
                            'example': 'The Asymmetry Phenomenon',
                            'formal_definition': 'Formal Analysis and Revision',
                            'theorem': 'Formal Analysis and Revision',
                            'objection_response': 'Formal Analysis and Revision',
                            'bridge_principle': 'Introduction'
                        }
                        section_title = section_mappings.get(content_type, section_title)
                    
                    for section in new_state['sections']:
                        if section['section_title'] == section_title:
                            # Examples
                            if content_type == 'example' or content_type == 'primary_example':
                                if 'examples' not in section:
                                    section['examples'] = {'primary': {}, 'supporting': []}
                                if content_type == 'primary_example' or content.get('is_primary'):
                                    section['examples']['primary'] = {
                                        'text': content['refined_version'],
                                        'technical_notes': content.get('technical_notes', ''),
                                        'philosophical_notes': content.get('philosophical_notes', '')
                                    }
                                else:
                                    section['examples']['supporting'].append({
                                        'text': content['refined_version'],
                                        'purpose': content.get('purpose', ''),
                                        'technical_notes': content.get('technical_notes', '')
                                    })
                            
                            # Formal content
                            elif content_type in ['formal_definition', 'theorem', 'proof_outline', 'formal_framework']:
                                if 'formal_content' not in section:
                                    section['formal_content'] = {'foundations': {}, 'development': []}
                                if content_type == 'formal_definition' or content_type == 'formal_framework':
                                    section['formal_content']['foundations'][content_type] = {
                                        'content': content['refined_version'],
                                        'technical_notes': content.get('technical_notes', ''),
                                        'philosophical_notes': content.get('philosophical_notes', '')
                                    }
                                else:
                                    section['formal_content']['development'].append({
                                        'type': content_type,
                                        'content': content['refined_version'],
                                        'technical_notes': content.get('technical_notes', '')
                                    })
                            
                            # Objections and responses
                            elif content_type in ['objection_response', 'anticipated_concern']:
                                if 'objections' not in section:
                                    section['objections'] = {'major': [], 'anticipated': []}
                                if content_type == 'objection_response':
                                    section['objections']['major'].append({
                                        'objection': content.get('original_version', ''),
                                        'response': content['refined_version'],
                                        'technical_support': content.get('technical_notes', '')
                                    })
                                else:
                                    section['objections']['anticipated'].append({
                                        'concern': content.get('original_version', ''),
                                        'resolution': content['refined_version']
                                    })

            # Also check refinement_process for additional content
            if 'refinement_process' in refinement:
                process = refinement['refinement_process']
                new_state['development_notes'][aspect].update({
                    'technical_resolution': process.get('technical_resolution', ''),
                    'philosophical_resolution': process.get('philosophical_resolution', ''),
                    'integration_strategy': process.get('integration_strategy', '')
                })
            
            # Save verification info if present
            if 'verification' in refinement:
                new_state['development_notes'][aspect]['verification'] = refinement['verification']
            
            return new_state
                
        except Exception as e:
            print(f"Error updating outline state: {e}")
            print(f"Traceback: {traceback.format_exc()}")  # Add this for better error tracking
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
        """Run development cycle for a specific aspect"""
        try:
            # Actor: Propose improvements
            print(f"\nGetting improvement proposal for {aspect}...")
            improvement_response = self.api_handler.make_api_call(
                stage='outline_improvement',
                prompt=self.prompt_manager.get_development_prompt(
                    current_state=json.dumps(current_state, indent=2),
                    focus_aspect=aspect
                )
            ) or "{}"  # Default to empty object if None
            
            # Critic: Analyze improvements
            print(f"\nGetting critique for {aspect}...")
            critique_response = self.api_handler.make_api_call(
                stage='outline_critique',
                prompt=self.prompt_manager.get_critique_prompt(
                    proposed_changes=improvement_response,
                    focus_aspect=aspect
                )
            ) or "{}"
            
            # Debug responses before cleaning
            print(f"\nDebug: Raw improvement response type: {type(improvement_response)}")
            print(f"\nDebug: Raw critique response type: {type(critique_response)}")
            
            # Clean responses
            cleaned_improvement = self.json_handler.clean_json_string(improvement_response)
            cleaned_critique = self.json_handler.clean_json_string(critique_response)
            
            # Better debug printing with start and end
            print("\nDebug: Improvement response start:")
            print(cleaned_improvement[:500])
            print("\nDebug: Improvement response end:")
            print(cleaned_improvement[-500:])
            print("\nDebug: Critique response start:")
            print(cleaned_critique[:500])
            print("\nDebug: Critique response end:")
            print(cleaned_critique[-500:])
            
            # Actor: Refine based on critique
            print(f"\nGetting refinement for {aspect}...")
            refined_response = self.api_handler.make_api_call(
                stage='outline_refinement',
                prompt=self.prompt_manager.get_refinement_prompt(
                    original_changes=cleaned_improvement,
                    critique=cleaned_critique,
                    focus_aspect=aspect
                )
            ) or "{}"  # Default to empty object if None
            
            cleaned_refinement = self.json_handler.clean_json_string(refined_response)
            
            development_result = {
                "aspect": aspect,
                "improvement": cleaned_improvement,
                "critique": cleaned_critique,
                "refinement": cleaned_refinement
            }
            
            return development_result
                
        except Exception as e:
            print(f"\nError in {aspect} development:\nType: {type(e)}\nMessage: {str(e)}")
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