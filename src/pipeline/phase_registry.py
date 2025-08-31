"""
Phase Registry for discovering and managing pipeline phases
"""

import importlib
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from .exceptions import InvalidPhaseError, DependencyError


@dataclass
class PhaseMetadata:
    """Metadata for a pipeline phase"""
    phase_id: str
    name: str
    description: str
    module_path: str
    script_path: str
    dependencies: List[str]
    outputs: List[str]
    phase_number: int
    sub_phase: int
    
    @property
    def full_id(self) -> str:
        """Get the full phase ID (e.g., '2.3')"""
        return f"{self.phase_number}.{self.sub_phase}"


class PhaseRegistry:
    """Registry for discovering and managing pipeline phases"""
    
    def __init__(self, project_root: str = None):
        """
        Initialize the phase registry
        
        Args:
            project_root: Root directory of the project. If None, auto-detects.
        """
        self.project_root = Path(project_root or self._detect_project_root())
        self.phases: Dict[str, PhaseMetadata] = {}
        self._discovered = False
        
    def _detect_project_root(self) -> str:
        """Auto-detect project root by looking for key files"""
        current = Path.cwd()
        while current.parent != current:  # Stop at filesystem root
            if (current / "src" / "phases").exists() and (current / "config").exists():
                return str(current)
            current = current.parent
        return str(Path.cwd())
    
    def discover_phases(self) -> Dict[str, PhaseMetadata]:
        """
        Discover all available phases by examining scripts and modules
        
        Returns:
            Dictionary mapping phase IDs to PhaseMetadata
        """
        if self._discovered:
            return self.phases
            
        scripts_dir = self.project_root / "scripts" / "phases"
        src_phases_dir = self.project_root / "src" / "phases"
        
        if not scripts_dir.exists():
            print(f"Warning: Scripts directory not found: {scripts_dir}")
            return {}
            
        # Pattern to extract phase info from script names
        script_pattern = re.compile(r'run_phase_(\d+)_(\d+)\.py')
        
        for script_file in scripts_dir.glob("run_phase_*.py"):
            match = script_pattern.match(script_file.name)
            if not match:
                continue
                
            phase_num = int(match.group(1))
            sub_phase = int(match.group(2))
            phase_id = f"{phase_num}.{sub_phase}"
            
            # Determine the module path based on phase structure
            module_path = self._determine_module_path(phase_num, sub_phase)
            
            # Create phase metadata
            metadata = PhaseMetadata(
                phase_id=phase_id,
                name=self._generate_phase_name(phase_num, sub_phase),
                description=self._extract_phase_description(script_file),
                module_path=module_path,
                script_path=str(script_file),
                dependencies=self._determine_dependencies(phase_num, sub_phase),
                outputs=self._determine_outputs(phase_num, sub_phase),
                phase_number=phase_num,
                sub_phase=sub_phase
            )
            
            self.phases[phase_id] = metadata
            
        self._discovered = True
        return self.phases
    
    def _determine_module_path(self, phase_num: int, sub_phase: int) -> str:
        """Determine the module path for a given phase"""
        phase_names = {
            1: "phase_one",
            2: "phase_two", 
            3: "phase_three"
        }
        
        phase_name = phase_names.get(phase_num, f"phase_{phase_num}")
        
        # For Phase 2 and 3, stages are organized differently
        if phase_num in [2, 3]:
            stage_num = sub_phase
            return f"src.phases.{phase_name}.stages.stage_{self._number_to_word(stage_num)}"
        else:
            return f"src.phases.{phase_name}"
    
    def _number_to_word(self, num: int) -> str:
        """Convert number to word (1->one, 2->two, etc.)"""
        words = {
            1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
            6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"
        }
        return words.get(num, str(num))
    
    def _generate_phase_name(self, phase_num: int, sub_phase: int) -> str:
        """Generate a human-readable name for the phase"""
        phase_names = {
            1: {1: "Conceptual Topic Generation", 2: "Literature Research"},
            2: {
                1: "Literature Processing",
                2: "Framework Development", 
                3: "Key Moves Development",
                4: "Detailed Outline",
                5: "Intelligent Consolidation",
                6: "Holistic Review",
                7: "Targeted Refinement", 
                8: "Writing Optimization"
            },
            3: {1: "Section Writing", 2: "Paper Integration"}
        }
        
        return phase_names.get(phase_num, {}).get(sub_phase, f"Phase {phase_num}.{sub_phase}")
    
    def _extract_phase_description(self, script_file: Path) -> str:
        """Extract description from script docstring or comments"""
        try:
            with open(script_file, 'r') as f:
                content = f.read()
                
            # Look for main function docstring
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'def main(' in line or 'def run_phase' in line:
                    # Look for docstring in following lines
                    for j in range(i+1, min(i+10, len(lines))):
                        if '"""' in lines[j]:
                            return lines[j].split('"""')[1].strip()
                        elif line.strip().startswith('print(') and 'Starting Phase' in line:
                            # Extract from print statement
                            match = re.search(r'"([^"]*)"', line)
                            if match:
                                return match.group(1)
                                
            return f"Pipeline phase execution"
            
        except Exception:
            return f"Phase execution"
    
    def _determine_dependencies(self, phase_num: int, sub_phase: int) -> List[str]:
        """Determine dependencies for a phase based on pipeline logic"""
        dependencies = []
        
        # Phase 1 dependencies
        if phase_num == 1 and sub_phase == 2:
            dependencies.append("1.1")
            
        # Phase 2 dependencies
        elif phase_num == 2:
            if sub_phase == 1:
                dependencies.extend(["1.1", "1.2"])
            else:
                dependencies.append(f"2.{sub_phase - 1}")
                if sub_phase == 2:
                    dependencies.append("2.1")
                    
        # Phase 3 dependencies  
        elif phase_num == 3:
            if sub_phase == 1:
                dependencies.extend([f"2.{i}" for i in range(1, 9)])
            else:
                dependencies.append("3.1")
                
        return dependencies
    
    def _determine_outputs(self, phase_num: int, sub_phase: int) -> List[str]:
        """Determine expected outputs for a phase"""
        output_map = {
            "1.1": ["final_selection.json"],
            "1.2": ["literature_research_papers.md"],
            "2.1": ["literature_readings.json", "literature_synthesis.json", "literature_synthesis.md"],
            "2.2": ["framework_development/framework.json", "framework_development/abstract/", "framework_development/outline/", "framework_development/key_moves/"],
            "2.3": ["key_moves_development/"],
            "2.4": ["detailed_outline/"],
            "2.5": ["consolidated_framework/"],
            "2.6": ["holistic_review/"],
            "2.7": ["refined_framework/"],
            "2.8": ["optimized_writing/"],
            "3.1": ["draft_sections/"],
            "3.2": ["final_paper/"]
        }
        
        phase_id = f"{phase_num}.{sub_phase}"
        return output_map.get(phase_id, [])
    
    def get_phase_metadata(self, phase_id: str) -> PhaseMetadata:
        """
        Get metadata for a specific phase
        
        Args:
            phase_id: Phase identifier (e.g., '2.3')
            
        Returns:
            PhaseMetadata for the requested phase
            
        Raises:
            InvalidPhaseError: If phase_id is not found
        """
        if not self._discovered:
            self.discover_phases()
            
        if phase_id not in self.phases:
            available = list(self.phases.keys())
            raise InvalidPhaseError(phase_id, available)
            
        return self.phases[phase_id]
    
    def validate_dependencies(self, phase_sequence: List[str]) -> bool:
        """
        Validate that all dependencies are satisfied for a sequence of phases
        
        Args:
            phase_sequence: List of phase IDs to execute in order
            
        Returns:
            True if all dependencies are satisfied
            
        Raises:
            DependencyError: If dependencies are not satisfied
        """
        if not self._discovered:
            self.discover_phases()
            
        completed_phases = set()
        
        for phase_id in phase_sequence:
            if phase_id not in self.phases:
                raise InvalidPhaseError(phase_id, list(self.phases.keys()))
                
            metadata = self.phases[phase_id]
            missing_deps = []
            
            for dep in metadata.dependencies:
                if dep not in completed_phases:
                    # Check if dependency will be satisfied by earlier phases in sequence
                    if dep not in phase_sequence[:phase_sequence.index(phase_id)]:
                        missing_deps.append(dep)
                        
            if missing_deps:
                raise DependencyError(phase_id, missing_deps)
                
            completed_phases.add(phase_id)
            
        return True
    
    def get_phase_module(self, phase_id: str) -> Any:
        """
        Import and return the module for a specific phase
        
        Args:
            phase_id: Phase identifier
            
        Returns:
            Imported module object
            
        Raises:
            InvalidPhaseError: If phase not found
            ImportError: If module cannot be imported
        """
        metadata = self.get_phase_metadata(phase_id)
        
        try:
            # Add project root to Python path if not already there
            project_root_str = str(self.project_root)
            if project_root_str not in sys.path:
                sys.path.insert(0, project_root_str)
                
            module = importlib.import_module(metadata.module_path)
            return module
            
        except ImportError as e:
            raise ImportError(f"Failed to import module for phase {phase_id}: {e}")
    
    def get_ordered_phases(self, start_phase: str = None, end_phase: str = None) -> List[str]:
        """
        Get phases in execution order, optionally filtered by range
        
        Args:
            start_phase: First phase to include (inclusive)
            end_phase: Last phase to include (inclusive)
            
        Returns:
            List of phase IDs in execution order
        """
        if not self._discovered:
            self.discover_phases()
            
        # Sort phases by phase number and sub-phase
        sorted_phases = sorted(
            self.phases.keys(),
            key=lambda x: (self.phases[x].phase_number, self.phases[x].sub_phase)
        )
        
        if start_phase:
            try:
                start_idx = sorted_phases.index(start_phase)
                sorted_phases = sorted_phases[start_idx:]
            except ValueError:
                raise InvalidPhaseError(start_phase, list(self.phases.keys()))
        
        if end_phase:
            try:
                end_idx = sorted_phases.index(end_phase)
                sorted_phases = sorted_phases[:end_idx + 1]
            except ValueError:
                raise InvalidPhaseError(end_phase, list(self.phases.keys()))
                
        return sorted_phases
    
    def list_phases(self) -> Dict[str, PhaseMetadata]:
        """List all available phases with their metadata"""
        if not self._discovered:
            self.discover_phases()
        return self.phases.copy()