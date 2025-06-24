#!/usr/bin/env python3
"""Quick script to upgrade all Claude 3.5 Sonnet models to Claude 4 Sonnet and bump token limits"""

import yaml
import sys
from datetime import datetime

def upgrade_config(config_path='config/conceptual_config.yaml'):
    """Upgrade all Claude 3.5 Sonnet references to Claude 4 Sonnet and bump token limits"""
    
    # Read the current config
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Backup the original
    backup_path = f"{config_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    with open(backup_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    print(f"Created backup at: {backup_path}")
    
    # Count changes
    model_changes = 0
    token_changes = 0
    
    # Update model references
    old_model = "claude-3-5-sonnet-20241022"
    new_model = "claude-sonnet-4-20250514"
    
    def update_models_and_tokens(obj):
        nonlocal model_changes, token_changes
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == 'model' and value == old_model:
                    obj[key] = new_model
                    model_changes += 1
                    print(f"  Updated model: {key} = {new_model}")
                elif key == 'max_tokens' and isinstance(value, int) and value < 16000:
                    # Bump token limits to at least 16k, but preserve higher limits
                    old_tokens = value
                    if value == 4096:
                        obj[key] = 16000
                    elif value == 8192:
                        obj[key] = 16000
                    elif value < 16000:
                        obj[key] = 16000
                    # Keep existing high limits like 32000
                    if obj[key] != old_tokens:
                        token_changes += 1
                        print(f"  Updated tokens: {old_tokens} → {obj[key]}")
                else:
                    update_models_and_tokens(value)
        elif isinstance(obj, list):
            for item in obj:
                update_models_and_tokens(item)
    
    # Apply updates
    print("\nUpgrading models and token limits...")
    update_models_and_tokens(config)
    
    # Special case: the claude-3-7-sonnet typo in key_moves_critic
    if 'models' in config and 'key_moves_critic' in config['models']:
        if config['models']['key_moves_critic']['model'] == 'claude-3-7-sonnet-20250219':
            config['models']['key_moves_critic']['model'] = new_model
            model_changes += 1
            print(f"  Fixed typo in key_moves_critic model")
    
    # Save the updated config
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    print(f"\nUpgrade complete!")
    print(f"Made {model_changes} model changes")
    print(f"Made {token_changes} token limit changes")
    print(f"All Claude 3.5 Sonnet models upgraded to Claude 4 Sonnet")
    print(f"All token limits bumped to minimum 16k")
    
    return model_changes + token_changes

if __name__ == "__main__":
    upgrade_config() 