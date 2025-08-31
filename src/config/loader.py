"""
Configuration Loader

This module handles loading and merging configuration files from different sources,
including base configuration, environment-specific overrides, and legacy compatibility.
"""

import os
import yaml
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from copy import deepcopy


class ConfigLoader:
    """
    Configuration loader that handles environment-aware configuration loading
    and merging from multiple sources.
    
    Features:
    - Base configuration loading from base.yaml
    - Environment-specific overrides from environments/{env}.yaml
    - Deep merging of configuration dictionaries
    - Legacy configuration compatibility
    - Error handling and logging
    """
    
    def __init__(self, config_path: Path):
        """
        Initialize the ConfigLoader.
        
        Args:
            config_path: Path to the configuration directory
        """
        self.config_path = Path(config_path)
        self._logger = logging.getLogger(__name__)
        
        # Validate configuration directory exists
        if not self.config_path.exists():
            raise ConfigurationLoadError(f"Configuration directory not found: {config_path}")
    
    def load_environment_config(self, environment: str) -> Dict[str, Any]:
        """
        Load configuration for a specific environment.
        
        This method loads the base configuration and then applies environment-specific
        overrides if they exist.
        
        Args:
            environment: Target environment ("development" or "production")
            
        Returns:
            Complete merged configuration dictionary
            
        Raises:
            ConfigurationLoadError: If configuration loading fails
        """
        try:
            # Load base configuration
            base_config = self._load_base_config()
            
            # Load environment-specific overrides
            env_config = self._load_environment_overrides(environment)
            
            # Merge configurations
            merged_config = self._deep_merge_configs(base_config, env_config)
            
            self._logger.info(f"Configuration loaded for environment: {environment}")
            self._logger.debug(f"Base config keys: {list(base_config.keys())}")
            self._logger.debug(f"Environment overrides: {list(env_config.keys())}")
            
            return merged_config
        
        except Exception as e:
            self._logger.error(f"Failed to load configuration: {str(e)}")
            raise ConfigurationLoadError(f"Configuration loading failed: {str(e)}")
    
    def _load_base_config(self) -> Dict[str, Any]:
        """
        Load the base configuration file.
        
        Returns:
            Base configuration dictionary
            
        Raises:
            ConfigurationLoadError: If base configuration cannot be loaded
        """
        base_config_path = self.config_path / "base.yaml"
        
        if not base_config_path.exists():
            # Try legacy configuration as fallback
            return self._load_legacy_config()
        
        try:
            with open(base_config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            if not isinstance(config, dict):
                raise ConfigurationLoadError("Base configuration must be a dictionary")
            
            self._logger.debug("Base configuration loaded successfully")
            return config
        
        except yaml.YAMLError as e:
            raise ConfigurationLoadError(f"Invalid YAML in base configuration: {str(e)}")
        except Exception as e:
            raise ConfigurationLoadError(f"Failed to load base configuration: {str(e)}")
    
    def _load_environment_overrides(self, environment: str) -> Dict[str, Any]:
        """
        Load environment-specific configuration overrides.
        
        Args:
            environment: Target environment
            
        Returns:
            Environment-specific configuration dictionary (empty if not found)
        """
        env_config_path = self.config_path / "environments" / f"{environment}.yaml"
        
        if not env_config_path.exists():
            self._logger.info(f"No environment-specific config found for: {environment}")
            return {}
        
        try:
            with open(env_config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            if config is None:
                return {}
            
            if not isinstance(config, dict):
                raise ConfigurationLoadError(f"Environment configuration must be a dictionary: {environment}")
            
            self._logger.debug(f"Environment overrides loaded for: {environment}")
            return config
        
        except yaml.YAMLError as e:
            raise ConfigurationLoadError(f"Invalid YAML in {environment} configuration: {str(e)}")
        except Exception as e:
            self._logger.warning(f"Failed to load environment config for {environment}: {str(e)}")
            return {}
    
    def _load_legacy_config(self) -> Dict[str, Any]:
        """
        Load legacy configuration from conceptual_config.yaml as fallback.
        
        Returns:
            Legacy configuration dictionary
            
        Raises:
            ConfigurationLoadError: If legacy configuration cannot be loaded
        """
        legacy_config_path = self.config_path / "conceptual_config.yaml"
        
        if not legacy_config_path.exists():
            raise ConfigurationLoadError("No base configuration or legacy configuration found")
        
        try:
            with open(legacy_config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            if not isinstance(config, dict):
                raise ConfigurationLoadError("Legacy configuration must be a dictionary")
            
            self._logger.warning("Using legacy configuration file - consider migrating to new format")
            return config
        
        except yaml.YAMLError as e:
            raise ConfigurationLoadError(f"Invalid YAML in legacy configuration: {str(e)}")
        except Exception as e:
            raise ConfigurationLoadError(f"Failed to load legacy configuration: {str(e)}")
    
    def _deep_merge_configs(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deep merge two configuration dictionaries.
        
        The override dictionary takes precedence over the base dictionary.
        Nested dictionaries are merged recursively.
        
        Args:
            base: Base configuration dictionary
            override: Override configuration dictionary
            
        Returns:
            Merged configuration dictionary
        """
        result = deepcopy(base)
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                # Recursively merge nested dictionaries
                result[key] = self._deep_merge_configs(result[key], value)
            else:
                # Override the value directly
                result[key] = deepcopy(value)
        
        return result
    
    def load_schema_config(self) -> Dict[str, Any]:
        """
        Load the configuration schema file.
        
        Returns:
            Schema configuration dictionary
            
        Raises:
            ConfigurationLoadError: If schema cannot be loaded
        """
        schema_path = self.config_path / "schema.yaml"
        
        if not schema_path.exists():
            raise ConfigurationLoadError("Schema configuration file not found")
        
        try:
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema = yaml.safe_load(f)
            
            if not isinstance(schema, dict):
                raise ConfigurationLoadError("Schema configuration must be a dictionary")
            
            return schema
        
        except yaml.YAMLError as e:
            raise ConfigurationLoadError(f"Invalid YAML in schema configuration: {str(e)}")
        except Exception as e:
            raise ConfigurationLoadError(f"Failed to load schema configuration: {str(e)}")
    
    def list_available_environments(self) -> list[str]:
        """
        List all available environment configurations.
        
        Returns:
            List of available environment names
        """
        environments_dir = self.config_path / "environments"
        
        if not environments_dir.exists():
            return []
        
        environments = []
        for file_path in environments_dir.glob("*.yaml"):
            if file_path.is_file():
                environments.append(file_path.stem)
        
        return sorted(environments)
    
    def config_file_exists(self, config_type: str, environment: Optional[str] = None) -> bool:
        """
        Check if a specific configuration file exists.
        
        Args:
            config_type: Type of configuration ("base", "schema", or "environment")
            environment: Environment name (required for environment type)
            
        Returns:
            True if the configuration file exists
        """
        if config_type == "base":
            return (self.config_path / "base.yaml").exists()
        elif config_type == "schema":
            return (self.config_path / "schema.yaml").exists()
        elif config_type == "environment":
            if not environment:
                raise ValueError("Environment name required for environment config type")
            return (self.config_path / "environments" / f"{environment}.yaml").exists()
        elif config_type == "legacy":
            return (self.config_path / "conceptual_config.yaml").exists()
        else:
            raise ValueError(f"Unknown configuration type: {config_type}")


class ConfigurationLoadError(Exception):
    """Exception raised for configuration loading errors."""
    pass