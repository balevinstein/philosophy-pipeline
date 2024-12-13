# src/utils/json_utils.py
import json
import re
import os
from pathlib import Path
from typing import Any, Optional

class JSONHandler:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.outputs_dir = self.project_root / 'outputs'
        os.makedirs(self.outputs_dir, exist_ok=True)

    def clean_json_string(self, s: str) -> str:
        """Enhanced JSON string cleaning"""
        if not s or s.isspace():
            return "{}"
            
        print("\nDebug: Cleaning JSON string starting with:", s[:100], "...")
        
        try:
            # First try direct parsing
            json.loads(s)
            return s
        except json.JSONDecodeError:
            print("Debug: Direct parsing failed, attempting cleaning...")
            
            # Remove markdown code blocks
            s = re.sub(r"```(?:json)?\n?(.*?)```", r"\1", s, flags=re.DOTALL)
            print("Debug: Removed code blocks")
            
            # Clean problematic characters in content fields
            print("Debug: Running pre-clean on content fields")
            s = self._pre_clean_content(s)
            print("Debug: After pre-cleaning:", s[:100])
            
            # Extract JSON-like content
            s = self._extract_json_content(s)
            print("Debug: Found JSON-like content")
            
            # Fix escape characters and property names
            s = self._fix_json_formatting(s)
            print("Debug: Fixing escape characters and property names")
            
            # Additional cleanup
            s = self._additional_cleanup(s)
            print("Debug: Performing additional JSON cleanup")
            
            # Clean formal notation
            s = self._clean_formal_notation(s)
            print("Debug: Post-cleaning formal notation")
            
            # Count braces for debugging
            open_curly = s.count('{')
            close_curly = s.count('}')
            open_square = s.count('[')
            close_square = s.count(']')
            print(f"Debug: Brace counts - Open curly: {open_curly}, Close curly: {close_curly}, Open square: {open_square}, Close square: {close_square}")
            
            try:
                # Try to parse the cleaned string
                json.loads(s)
                return s
            except json.JSONDecodeError:
                print("\nDebug: Standard cleaning failed, attempting LLM repair")
                # Attempt repair with LLM if available
                return self._attempt_json_repair(s)

    def _pre_clean_content(self, s: str) -> str:
        """Clean problematic characters in content fields"""
        # Replace smart quotes
        s = s.replace('"', '"').replace('"', '"')
        # Remove line breaks in content
        s = re.sub(r':\s*"([^"]*)"', lambda m: ':"' + m.group(1).replace('\n', ' ') + '"', s)
        return s

    def _extract_json_content(self, s: str) -> str:
        """Extract JSON content from string"""
        # Look for array
        array_match = re.search(r'\[\s*\{.*\}\s*\]', s, re.DOTALL)
        if array_match:
            return array_match.group(0)
        # Look for object
        object_match = re.search(r'\{.*\}', s, re.DOTALL)
        if object_match:
            return object_match.group(0)
        return s

    def _fix_json_formatting(self, s: str) -> str:
        """Fix common JSON formatting issues"""
        # Fix unescaped quotes in strings
        s = re.sub(r'(?<!\\)"([^"]*)":', r'"\1":', s)
        # Fix trailing commas
        s = re.sub(r',(\s*[}\]])', r'\1', s)
        return s

    def _additional_cleanup(self, s: str) -> str:
        """Additional JSON cleanup steps"""
        # Remove comments
        s = re.sub(r'//.*?\n|/\*.*?\*/', '', s, flags=re.DOTALL)
        # Fix missing quotes around property names
        s = re.sub(r'(\{|\,)\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', s)
        return s

    def _clean_formal_notation(self, s: str) -> str:
        """Clean formal notation that might break JSON"""
        # Replace LaTeX-style math notation
        s = re.sub(r'\$\$(.*?)\$\$', r'"\1"', s, flags=re.DOTALL)
        s = re.sub(r'\$(.*?)\$', r'"\1"', s)
        return s

    def _attempt_json_repair(self, s: str, max_attempts: int = 3) -> str:
        """Attempt to repair invalid JSON using progressively more aggressive methods"""
        for attempt in range(max_attempts):
            print(f"\nAttempting JSON repair (attempt {attempt + 1}/{max_attempts})")
            try:
                # Start with basic structural fixes
                if attempt == 0:
                    repaired = self._basic_structural_repair(s)
                # Try removing problematic sections
                elif attempt == 1:
                    repaired = self._remove_problematic_sections(s)
                # Last resort: aggressive cleaning
                else:
                    repaired = self._aggressive_cleaning(s)
                
                # Validate the repaired JSON
                json.loads(repaired)
                return repaired
                
            except Exception as e:
                print(f"Repair attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_attempts - 1:
                    print("Trying again with error info...")
                else:
                    # Return best effort result
                    return self._create_empty_structure(s)

    def _basic_structural_repair(self, s: str) -> str:
        """Basic structural repairs"""
        # Balance brackets and braces
        open_curly = s.count('{')
        close_curly = s.count('}')
        open_square = s.count('[')
        close_square = s.count(']')
        
        s = s.rstrip()
        while open_curly > close_curly:
            s += '}'
            close_curly += 1
        while open_square > close_square:
            s += ']'
            close_square += 1
            
        return s

    def _remove_problematic_sections(self, s: str) -> str:
        """Remove sections likely to cause JSON parsing issues"""
        # Remove anything that looks like a comment
        s = re.sub(r'//.*?(?:\n|$)|/\*.*?\*/', '', s, flags=re.DOTALL)
        # Remove undefined values
        s = re.sub(r':\s*undefined\s*([,}])', r':null\1', s)
        return s

    def _aggressive_cleaning(self, s: str) -> str:
        """Aggressive JSON cleaning - last resort"""
        # Strip all whitespace and rebuild
        s = ''.join(s.split())
        # Ensure property names are quoted
        s = re.sub(r'([{,])([a-zA-Z_][a-zA-Z0-9_]*?):', r'\1"\2":', s)
        return s

    def _create_empty_structure(self, s: str) -> str:
        """Create empty structure matching original"""
        # If it looks like an array was intended
        if s.lstrip().startswith('['):
            return '[]'
        # Default to empty object
        return '{}'

    def load_json(self, filename: str) -> Any:
        """Load and parse JSON file with enhanced error handling"""
        filepath = self.outputs_dir / filename
        print(f"Loading from: {filepath}")
        try:
            with open(filepath, 'r') as f:
                content = f.read()
                try:
                    return json.loads(content)
                except json.JSONDecodeError as e:
                    print(f"\nError parsing JSON from {filepath}")
                    cleaned = self.clean_json_string(content)
                    return json.loads(cleaned)
        except FileNotFoundError:
            print(f"\nFile not found: {filepath}")
            raise

    def save_json(self, data: Any, filename: str) -> None:
        """Save data as JSON with pretty printing"""
        filepath = self.outputs_dir / filename
        print(f"Saving to: {filepath}")
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)