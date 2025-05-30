# src/utils/json_utils.py
import json
import re
import os
from pathlib import Path
from typing import Any, Optional, Tuple


class JSONHandler:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.outputs_dir = self.project_root / "outputs"
        os.makedirs(self.outputs_dir, exist_ok=True)

    def clean_json_string(self, s: str) -> str:
        """Enhanced JSON string cleaning with better pre/post processing"""
        if not s or s.isspace():
            return "{}"

        print("\nDebug: Cleaning JSON string starting with:", s[:100], "...")

        try:
            # First try direct parsing
            json.loads(s)
            return s
        except json.JSONDecodeError:
            print("Debug: Direct parsing failed, attempting cleaning...")

            # Step 1: Strip everything before first { or [ and after last } or ]
            s = self._extract_json_boundaries(s)
            print("Debug: Extracted JSON boundaries")

            # Step 2: Remove markdown code blocks
            s = re.sub(r"```(?:json)?\n?(.*?)```", r"\1", s, flags=re.DOTALL)
            print("Debug: Removed code blocks")

            # Step 3: Clean problematic characters in content fields
            print("Debug: Running pre-clean on content fields")
            s = self._pre_clean_content(s)
            print("Debug: After pre-cleaning:", s[:100])

            # Step 4: Fix escape characters and property names
            s = self._fix_json_formatting(s)
            print("Debug: Fixed escape characters and property names")

            # Step 5: Additional cleanup
            s = self._additional_cleanup(s)
            print("Debug: Performed additional JSON cleanup")

            # Step 6: Clean formal notation
            s = self._clean_formal_notation(s)
            print("Debug: Post-cleaning formal notation")

            # Count braces for debugging
            open_curly = s.count("{")
            close_curly = s.count("}")
            open_square = s.count("[")
            close_square = s.count("]")
            print(
                f"Debug: Brace counts - Open curly: {open_curly}, Close curly: {close_curly}, Open square: {open_square}, Close square: {close_square}"
            )

            try:
                # Try to parse the cleaned string
                json.loads(s)
                return s
            except json.JSONDecodeError as e:
                print(f"\nDebug: Standard cleaning failed: {str(e)}")
                # Attempt repair with more aggressive methods
                return self._attempt_json_repair(s)

    def _extract_json_boundaries(self, s: str) -> str:
        """Extract JSON content between first { or [ and last } or ]"""
        # Find the first { or [
        first_brace = s.find('{')
        first_bracket = s.find('[')
        
        if first_brace == -1 and first_bracket == -1:
            return s
            
        if first_brace == -1:
            start = first_bracket
            end_char = ']'
        elif first_bracket == -1:
            start = first_brace
            end_char = '}'
        else:
            if first_brace < first_bracket:
                start = first_brace
                end_char = '}'
            else:
                start = first_bracket
                end_char = ']'
        
        # Find the last matching closing character
        last = s.rfind(end_char)
        
        if last == -1 or last <= start:
            return s
            
        return s[start:last+1]

    def _pre_clean_content(self, s: str) -> str:
        """Clean problematic characters in content fields"""
        # Replace smart quotes and other Unicode quotes
        quote_replacements = {
            '"': '"', '"': '"', ''': "'", ''': "'",
            '«': '"', '»': '"', '„': '"', '"': '"'
        }
        for old, new in quote_replacements.items():
            s = s.replace(old, new)
            
        # Fix line breaks within quoted strings
        # This regex finds quoted strings and replaces newlines within them
        def fix_multiline(match):
            content = match.group(1)
            # Replace newlines with spaces
            content = content.replace('\n', ' ').replace('\r', ' ')
            # Collapse multiple spaces
            content = re.sub(r'\s+', ' ', content)
            return f'"{content}"'
        
        s = re.sub(r'"([^"]*)"', fix_multiline, s, flags=re.DOTALL)
        
        return s

    def _fix_json_formatting(self, s: str) -> str:
        """Fix common JSON formatting issues"""
        # Fix unescaped quotes inside strings (but not property quotes)
        # This is tricky - we need to identify quotes that are inside values
        lines = s.split('\n')
        fixed_lines = []
        
        for line in lines:
            # Simple heuristic: if line contains ": " it might have a value
            if '": "' in line:
                # Find the value part (after ": ")
                parts = line.split('": "', 1)
                if len(parts) == 2:
                    prefix = parts[0] + '": "'
                    value_part = parts[1]
                    # Find the closing quote (last quote before comma or brace)
                    if value_part.endswith('",'):
                        value = value_part[:-2]
                        suffix = '",'
                    elif value_part.endswith('"'):
                        value = value_part[:-1]
                        suffix = '"'
                    else:
                        value = value_part
                        suffix = ''
                    
                    # Escape any unescaped quotes in the value
                    value = value.replace('\\"', '§ESCAPED§')  # Temporarily mark already escaped quotes
                    value = value.replace('"', '\\"')  # Escape unescaped quotes
                    value = value.replace('§ESCAPED§', '\\"')  # Restore already escaped quotes
                    
                    line = prefix + value + suffix
            
            fixed_lines.append(line)
        
        s = '\n'.join(fixed_lines)
        
        # Fix trailing commas
        s = re.sub(r',(\s*[}\]])', r'\1', s)
        
        # Fix missing commas between array elements or object properties
        s = re.sub(r'"\s*\n\s*"', '",\n"', s)
        s = re.sub(r'}\s*\n\s*{', '},\n{', s)
        s = re.sub(r']\s*\n\s*\[', '],\n[', s)
        
        return s

    def _additional_cleanup(self, s: str) -> str:
        """Additional JSON cleanup steps"""
        # Remove comments
        s = re.sub(r"//.*?(?:\n|$)", "", s)
        s = re.sub(r"/\*.*?\*/", "", s, flags=re.DOTALL)
        
        # Fix missing quotes around property names
        # But be careful not to add quotes to already quoted properties
        s = re.sub(r'([{\,]\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', s)
        
        # Remove any 'undefined' values
        s = re.sub(r':\s*undefined\s*([,}])', r':null\1', s)
        
        # Fix common boolean/null issues
        s = re.sub(r':\s*True\s*([,}])', r':true\1', s)
        s = re.sub(r':\s*False\s*([,}])', r':false\1', s)
        s = re.sub(r':\s*None\s*([,}])', r':null\1', s)
        
        return s

    def _clean_formal_notation(self, s: str) -> str:
        """Clean formal notation that might break JSON"""
        # Be more careful with math notation - only replace if it's clearly breaking JSON
        # Don't replace math that's already inside quotes
        
        # First, protect already quoted content
        protected = []
        def protect_quoted(match):
            protected.append(match.group(0))
            return f"§PROTECTED{len(protected)-1}§"
        
        s = re.sub(r'"[^"]*"', protect_quoted, s)
        
        # Now clean unquoted math
        s = re.sub(r'\$\$(.*?)\$\$', r'"\1"', s, flags=re.DOTALL)
        s = re.sub(r'\$(.*?)\$', r'"\1"', s)
        
        # Restore protected content
        for i, content in enumerate(protected):
            s = s.replace(f"§PROTECTED{i}§", content)
        
        return s

    def _attempt_json_repair(self, s: str, max_attempts: int = 3) -> str:
        """Attempt to repair invalid JSON using progressively more aggressive methods"""
        for attempt in range(max_attempts):
            print(f"\nAttempting JSON repair (attempt {attempt + 1}/{max_attempts})")
            try:
                if attempt == 0:
                    # First attempt: balance braces and brackets
                    repaired = self._balance_braces(s)
                elif attempt == 1:
                    # Second attempt: remove problematic sections
                    repaired = self._remove_problematic_sections(s)
                else:
                    # Last attempt: extract core structure
                    repaired = self._extract_core_structure(s)

                # Validate the repaired JSON
                json.loads(repaired)
                print("JSON repair successful!")
                return repaired

            except Exception as e:
                print(f"Repair attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_attempts - 1:
                    print("Trying more aggressive repair...")

        # Last resort: return minimal valid structure
        return self._create_minimal_structure(s)

    def _balance_braces(self, s: str) -> str:
        """Balance braces and brackets"""
        # Count all braces and brackets
        stack = []
        for char in s:
            if char in '{[':
                stack.append(char)
            elif char in '}]':
                if stack and ((char == '}' and stack[-1] == '{') or (char == ']' and stack[-1] == '[')):
                    stack.pop()
        
        # Add missing closing characters
        while stack:
            opener = stack.pop()
            if opener == '{':
                s += '}'
            else:
                s += ']'
        
        return s

    def _remove_problematic_sections(self, s: str) -> str:
        """Remove sections that commonly cause issues"""
        # Remove any text after the last valid closing brace/bracket
        # Find the last } or ] that properly closes the structure
        depth = 0
        last_valid_close = -1
        
        for i, char in enumerate(s):
            if char in '{[':
                depth += 1
            elif char in '}]':
                depth -= 1
                if depth == 0:
                    last_valid_close = i
        
        if last_valid_close > 0:
            s = s[:last_valid_close + 1]
        
        return s

    def _extract_core_structure(self, s: str) -> str:
        """Try to extract just the core JSON structure"""
        # Look for the most common patterns
        # Try to find complete objects or arrays
        
        # Pattern 1: Object with quotes property (common in our outputs)
        quotes_match = re.search(r'{\s*"quotes"\s*:\s*\[(.*?)\]\s*}', s, re.DOTALL)
        if quotes_match:
            try:
                test = quotes_match.group(0)
                json.loads(test)
                return test
            except:
                pass
        
        # Pattern 2: Any complete object
        obj_match = re.search(r'{\s*"[^"]+"\s*:.*?}(?=\s*[,}\]])' , s, re.DOTALL)
        if obj_match:
            try:
                test = obj_match.group(0)
                json.loads(test)
                return test
            except:
                pass
        
        # Pattern 3: Simple array
        arr_match = re.search(r'\[\s*({.*?}(?:\s*,\s*{.*?})*)\s*\]', s, re.DOTALL)
        if arr_match:
            try:
                test = arr_match.group(0)
                json.loads(test)
                return test
            except:
                pass
        
        raise ValueError("Could not extract valid JSON structure")

    def _create_minimal_structure(self, s: str) -> str:
        """Create minimal valid structure based on content"""
        # Check what type of structure was likely intended
        if '"quotes"' in s and '[' in s:
            return '{"quotes": []}'
        elif '[' in s and s.strip().startswith('['):
            return '[]'
        else:
            return '{}'

    def load_json(self, filename: str) -> Any:
        """Load and parse JSON file with enhanced error handling"""
        filepath = self.outputs_dir / filename
        print(f"Loading from: {filepath}")
        try:
            with open(filepath, "r") as f:
                content = f.read()
                try:
                    return json.loads(content)
                except json.JSONDecodeError as e:
                    print(f"\nError parsing JSON from {filepath}: {e}")
                    cleaned = self.clean_json_string(content)
                    return json.loads(cleaned)
        except FileNotFoundError:
            print(f"\nFile not found: {filepath}")
            raise

    def save_json(self, data: Any, filename: str) -> None:
        """Save data as JSON with pretty printing"""
        filepath = self.outputs_dir / filename
        print(f"Saving to: {filepath}")
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
