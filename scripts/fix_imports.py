#!/usr/bin/env python3
"""
Script to fix relative import issues in phase scripts.
"""

import os
import re
from pathlib import Path

def fix_relative_imports(file_path):
    """Fix relative imports in a single file."""
    print(f"Fixing imports in: {file_path}")
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check if file already has sys.path modification
    if 'sys.path.append' in content:
        print(f"  - Already has sys.path modification, skipping")
        return False
    
    # Replace relative imports with absolute imports
    old_pattern = r'from \.\.dev\.run_utils import'
    new_pattern = 'from scripts.dev.run_utils import'
    
    if old_pattern in content:
        content = re.sub(old_pattern, new_pattern, content)
        print(f"  - Fixed run_utils import")
    
    # Add sys.path modification if not present
    lines = content.split('\n')
    new_lines = []
    path_added = False
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        
        # Add sys.path modification after the first import or after the first line
        if not path_added and (line.strip().startswith('import ') or line.strip().startswith('from ') or i == 0):
            if i == 0 or (i > 0 and not lines[i-1].strip().startswith('import ') and not lines[i-1].strip().startswith('from ')):
                new_lines.append('')
                new_lines.append('# Fix import paths for moved script location')
                new_lines.append('import sys')
                new_lines.append('import os')
                new_lines.append("sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))")
                new_lines.append('')
                path_added = True
    
    if path_added:
        new_content = '\n'.join(new_lines)
        with open(file_path, 'w') as f:
            f.write(new_content)
        print(f"  - Added sys.path modification")
        return True
    else:
        print(f"  - No changes needed")
        return False

def main():
    """Main function to fix all phase scripts."""
    script_dir = Path(__file__).parent
    
    # Fix phase scripts
    phases_dir = script_dir / 'phases'
    if phases_dir.exists():
        print("\n=== Fixing Phase Scripts ===")
        for script_file in phases_dir.glob('*.py'):
            fix_relative_imports(script_file)
    
    print("\n=== Import Fixes Complete ===")
    print("All phase scripts should now have correct import paths.")

if __name__ == "__main__":
    main()

