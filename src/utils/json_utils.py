# src/utils/json_utils.py
import json
import os
from typing import Any, Dict
from .api import load_config

class JSONHandler:
    def __init__(self):
        self.config = load_config()
        self.output_dir = self.config['paths']['outputs']
        
        # Create outputs directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def load_json(self, filename: str) -> Dict[str, Any]:
        """Load JSON from file"""
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'r') as f:
            return json.load(f)

    def save_json(self, data: Dict[str, Any], filename: str) -> None:
        """Save JSON to file"""
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def clean_json_string(self, s: str) -> str:
        """Clean a string to make it valid JSON"""
        # Remove any text after 'Note:'
        if "Note:" in s:
            s = s.split("Note:")[0]
        
        # Handle escaped characters properly
        s = s.replace("\\n", "\n").replace("\\'", "'")
        
        # Remove any other potential problematic characters
        import re
        s = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', s)
        
        return s.strip()