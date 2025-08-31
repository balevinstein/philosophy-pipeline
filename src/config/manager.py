"""
Configuration Manager

This module provides the main ConfigManager class that handles loading, validation,
and access to configuration settings across different environments.
"""

import os
import logging
from typing import Dict, Any, List, Optional, Union
from pathlib import Path

from .loader import ConfigLoader
from .validator import ConfigValidator


class ConfigManager:
    """
    Main configuration management class that provides environment-aware
    configuration loading, validation, and access methods.
    
    Features:
    - Environment-specific configuration loading (development/production)
    - Schema validation for configuration integrity
    - Easy access methods for common configuration patterns
    - Backward compatibility with existing configuration structure
    - Caching for performance optimization
    """
    
    def __init__(self, environment: str = "development", config_path: Optional[str] = None):
        """
        Initialize the ConfigManager.
        
        Args:
            environment: Target environment ("development" or "production")
            config_path: Optional override for configuration directory path
        """
        self.environment = self._determine_environment(environment)
        self.config_path = self._determine_config_path(config_path)
        self.loader = ConfigLoader(self.config_path)
        self.validator = ConfigValidator(self.config_path)
        
        self._config_cache: Optional[Dict[str, Any]] = None
        self._logger = logging.getLogger(__name__)
        
        # Log configuration initialization
        self._logger.info(f"ConfigManager initialized for environment: {self.environment}")
        self._logger.debug(f"Configuration path: {self.config_path}")
    
    def _determine_environment(self, environment: str) -> str:
        """
        Determine the target environment, with environment variable override.
        
        Args:
            environment: Requested environment
            
        Returns:
            Final environment to use
        """
        # Check for environment variable override
        env_override = os.getenv("PHILOSOPHY_PIPELINE_ENV")
        if env_override:
            self._logger.info(f"Environment overridden by env var: {env_override}")
            return env_override.lower()
        
        # Validate environment
        valid_environments = ["development", "production"]
        if environment.lower() not in valid_environments:
            self._logger.warning(f"Invalid environment '{environment}', defaulting to 'development'")
            return "development"
        
        return environment.lower()
    
    def _determine_config_path(self, config_path: Optional[str]) -> Path:
        """
        Determine the configuration directory path.
        
        Args:
            config_path: Optional override path
            
        Returns:
            Path to configuration directory
        """
        if config_path:
            return Path(config_path)
        
        # Check for environment variable override
        env_path = os.getenv("PHILOSOPHY_PIPELINE_CONFIG_PATH")
        if env_path:
            return Path(env_path)
        
        # Default to project config directory
        project_root = Path(__file__).parent.parent.parent  # Go up to project root
        return project_root / "config"
    
    def load_config(self, force_reload: bool = False) -> Dict[str, Any]:
        """
        Load the complete configuration for the current environment.
        
        Args:
            force_reload: Force reload even if cached configuration exists
            
        Returns:
            Complete configuration dictionary
            
        Raises:
            ConfigurationError: If configuration loading or validation fails
        """
        if self._config_cache and not force_reload:
            return self._config_cache
        
        try:
            # Load configuration using the loader
            config = self.loader.load_environment_config(self.environment)
            
            # Validate the configuration
            validation_errors = self.validator.validate_config(config, self.environment)
            if validation_errors:
                error_msg = f"Configuration validation failed: {validation_errors}"
                self._logger.error(error_msg)
                raise ConfigurationError(error_msg)
            
            # Cache the configuration
            self._config_cache = config
            
            self._logger.info(f"Configuration loaded successfully for environment: {self.environment}")
            return config
        
        except Exception as e:
            self._logger.error(f"Failed to load configuration: {str(e)}")
            raise ConfigurationError(f"Configuration loading failed: {str(e)}")
    
    def get_model_config(self, stage_name: str) -> Dict[str, Any]:
        """
        Get model configuration for a specific stage.
        
        Args:
            stage_name: Name of the stage (e.g., "idea_generation", "topic_evaluation")
            
        Returns:
            Model configuration dictionary
            
        Raises:
            ConfigurationError: If stage configuration is not found
        """
        config = self.load_config()
        
        # Check in models section first
        if "models" in config and stage_name in config["models"]:
            return config["models"][stage_name]
        
        # Check in workers section for backward compatibility
        if "workers" in config and stage_name in config["workers"]:
            return config["workers"][stage_name]
        
        # Check in api section as fallback
        if "api" in config:
            self._logger.warning(f"Using fallback API config for stage: {stage_name}")
            return config["api"]
        
        raise ConfigurationError(f"No configuration found for stage: {stage_name}")
    
    def get_path_config(self, path_key: str) -> str:
        """
        Get a file path configuration.
        
        Args:
            path_key: Key for the path configuration
            
        Returns:
            Full path string
            
        Raises:
            ConfigurationError: If path configuration is not found
        """
        config = self.load_config()
        
        if "paths" not in config:
            raise ConfigurationError("No paths configuration found")
        
        paths = config["paths"]
        
        # Handle nested path configurations (e.g., literature_output.synthesis.json)
        if "." in path_key:
            parts = path_key.split(".")
            current = paths
            for part in parts:
                if part not in current:
                    raise ConfigurationError(f"Path configuration not found: {path_key}")
                current = current[part]
            relative_path = current
        else:
            if path_key not in paths:
                raise ConfigurationError(f"Path configuration not found: {path_key}")
            relative_path = paths[path_key]
        
        # Construct full path
        if path_key == "base_dir" or path_key == "papers_dir":
            # These are base directories, return as-is
            return relative_path
        
        # Combine with base_dir for other paths
        base_dir = paths.get("base_dir", "./outputs")
        return os.path.join(base_dir, relative_path)
    
    def get_parameter(self, param_key: str, default: Any = None) -> Any:
        """
        Get a parameter configuration value.
        
        Args:
            param_key: Key for the parameter (supports nested keys with dots)
            default: Default value if parameter is not found
            
        Returns:
            Parameter value
        """
        config = self.load_config()
        
        if "parameters" not in config:
            return default
        
        # Handle nested parameter access (e.g., "development_cycles.abstract_num_cycles")
        if "." in param_key:
            parts = param_key.split(".")
            current = config["parameters"]
            for part in parts:
                if not isinstance(current, dict) or part not in current:
                    return default
                current = current[part]
            return current
        else:
            return config["parameters"].get(param_key, default)
    
    def get_environment_setting(self, setting_key: str, default: Any = None) -> Any:
        """
        Get an environment-specific setting.
        
        Args:
            setting_key: Key for the environment setting
            default: Default value if setting is not found
            
        Returns:
            Environment setting value
        """
        config = self.load_config()
        
        if "environment" not in config:
            return default
        
        return config["environment"].get(setting_key, default)
    
    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        """
        Validate a configuration dictionary against the schema.
        
        Args:
            config: Configuration dictionary to validate
            
        Returns:
            List of validation error messages (empty if valid)
        """
        return self.validator.validate_config(config, self.environment)
    
    def get_all_model_configs(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all model configurations.
        
        Returns:
            Dictionary mapping stage names to their model configurations
        """
        config = self.load_config()
        
        all_configs = {}
        
        # Add models configurations
        if "models" in config:
            all_configs.update(config["models"])
        
        # Add workers configurations for backward compatibility
        if "workers" in config:
            all_configs.update(config["workers"])
        
        return all_configs
    
    def is_debug_enabled(self) -> bool:
        """Check if debug mode is enabled."""
        return self.get_environment_setting("debug", False)
    
    def get_log_level(self) -> str:
        """Get the configured log level."""
        return self.get_environment_setting("log_level", "INFO")
    
    def is_cache_enabled(self) -> bool:
        """Check if caching is enabled."""
        return self.get_environment_setting("cache_enabled", True)
    
    def get_current_environment(self) -> str:
        """Get the current environment name."""
        return self.environment
    
    def reload_config(self) -> Dict[str, Any]:
        """
        Force reload the configuration from files.
        
        Returns:
            Reloaded configuration dictionary
        """
        return self.load_config(force_reload=True)


class ConfigurationError(Exception):
    """Exception raised for configuration-related errors."""
    pass