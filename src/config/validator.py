"""
Configuration Validator

This module provides configuration validation using schema definitions
and environment-specific validation rules.
"""

import logging
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
import re

from .loader import ConfigLoader


class ConfigValidator:
    """
    Configuration validator that validates configuration dictionaries
    against defined schemas and rules.
    
    Features:
    - Schema-based validation for configuration structure
    - Environment-specific validation rules
    - Type checking and format validation
    - Custom validation rules for specific fields
    - Detailed error reporting
    """
    
    def __init__(self, config_path: Path):
        """
        Initialize the ConfigValidator.
        
        Args:
            config_path: Path to the configuration directory
        """
        self.config_path = Path(config_path)
        self.loader = ConfigLoader(config_path)
        self._logger = logging.getLogger(__name__)
        
        # Load schema configuration
        try:
            self.schema_config = self.loader.load_schema_config()
            self.schema = self.schema_config.get("schema", {})
            self.validation_rules = self.schema_config.get("validation_rules", {})
            self.env_variables = self.schema_config.get("env_variables", {})
        except Exception as e:
            self._logger.warning(f"Could not load schema configuration: {str(e)}")
            self.schema_config = {}
            self.schema = {}
            self.validation_rules = {}
            self.env_variables = {}
    
    def validate_config(self, config: Dict[str, Any], environment: str = "development") -> List[str]:
        """
        Validate a configuration dictionary against the schema and rules.
        
        Args:
            config: Configuration dictionary to validate
            environment: Target environment for environment-specific rules
            
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        
        # Basic structure validation
        errors.extend(self._validate_structure(config))
        
        # Type and format validation
        errors.extend(self._validate_types_and_formats(config))
        
        # Environment-specific validation
        errors.extend(self._validate_environment_rules(config, environment))
        
        # Business logic validation
        errors.extend(self._validate_business_logic(config))
        
        # Environment variables validation
        errors.extend(self._validate_environment_variables())
        
        if errors:
            self._logger.warning(f"Configuration validation found {len(errors)} errors")
            for error in errors:
                self._logger.debug(f"Validation error: {error}")
        else:
            self._logger.debug("Configuration validation passed")
        
        return errors
    
    def _validate_structure(self, config: Dict[str, Any]) -> List[str]:
        """
        Validate the basic structure of the configuration.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            List of structural validation errors
        """
        errors = []
        
        if not self.schema:
            return errors  # No schema available for validation
        
        # Check required top-level keys
        required_keys = self.schema.get("required", [])
        for key in required_keys:
            if key not in config:
                errors.append(f"Missing required top-level key: {key}")
        
        return errors
    
    def _validate_types_and_formats(self, config: Dict[str, Any]) -> List[str]:
        """
        Validate types and formats of configuration values.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            List of type and format validation errors
        """
        errors = []
        
        # Validate models section
        if "models" in config:
            errors.extend(self._validate_models_section(config["models"]))
        
        # Validate paths section
        if "paths" in config:
            errors.extend(self._validate_paths_section(config["paths"]))
        
        # Validate parameters section
        if "parameters" in config:
            errors.extend(self._validate_parameters_section(config["parameters"]))
        
        # Validate API section
        if "api" in config:
            errors.extend(self._validate_api_section(config["api"]))
        
        # Validate workers section
        if "workers" in config:
            errors.extend(self._validate_workers_section(config["workers"]))
        
        # Validate environment section
        if "environment" in config:
            errors.extend(self._validate_environment_section(config["environment"]))
        
        return errors
    
    def _validate_models_section(self, models: Dict[str, Any]) -> List[str]:
        """Validate the models section."""
        errors = []
        
        for model_name, model_config in models.items():
            if not isinstance(model_config, dict):
                errors.append(f"Model '{model_name}' must be a dictionary")
                continue
            
            # Check required fields
            required_fields = ["provider", "model", "max_tokens", "temperature"]
            for field in required_fields:
                if field not in model_config:
                    errors.append(f"Model '{model_name}' missing required field: {field}")
            
            # Validate provider
            if "provider" in model_config:
                if model_config["provider"] not in ["anthropic", "openai"]:
                    errors.append(f"Model '{model_name}' has invalid provider: {model_config['provider']}")
            
            # Validate model name format
            if "model" in model_config:
                model_name_pattern = r"^(claude-|gpt-|o1-)"
                if not re.match(model_name_pattern, model_config["model"]):
                    errors.append(f"Model '{model_name}' has invalid model name format: {model_config['model']}")
            
            # Validate max_tokens
            if "max_tokens" in model_config:
                max_tokens = model_config["max_tokens"]
                if not isinstance(max_tokens, int) or max_tokens < 1000 or max_tokens > 200000:
                    errors.append(f"Model '{model_name}' has invalid max_tokens: {max_tokens}")
            
            # Validate temperature
            if "temperature" in model_config:
                temperature = model_config["temperature"]
                if not isinstance(temperature, (int, float)) or temperature < 0.0 or temperature > 1.0:
                    errors.append(f"Model '{model_name}' has invalid temperature: {temperature}")
        
        return errors
    
    def _validate_paths_section(self, paths: Dict[str, Any]) -> List[str]:
        """Validate the paths section."""
        errors = []
        
        # Check required paths
        required_paths = ["base_dir", "papers_dir"]
        for path_key in required_paths:
            if path_key not in paths:
                errors.append(f"Missing required path: {path_key}")
        
        # Validate path formats
        for path_key, path_value in paths.items():
            if isinstance(path_value, str):
                # Check for relative path format for directories
                if path_key in ["base_dir", "papers_dir"]:
                    if not path_value.startswith("./"):
                        errors.append(f"Path '{path_key}' should start with './': {path_value}")
                # Check for JSON file extensions
                elif path_key.endswith("_json") or "json" in path_key:
                    if not path_value.endswith(".json"):
                        errors.append(f"Path '{path_key}' should end with '.json': {path_value}")
        
        return errors
    
    def _validate_parameters_section(self, parameters: Dict[str, Any]) -> List[str]:
        """Validate the parameters section."""
        errors = []
        
        # Validate numeric parameters
        numeric_params = {
            "num_initial_topics": (1, 20),
            "cull_min": (1, None),
            "cull_max": (1, None),
            "max_selected_topics": (1, 10),
            "development_stages": (1, 10),
            "min_examples_per_topic": (1, None),
        }
        
        for param_name, (min_val, max_val) in numeric_params.items():
            if param_name in parameters:
                value = parameters[param_name]
                if not isinstance(value, int):
                    errors.append(f"Parameter '{param_name}' must be an integer: {value}")
                elif value < min_val:
                    errors.append(f"Parameter '{param_name}' must be at least {min_val}: {value}")
                elif max_val is not None and value > max_val:
                    errors.append(f"Parameter '{param_name}' must be at most {max_val}: {value}")
        
        # Validate max_technical_score
        if "max_technical_score" in parameters:
            score = parameters["max_technical_score"]
            if not isinstance(score, (int, float)) or score < 0.0 or score > 1.0:
                errors.append(f"Parameter 'max_technical_score' must be between 0.0 and 1.0: {score}")
        
        # Validate development_cycles
        if "development_cycles" in parameters:
            cycles = parameters["development_cycles"]
            if not isinstance(cycles, dict):
                errors.append("Parameter 'development_cycles' must be a dictionary")
            else:
                cycle_params = ["abstract_num_cycles", "outline_num_cycles", "key_moves_num_cycles"]
                for cycle_param in cycle_params:
                    if cycle_param in cycles:
                        value = cycles[cycle_param]
                        if not isinstance(value, int) or value < 1 or value > 10:
                            errors.append(f"Cycle parameter '{cycle_param}' must be between 1 and 10: {value}")
        
        # Validate literature_processing
        if "literature_processing" in parameters:
            lit_proc = parameters["literature_processing"]
            if not isinstance(lit_proc, dict):
                errors.append("Parameter 'literature_processing' must be a dictionary")
            else:
                if "max_retries" in lit_proc:
                    value = lit_proc["max_retries"]
                    if not isinstance(value, int) or value < 1 or value > 10:
                        errors.append(f"Literature processing 'max_retries' must be between 1 and 10: {value}")
        
        return errors
    
    def _validate_api_section(self, api: Dict[str, Any]) -> List[str]:
        """Validate the API section."""
        errors = []
        
        # Check required fields
        required_fields = ["model", "max_tokens", "temperature"]
        for field in required_fields:
            if field not in api:
                errors.append(f"API section missing required field: {field}")
        
        # Validate model name
        if "model" in api:
            model_pattern = r"^(claude-|gpt-|o1-)"
            if not re.match(model_pattern, api["model"]):
                errors.append(f"API model has invalid format: {api['model']}")
        
        return errors
    
    def _validate_workers_section(self, workers: Dict[str, Any]) -> List[str]:
        """Validate the workers section."""
        errors = []
        
        for worker_name, worker_config in workers.items():
            if not isinstance(worker_config, dict):
                errors.append(f"Worker '{worker_name}' must be a dictionary")
                continue
            
            # Check required fields
            required_fields = ["model", "max_tokens", "temperature"]
            for field in required_fields:
                if field not in worker_config:
                    errors.append(f"Worker '{worker_name}' missing required field: {field}")
        
        return errors
    
    def _validate_environment_section(self, environment: Dict[str, Any]) -> List[str]:
        """Validate the environment section."""
        errors = []
        
        # Check required fields
        required_fields = ["debug", "log_level", "cache_enabled"]
        for field in required_fields:
            if field not in environment:
                errors.append(f"Environment section missing required field: {field}")
        
        # Validate log_level
        if "log_level" in environment:
            valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            if environment["log_level"] not in valid_levels:
                errors.append(f"Invalid log_level: {environment['log_level']}")
        
        # Validate boolean fields
        boolean_fields = ["debug", "cache_enabled", "verbose_output", "performance_monitoring"]
        for field in boolean_fields:
            if field in environment and not isinstance(environment[field], bool):
                errors.append(f"Environment field '{field}' must be boolean: {environment[field]}")
        
        return errors
    
    def _validate_environment_rules(self, config: Dict[str, Any], environment: str) -> List[str]:
        """Validate environment-specific rules."""
        errors = []
        
        if environment not in self.validation_rules:
            return errors
        
        rules = self.validation_rules[environment]
        
        # Development-specific rules
        if environment == "development":
            if "required_debug" in rules and rules["required_debug"]:
                if not config.get("environment", {}).get("debug", False):
                    errors.append("Debug mode must be enabled in development environment")
        
        # Production-specific rules
        elif environment == "production":
            if "required_backups" in rules and rules["required_backups"]:
                if not config.get("outputs", {}).get("create_backups", False):
                    errors.append("Backups must be enabled in production environment")
            
            if "min_cycles" in rules:
                min_cycles = rules["min_cycles"]
                dev_cycles = config.get("parameters", {}).get("development_cycles", {})
                for cycle_type, cycle_count in dev_cycles.items():
                    if isinstance(cycle_count, int) and cycle_count < min_cycles:
                        errors.append(f"Production requires at least {min_cycles} {cycle_type}: {cycle_count}")
        
        return errors
    
    def _validate_business_logic(self, config: Dict[str, Any]) -> List[str]:
        """Validate business logic constraints."""
        errors = []
        
        # Check that cull_min <= cull_max
        params = config.get("parameters", {})
        cull_min = params.get("cull_min")
        cull_max = params.get("cull_max")
        if cull_min is not None and cull_max is not None:
            if cull_min > cull_max:
                errors.append(f"cull_min ({cull_min}) must be <= cull_max ({cull_max})")
        
        # Check that max_selected_topics is reasonable relative to num_initial_topics
        num_initial = params.get("num_initial_topics")
        max_selected = params.get("max_selected_topics")
        if num_initial is not None and max_selected is not None:
            if max_selected > num_initial:
                errors.append(f"max_selected_topics ({max_selected}) cannot exceed num_initial_topics ({num_initial})")
        
        return errors
    
    def _validate_environment_variables(self) -> List[str]:
        """Validate that required environment variables are set."""
        errors = []
        
        if not self.env_variables:
            return errors
        
        required_vars = self.env_variables.get("required", [])
        for var_name in required_vars:
            import os
            if not os.getenv(var_name):
                errors.append(f"Required environment variable not set: {var_name}")
        
        return errors
    
    def validate_model_config(self, model_config: Dict[str, Any], model_name: str) -> List[str]:
        """
        Validate a single model configuration.
        
        Args:
            model_config: Model configuration dictionary
            model_name: Name of the model for error reporting
            
        Returns:
            List of validation error messages
        """
        return self._validate_models_section({model_name: model_config})