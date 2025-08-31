#!/usr/bin/env python3
"""
Configuration System Usage Examples

This script demonstrates how to use the new unified configuration system
in the Philosophy Pipeline project.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(project_root))

def example_basic_usage():
    """Example of basic configuration usage."""
    print("=== Basic Configuration Usage ===")
    
    from src.config import ConfigManager
    
    # Initialize for development environment (default)
    config_manager = ConfigManager()
    
    # Load complete configuration
    config = config_manager.load_config()
    
    print(f"Current environment: {config_manager.get_current_environment()}")
    print(f"Debug enabled: {config_manager.is_debug_enabled()}")
    print(f"Log level: {config_manager.get_log_level()}")
    print(f"Cache enabled: {config_manager.is_cache_enabled()}")


def example_model_configuration():
    """Example of accessing model configurations."""
    print("\n=== Model Configuration Access ===")
    
    from src.config import ConfigManager
    
    config_manager = ConfigManager(environment="development")
    
    # Get specific model configuration
    idea_gen_config = config_manager.get_model_config("idea_generation")
    print(f"Idea generation model: {idea_gen_config['model']}")
    print(f"Max tokens: {idea_gen_config['max_tokens']}")
    print(f"Temperature: {idea_gen_config['temperature']}")
    
    # Get all model configurations
    all_models = config_manager.get_all_model_configs()
    print(f"Total available models: {len(all_models)}")


def example_path_configuration():
    """Example of accessing path configurations."""
    print("\n=== Path Configuration Access ===")
    
    from src.config import ConfigManager
    
    config_manager = ConfigManager(environment="production")
    
    # Get basic paths
    base_dir = config_manager.get_path_config("base_dir")
    papers_dir = config_manager.get_path_config("papers_dir")
    
    print(f"Base directory: {base_dir}")
    print(f"Papers directory: {papers_dir}")
    
    # Get nested paths
    synthesis_json = config_manager.get_path_config("literature_output.synthesis.json")
    print(f"Literature synthesis JSON: {synthesis_json}")


def example_parameter_access():
    """Example of accessing parameters."""
    print("\n=== Parameter Access ===")
    
    from src.config import ConfigManager
    
    config_manager = ConfigManager(environment="development")
    
    # Get basic parameters
    num_topics = config_manager.get_parameter("num_initial_topics")
    max_selected = config_manager.get_parameter("max_selected_topics")
    
    print(f"Number of initial topics: {num_topics}")
    print(f"Maximum selected topics: {max_selected}")
    
    # Get nested parameters
    abstract_cycles = config_manager.get_parameter("development_cycles.abstract_num_cycles")
    print(f"Abstract development cycles: {abstract_cycles}")
    
    # Get parameter with default value
    custom_param = config_manager.get_parameter("nonexistent_param", "default_value")
    print(f"Custom parameter (with default): {custom_param}")


def example_environment_comparison():
    """Example comparing different environments."""
    print("\n=== Environment Comparison ===")
    
    from src.config import ConfigManager
    
    # Development environment
    dev_manager = ConfigManager(environment="development")
    dev_config = dev_manager.load_config()
    
    # Production environment
    prod_manager = ConfigManager(environment="production")
    prod_config = prod_manager.load_config()
    
    print("Development vs Production:")
    print(f"  Debug mode: {dev_manager.is_debug_enabled()} vs {prod_manager.is_debug_enabled()}")
    print(f"  Log level: {dev_manager.get_log_level()} vs {prod_manager.get_log_level()}")
    
    # Compare model configurations
    dev_model = dev_manager.get_model_config("idea_generation")
    prod_model = prod_manager.get_model_config("idea_generation")
    
    print(f"  Idea generation max_tokens: {dev_model['max_tokens']} vs {prod_model['max_tokens']}")
    print(f"  Idea generation temperature: {dev_model['temperature']} vs {prod_model['temperature']}")


def example_apihandler_integration():
    """Example of APIHandler integration with new config system."""
    print("\n=== APIHandler Integration ===")
    
    from src.config import ConfigManager
    from src.utils.api import APIHandler
    
    # Method 1: Use ConfigManager directly
    config_manager = ConfigManager(environment="development")
    
    try:
        # This would work if API keys are available
        api_handler = APIHandler(config_manager=config_manager)
        print("✓ APIHandler created with ConfigManager")
        print(f"  Configuration loaded: {len(api_handler.config.keys())} sections")
    except ValueError as e:
        print(f"⚠ APIHandler creation failed (expected without API keys): {e}")
    
    # Method 2: Let APIHandler use automatic detection
    try:
        api_handler = APIHandler()
        print("✓ APIHandler created with automatic config detection")
    except ValueError as e:
        print(f"⚠ APIHandler creation failed (expected without API keys): {e}")


def example_validation():
    """Example of configuration validation."""
    print("\n=== Configuration Validation ===")
    
    from src.config import ConfigManager
    
    config_manager = ConfigManager(environment="development")
    config = config_manager.load_config()
    
    # Validate the configuration
    validation_errors = config_manager.validate_config(config)
    
    if not validation_errors:
        print("✓ Configuration validation passed")
    else:
        print(f"⚠ Configuration validation found {len(validation_errors)} issues:")
        for error in validation_errors:
            print(f"  - {error}")


def main():
    """Run all configuration examples."""
    print("Philosophy Pipeline Configuration System Examples")
    print("=" * 60)
    
    try:
        example_basic_usage()
        example_model_configuration()
        example_path_configuration()
        example_parameter_access()
        example_environment_comparison()
        example_apihandler_integration()
        example_validation()
        
        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
        
    except ImportError as e:
        print(f"ImportError: {e}")
        print("Make sure you're running from the project root with dependencies installed.")
    except Exception as e:
        print(f"Error running examples: {e}")
        print("Check that configuration files exist and are valid.")


if __name__ == "__main__":
    main()