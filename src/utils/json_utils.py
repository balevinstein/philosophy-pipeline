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
        """Enhanced JSON string cleaning with better error handling"""
        try:
            json.loads(s)
            return s
        except json.JSONDecodeError:
            s = re.sub(r"```(?:json)?\n?(.*?)```", r"\1", s, flags=re.DOTALL)
            s = self._extract_json_content(s)
            s = self._fix_common_json_issues(s)
            return self._validate_json(s)

    def _extract_json_content(self, s: str) -> str:
        """Extract JSON content from string"""
        json_match = re.search(r'(\{.*\}|\[.*\])', s, re.DOTALL)
        return json_match.group(1) if json_match else s

    def _fix_common_json_issues(self, s: str) -> str:
        """Fix common JSON formatting issues"""
        # Basic cleanup
        s = s.replace('\n', ' ').replace('\r', ' ')
        s = re.sub(r'\s+', ' ', s)
        
        # Handle commas in values by replacing with semicolons
        s = re.sub(r'([{,])\s*"([^"]+)":\s*"([^"]*),([^"]*)"', r'\1"\2":"\3;\4"', s)
        
        # Fix other common issues
        s = s.replace(',,', ',')
        s = re.sub(r',\s*([}\]])', r'\1', s)
        
        return s.strip()

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