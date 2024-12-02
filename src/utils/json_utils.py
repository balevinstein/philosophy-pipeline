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
            print("Debug: Empty or whitespace input")
            return "{}"
            
        print(f"\nDebug: Cleaning JSON string starting with: {s[:100]}...")
            
        # First try direct parsing
        try:
            json.loads(s)
            print("Debug: Direct JSON parse successful")
            return s
        except json.JSONDecodeError:
            print("Debug: Direct parse failed, attempting cleanup")
            
            # If string contains ```json, extract content between backticks
            if "```json" in s:
                print("Debug: Found ```json marker")
                match = re.search(r'```json\n(.*?)\n```', s, re.DOTALL)
                if match:
                    s = match.group(1)
                    print("Debug: Extracted content between ```json markers")
                else:
                    print("Debug: Couldn't extract content between ```json markers")
                    s = s.replace("```json", "").replace("```", "")
                    
            # Try to find JSON-like content
            json_pattern = re.compile(r'(\{[\s\S]*\}|\[[\s\S]*\])')
            match = json_pattern.search(s)
            if match:
                print("Debug: Found JSON-like content")
                s = match.group(1)
            else:
                print("Debug: No JSON-like content found")
                return "{}"
                
            # Fix common JSON issues
            s = s.strip()
            
            # Try to complete incomplete JSON
            open_curly = s.count('{')
            close_curly = s.count('}')
            open_square = s.count('[')
            close_square = s.count(']')
            
            print(f"Debug: Brace counts - Open curly: {open_curly}, Close curly: {close_curly}, Open square: {open_square}, Close square: {close_square}")
            
            # Add missing closing braces/brackets
            while open_curly > close_curly:
                s += '}'
                close_curly += 1
                print("Debug: Added closing curly brace")
            while open_square > close_square:
                s += ']'
                close_square += 1
                print("Debug: Added closing square bracket")
            
            # Validate final result
            try:
                result = json.loads(s)
                print("Debug: Final JSON validation successful")
                return json.dumps(result)
            except json.JSONDecodeError as e:
                print(f"Debug: Final JSON validation failed: {e}")
                return "{}"
    
    def _complete_incomplete_json(self, s: str) -> str:
        """Attempt to complete incomplete JSON objects/arrays"""
        # Count opening/closing braces/brackets
        open_curly = s.count('{')
        close_curly = s.count('}')
        open_square = s.count('[')
        close_square = s.count(']')
        
        # Add missing closing braces/brackets
        s = s.rstrip()
        while open_curly > close_curly:
            s += '}'
            close_curly += 1
        while open_square > close_square:
            s += ']'
            close_square += 1
            
        return s

    def _extract_json_content(self, s: str) -> str:
        """Extract JSON content from string with better debugging"""
        json_match = re.search(r'(\{.*\}|\[.*\])', s, re.DOTALL)
        if not json_match:
            print("\nDebug: Failed to extract JSON content")
            print("Input string start:", s[:200])
            print("Input string end:", s[-200:])
            return "{}"
        return json_match.group(1)

    def _fix_common_json_issues(self, s: str) -> str:
        """Fix common JSON formatting issues"""
        # Remove empty responses
        if not s.strip():
            return "{}"
            
        # Handle non-JSON responses
        if s.startswith("I notice") or s.startswith("Without"):
            return "{}"

        # Remove markdown code blocks
        s = re.sub(r"```(?:json)?\n?(.*?)```", r"\1", s, flags=re.DOTALL)
        
        # Fix truncated objects
        open_count = s.count('{')
        close_count = s.count('}')
        if open_count > close_count:
            s = s + ('}' * (open_count - close_count))
    
    def _validate_json(self, s: str) -> str:
        """Validate JSON and provide debug info if invalid"""
        try:
            json.loads(s)
            return s
        except json.JSONDecodeError as e:
            print("\nJSON Validation Error:")
            print(f"Error: {str(e)}")
            print(f"Position: {e.pos}")
            print(f"Line: {e.lineno}, Column: {e.colno}")
            print("\nContext:")
            start = max(0, e.pos - 50)
            end = min(len(s), e.pos + 50)
            print(f"...{s[start:end]}...")
            raise

    def load_json(self, filename: str) -> Any:
        """Load and parse JSON file with better error reporting"""
        filepath = self.outputs_dir / filename
        print(f"Loading from: {filepath}")
        try:
            with open(filepath, 'r') as f:
                content = f.read()
                try:
                    return json.loads(content)
                except json.JSONDecodeError as e:
                    print(f"\nError parsing JSON from {filepath}")
                    return json.loads(self.clean_json_string(content))
        except FileNotFoundError as e:
            print(f"\nFile not found: {filepath}")
            raise

    def save_json(self, data: Any, filename: str) -> None:
        """Save data as JSON"""
        filepath = self.outputs_dir / filename
        print(f"Saving to: {filepath}")
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def test_json_cleaning(self):
        """Test JSON cleaning with common API response formats"""
        test_cases = [
            '```json\n{"key": "value"}\n```',
            'Here is the JSON:\n```\n{"key": "value"}\n```\n',
            'json```{"key": "value"}```',
            '{"key": "value"}',
            'Response: {"key": "value"} Note: some extra text',
            '\n\n{"key": "value"}\n\n'
        ]
        
        for i, case in enumerate(test_cases):
            print(f"\nTest case {i+1}:")
            print("Input:", case)
            cleaned = self.clean_json_string(case)
            print("Cleaned:", cleaned)
            try:
                parsed = json.loads(cleaned)
                print("Successfully parsed!")
            except json.JSONDecodeError as e:
                print(f"Failed to parse: {e}")
                raise e
            
    

if __name__ == "__main__":
    # Run tests if file is executed directly
    handler = JSONHandler()
    handler.test_json_cleaning()