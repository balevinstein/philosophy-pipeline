"""
Philosophy Pipeline Configuration Module

This module provides a unified, environment-aware configuration system that consolidates
all configuration settings across the philosophy pipeline project.

Key Components:
- ConfigManager: Main configuration management class
- ConfigValidator: Schema validation for configurations
- ConfigLoader: Environment-aware configuration loading

Usage:
    from src.config import ConfigManager
    
    config_manager = ConfigManager(environment="development")
    config = config_manager.load_config()
    model_config = config_manager.get_model_config("idea_generation")
"""

from .manager import ConfigManager
from .validator import ConfigValidator
from .loader import ConfigLoader

__all__ = ["ConfigManager", "ConfigValidator", "ConfigLoader"]

# Version information
__version__ = "1.0.0"
__author__ = "Philosophy Pipeline Team"