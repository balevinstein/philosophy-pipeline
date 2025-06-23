from typing import Dict, Any, List, Tuple
import logging
import json

from src.phases.core.worker_base import Worker
from src.phases.phase_two.stages.stage_eight.prompts.writing_optimization_prompts import WritingOptimizationPrompts
from src.utils.api import APIHandler
from src.utils.json_utils import JSONHandler


class WritingOptimizationWorker(Worker):
    """Worker for optimizing writing context for Phase III"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.prompts = WritingOptimizationPrompts()
        self.logger = logging.getLogger(__name__)
        self.api_handler = APIHandler(config)
        self.json_handler = JSONHandler()
        
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate writing aids and optimized context for Phase III
        
        Args:
            state: Dictionary containing:
                - refined_moves: List of refined philosophical moves
                - revised_thesis: The updated thesis
                - outline: The paper structure
                - literature_synthesis: Literature context
                - move_examples: Examples of good philosophical moves
                
        Returns:
            Dictionary containing optimized writing context
        """
        self.logger.info("Starting writing context optimization...")
        
        # Extract inputs
        refined_moves = state.get("refined_moves", [])
        revised_thesis = state.get("revised_thesis", "")
        revised_contribution = state.get("revised_contribution", "")
        outline = state.get("outline", {})
        literature = state.get("literature_synthesis", {})
        move_examples = state.get("move_examples", {})
        
        # Generate different types of writing aids
        hooks = self._generate_introduction_hooks(revised_thesis, revised_contribution)
        transitions = self._generate_section_transitions(outline, refined_moves)
        move_integration = self._generate_move_integration_guidance(refined_moves, outline)
        phrase_banks = self._generate_phrase_banks()
        
        # Create the optimized writing context
        optimized_context = {
            "paper_metadata": {
                "thesis": revised_thesis,
                "core_contribution": revised_contribution,
                "target_journal": "Analysis",
                "word_target": 4000
            },
            "writing_aids": {
                "introduction_hooks": hooks,
                "section_transitions": transitions,
                "phrase_banks": phrase_banks,
                "conclusion_clinchers": self._generate_conclusion_options(revised_thesis)
            },
            "content_organization": {
                "move_to_section_mapping": self._map_moves_to_sections(refined_moves, outline),
                "move_integration_guidance": move_integration,
                "citation_placement": self._map_citations_to_arguments(refined_moves, literature)
            },
            "section_blueprints": self._create_section_blueprints(outline, refined_moves, transitions),
            "refined_moves": refined_moves,
            "literature_context": literature
        }
        
        self.logger.info("Writing context optimization complete.")
        return optimized_context
        
    def _generate_introduction_hooks(self, thesis: str, contribution: str) -> List[Dict[str, str]]:
        """Generate multiple hook options for the introduction"""
        
        prompt = self.prompts.get_hooks_prompt(thesis, contribution)
        
        response_text, _ = self.api_handler.make_api_call(
            stage="phase_2_8_hooks",
            prompt=prompt,
            system_prompt=self.prompts.get_system_prompt()
        )
        
        try:
            # Extract JSON portion if response has narrative text before it
            json_start = response_text.find('```json\n{')
            if json_start != -1:
                json_end = response_text.rfind('}\n```')
                if json_end != -1:
                    json_content = response_text[json_start+8:json_end+1]  # Extract just the JSON
                    hooks_data = json.loads(json_content)
                else:
                    # Try without ending markers
                    json_content = response_text[json_start+8:]
                    cleaned_response = self.json_handler.clean_json_string(json_content)
                    hooks_data = json.loads(cleaned_response)
            else:
                # Standard JSON parsing
                cleaned_response = self.json_handler.clean_json_string(response_text)
                hooks_data = json.loads(cleaned_response)
        except (json.JSONDecodeError, Exception) as e:
            self.logger.warning(f"Failed to parse introduction hooks JSON: {e}")
            return []
        
        return hooks_data.get("hooks", [])
        
    def _generate_section_transitions(self, outline: Dict[str, Any], moves: List[Dict[str, Any]]) -> Dict[str, str]:
        """Generate smooth transitions between sections"""
        
        prompt = self.prompts.get_transitions_prompt(outline, moves)
        
        response_text, _ = self.api_handler.make_api_call(
            stage="phase_2_8_transitions",
            prompt=prompt,
            system_prompt=self.prompts.get_system_prompt()
        )
        
        cleaned_response = self.json_handler.clean_json_string(response_text)
        transitions_data = json.loads(cleaned_response)
        
        return transitions_data.get("transitions", {})
        
    def _generate_move_integration_guidance(self, moves: List[Dict[str, Any]], outline: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate guidance for integrating each move into the narrative"""
        
        prompt = self.prompts.get_integration_prompt(moves, outline)
        
        response_text, _ = self.api_handler.make_api_call(
            stage="phase_2_8_integration",
            prompt=prompt,
            system_prompt=self.prompts.get_system_prompt()
        )
        
        cleaned_response = self.json_handler.clean_json_string(response_text)
        integration_data = json.loads(cleaned_response)
        
        return integration_data.get("integration_guidance", [])
        
    def _generate_phrase_banks(self) -> Dict[str, List[str]]:
        """Generate Analysis-style phrase banks"""
        
        prompt = self.prompts.get_phrase_banks_prompt()
        
        response_text, _ = self.api_handler.make_api_call(
            stage="phase_2_8_phrases",
            prompt=prompt,
            system_prompt=self.prompts.get_system_prompt()
        )
        
        cleaned_response = self.json_handler.clean_json_string(response_text)
        phrases_data = json.loads(cleaned_response)
        
        return phrases_data.get("phrase_banks", {})
        
    def _generate_conclusion_options(self, thesis: str) -> List[Dict[str, str]]:
        """Generate conclusion clincher options"""
        
        prompt = self.prompts.get_conclusion_prompt(thesis)
        
        response_text, _ = self.api_handler.make_api_call(
            stage="phase_2_8_conclusion",
            prompt=prompt,
            system_prompt=self.prompts.get_system_prompt()
        )
        
        try:
            # Extract JSON portion if response has narrative text before it
            json_start = response_text.find('```json\n{')
            if json_start != -1:
                json_end = response_text.rfind('}\n```')
                if json_end != -1:
                    json_content = response_text[json_start+8:json_end+1]  # Extract just the JSON
                    conclusion_data = json.loads(json_content)
                else:
                    # Try without ending markers
                    json_content = response_text[json_start+8:]
                    cleaned_response = self.json_handler.clean_json_string(json_content)
                    conclusion_data = json.loads(cleaned_response)
            else:
                # Standard JSON parsing
                cleaned_response = self.json_handler.clean_json_string(response_text)
                conclusion_data = json.loads(cleaned_response)
        except (json.JSONDecodeError, Exception) as e:
            self.logger.warning(f"Failed to parse conclusion options JSON: {e}")
            return []
        
        return conclusion_data.get("conclusion_options", [])
        
    def _map_moves_to_sections(self, moves: List[Dict[str, Any]], outline: Dict[str, Any]) -> Dict[str, List[int]]:
        """Map each move to its optimal section placement"""
        
        # Simple mapping based on outline guidance
        # In practice, this could be more sophisticated
        mapping = {}
        
        for section_key, section_data in outline.items():
            if isinstance(section_data, dict) and "content_guidance" in section_data:
                guidance = section_data["content_guidance"].lower()
                section_moves = []
                
                for i, move in enumerate(moves):
                    move_text = move.get("key_move_text", "").lower()
                    # Simple keyword matching - could be improved
                    if any(keyword in guidance for keyword in move_text.split()[:5]):
                        section_moves.append(i)
                        
                if section_moves:
                    mapping[section_key] = section_moves
                    
        return mapping
        
    def _map_citations_to_arguments(self, moves: List[Dict[str, Any]], literature: Dict[str, Any]) -> Dict[str, List[str]]:
        """Map citations to the arguments they best support"""
        
        citation_map = {}
        
        # Extract key papers from literature synthesis
        key_papers = []
        if "literature_overview" in literature:
            overview = literature["literature_overview"]
            if "primary_papers" in overview:
                for paper in overview["primary_papers"]:
                    key_papers.append({
                        "title": paper.get("title", ""),
                        "authors": paper.get("authors", []),
                        "key_points": paper.get("key_engagements", [])
                    })
                    
        # Map to moves (simplified - could use semantic matching)
        for i, move in enumerate(moves):
            move_citations = []
            move_content = move.get("refined_content", move.get("final_content", "")).lower()
            
            for paper in key_papers:
                # Check if paper themes appear in move
                for point in paper.get("key_points", []):
                    if isinstance(point, str) and point.lower() in move_content:
                        citation = f"{', '.join(paper['authors'])} - {paper['title']}"
                        move_citations.append(citation)
                        break
                        
            if move_citations:
                citation_map[f"move_{i}"] = move_citations
                
        return citation_map
        
    def _create_section_blueprints(
        self, 
        outline: Dict[str, Any], 
        moves: List[Dict[str, Any]], 
        transitions: Dict[str, str]
    ) -> List[Dict[str, Any]]:
        """Create detailed blueprints for each section"""
        
        blueprints = []
        
        for section_key, section_data in outline.items():
            if isinstance(section_data, dict) and "word_target" in section_data:
                blueprint = {
                    "section_key": section_key,
                    "title": section_data.get("title", section_key.replace("_", " ").title()),
                    "word_target": section_data["word_target"],
                    "content_guidance": section_data.get("content_guidance", ""),
                    "transition_in": transitions.get(f"into_{section_key}", ""),
                    "transition_out": transitions.get(f"from_{section_key}", ""),
                    "suggested_moves": self._map_moves_to_sections(moves, {section_key: section_data}).get(section_key, [])
                }
                blueprints.append(blueprint)
                
        return blueprints 