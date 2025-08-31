# src/stages/outline_generation.py

import os
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path
import json
import subprocess
import platform
import sys
from .base import BaseStage
from ..prompts.outline_prompts import OutlinePrompts

class OutlineGenerationStage(BaseStage):
    """Stage for developing detailed philosophical paper outline"""
    
    def __init__(self):
        super().__init__()
        self.prompt_manager = OutlinePrompts()
        
        # Define core development aspects
        self.development_aspects = [
            "argument_structure",
            "example_development",
            "formal_framework", 
            "objection_mapping",
            "integration"
        ]
        

        self.outline_dir = Path(self.get_full_path('outline_development')).parent / 'outlines'
        self.current_dir = self.outline_dir / 'current'
        self.history_dir = self.outline_dir / 'history'

        # Create directories
        for dir in [self.outline_dir, self.current_dir, self.history_dir]:
            dir.mkdir(parents=True, exist_ok=True)


    
    def load_stage_input(self) -> Dict[str, Any]:
        """Load selected paper and initial outline"""
        input_data = self.json_handler.load_json(self.get_full_path('final_selection'))
        print(f"\nLoaded input data: {json.dumps(input_data, indent=2)[:500]}")
        
        # Extract the selected paper info from nested structure
        final_selection = input_data.get('final_selection', {})
        selected_paper = final_selection.get('selected_paper', {})
        
        return {
            "title": selected_paper.get('title', ''),
            "selection_rationale": selected_paper.get('selection_rationale', {}),
            "development_recommendations": selected_paper.get('development_recommendations', []),
            "success_criteria": selected_paper.get('success_criteria', []),
            "core_analysis": input_data.get('analysis', {}).get('selected_topics', [])[0].get('core_analysis', {})  # Add this for additional context
        }
        
    
    def save_content(self, content: str, filename: str) -> str:
        """Save content to both current and history"""
        # Save current version
        current_path = self.current_dir / f"{filename}.md"
        with open(current_path, 'w') as f:
            f.write(content)
            
        # Save historical version with timestamp
        history_path = self.history_dir / f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(history_path, 'w') as f:
            f.write(content)
            
        return str(current_path)  # Return path to current version

    def load_content(self, filepath: str) -> str:
        """Load content from markdown file"""
        try:
            with open(filepath, 'r') as f:
                return f.read()
        except FileNotFoundError:
            print(f"No existing content found at {filepath}")
            return ""
        
    def synthesize_current_state(self, outlines: List[str], current_state: Dict[str, Any]) -> str:
        """Generate synthesis of current development state"""
        return self.api_handler.make_api_call(
            stage='synthesis',
            prompt=self.prompt_manager.get_synthesis_prompt(outlines, current_state)
        )
            
    def develop_aspect(self, current_state: Dict[str, Any], aspect: str, cycle: int) -> Dict[str, Any]:
        try:
            print(f"\nDeveloping {aspect}...")
            
            # Prepare initial content
            current_content = ""
            if current_state.get('content_path'):
                current_content = self.load_content(current_state['content_path'])
            elif aspect == "argument_structure":  # First aspect
                current_content = f"""
                # {current_state['title']}

                ## Core Analysis
                {json.dumps(current_state.get('core_analysis', {}), indent=2)}

                ## Development Guidance
                Selection Rationale:
                {json.dumps(current_state.get('selection_rationale', {}), indent=2)}

                Development Recommendations:
                {chr(10).join('- ' + rec for rec in current_state.get('development_recommendations', []))}

                Success Criteria:
                {chr(10).join('- ' + crit for crit in current_state.get('success_criteria', []))}
                """

            # Add synthesis to content if available
            if cycle > 1 and current_state.get('current_synthesis'):
                current_content += f"\n\n## Current Development Status (Synthesis)\n{current_state['current_synthesis']}"
                    
            
            print(f"\nInitial content for {aspect}:\n{current_content}") 
            development_response = self.api_handler.make_api_call(
                stage='outline_improvement',
                prompt=self.prompt_manager.get_development_prompt(
                    aspect=aspect,
                    current_content=current_content,
                    cycle=cycle
                )
            )
            print(f"\nDevelopment Response Preview:\n{development_response[:500]}")  # Add this
            
            # Critique
            critique_response = self.api_handler.make_api_call(
                stage='outline_critique',
                prompt=self.prompt_manager.get_critique_prompt(
                    content=development_response,
                    aspect=aspect
                )
            )
            print(f"\nCritique Response Preview:\n{critique_response[:500]}")  # Add this

            
            # Refinement
            refined_content = self.api_handler.make_api_call(
                stage='outline_refinement',
                prompt=self.prompt_manager.get_refinement_prompt(
                    content=development_response,
                    critique=critique_response,
                    aspect=aspect
                )
            )
            print(f"\nRefined Content Preview:\n{refined_content[:500]}")  # Add this
            
            # Save content and generate simple metadata
            content_path = self.save_content(
                refined_content,
                #f"{aspect}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                f"{aspect}"
            )

            try:
                # Simple metadata extraction
                lines = refined_content.split('\n')
                sections = [line.strip('# ') for line in lines if line.startswith('#')]
                word_count = len(refined_content.split())
                
                metadata = {
                    "sections": sections,
                    "word_count": word_count,
                    "aspect": aspect,
                    "timestamp": datetime.now().isoformat(),
                    "content_path": content_path
                }
            except Exception as e:
                print(f"Error creating metadata: {e}")
                metadata = {
                    "error": "Failed to create metadata",
                    "aspect": aspect,
                    "timestamp": datetime.now().isoformat(),
                    "content_path": content_path
                }
                
            return {
                "content_path": content_path,
                "metadata": metadata,
                "development_history": {
                    "aspect": aspect,
                    "timestamp": datetime.now().isoformat(),
                    "critique_summary": critique_response
                }
            }

        except Exception as e:
            print(f"Error in {aspect} development: {str(e)}")
            return None
    


    def merge_states(self, current_state: Dict[str, Any], new_state: Dict[str, Any]) -> Dict[str, Any]:
        """Merge development results into current state"""
        merged = current_state.copy()
        
        # Update content path
        merged['content_path'] = new_state['content_path']
        
        # Update metadata
        if 'metadata' not in merged:
            merged['metadata'] = {}
        merged['metadata'].update(new_state['metadata'])
        
        # Append to development history
        if 'development_history' not in merged:
            merged['development_history'] = []
        merged['development_history'].append(new_state['development_history'])
        
        return merged

    def run(self) -> Dict[str, Any]:
        """Run the outline development process"""
        try:
            current_state = self.load_stage_input()
            print(f"\nStarting outline development for: {current_state['title']}")
            current_state["started_at"] = datetime.now().isoformat()
            
            num_cycles = self.config['parameters']['outline_development_cycles']
            
            for cycle in range(num_cycles):
                print(f"\n=== Starting development cycle {cycle + 1}/{num_cycles} ===")
                
                # Store outlines from this cycle
                cycle_outlines = []
                
                for aspect in self.development_aspects:
                    development_result = self.develop_aspect(
                        current_state, 
                        aspect,
                        cycle=cycle + 1
                    )
                    if development_result:
                        current_state = self.merge_states(current_state, development_result)
                        # Collect outline for synthesis
                        cycle_outlines.append(self.load_content(development_result['content_path']))
                        
                        self.save_stage_output(current_state)
                
                # After each cycle (except the last), synthesize and add to state
                if cycle < num_cycles - 1:
                    synthesis = self.synthesize_current_state(cycle_outlines, current_state)
                    current_state['current_synthesis'] = synthesis
                    print(f"\nCycle {cycle + 1} Synthesis:\n{synthesis}")
                
            return current_state

        except Exception as e:
            print(f"Error in outline generation: {str(e)}")
            return None
    
    def save_stage_output(self, output: Dict[str, Any]) -> None:
        """Save stage output"""
        try:
            # Save state JSON
            self.json_handler.save_json(
                output,
                self.get_full_path('outline_development_state')
            )
            print(f"\nDevelopment state saved")
        except Exception as e:
            print(f"Error saving development results: {e}")



if __name__ == "__main__":
    # Platform-specific sleep prevention
    if platform.system() == "Darwin":  # macOS
        caffeinate = subprocess.Popen(['caffeinate', '-i'])
    elif platform.system() == "Windows":
        # Windows doesn't need this - it has different power management
        caffeinate = None
    
    try:
        generator = OutlineGenerationStage()
        results = generator.run()
    finally:
        if caffeinate:
            caffeinate.terminate()