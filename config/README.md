# Philosophy Pipeline Configuration System

This directory contains the unified configuration system for the Philosophy Pipeline project. The configuration system provides environment-aware settings management with validation and easy customization.

## Configuration Structure

```
config/
├── base.yaml              # Core configuration settings
├── environments/
│   ├── development.yaml   # Development environment overrides  
│   └── production.yaml    # Production environment settings
├── schema.yaml           # Configuration validation schema
├── conceptual_config.yaml # Legacy configuration (deprecated)
└── README.md             # This documentation
```

## Configuration Files

### base.yaml
Contains the core configuration settings that apply across all environments:
- Model configurations for all pipeline stages
- File path definitions
- Default parameters and settings
- Worker configurations
- API settings

### environments/development.yaml
Development environment specific overrides:
- Reduced token limits for faster iterations
- Higher temperature settings for creative development
- Smaller development cycles
- Debug mode enabled
- Development-specific paths

### environments/production.yaml
Production environment optimizations:
- Full token limits for comprehensive processing
- Conservative temperature settings for consistency
- Extended development cycles
- Performance monitoring enabled
- Production backup settings

### schema.yaml
Validation schema and rules:
- Structure validation rules
- Type and format requirements
- Environment-specific validation rules
- Environment variable requirements

## Usage

### Basic Usage

```python
from src.config import ConfigManager

# Initialize for development (default)
config_manager = ConfigManager()

# Or specify environment explicitly
config_manager = ConfigManager(environment="production")

# Load complete configuration
config = config_manager.load_config()

# Get model configuration for a specific stage
model_config = config_manager.get_model_config("idea_generation")

# Get path configuration
output_path = config_manager.get_path_config("base_dir")

# Get parameters
num_topics = config_manager.get_parameter("num_initial_topics")
cycles = config_manager.get_parameter("development_cycles.abstract_num_cycles")
```

### Environment Detection

The system automatically detects the environment in the following order:
1. `PHILOSOPHY_PIPELINE_ENV` environment variable
2. Environment specified in ConfigManager constructor
3. Defaults to "development"

### Configuration Override Hierarchy

Settings are merged in this order (later settings override earlier ones):
1. Base configuration (`base.yaml`)
2. Environment-specific configuration (`environments/{env}.yaml`)
3. Environment variables (where applicable)

## Environment Variables

Create a `.env` file from `.env.template` in the project root:

```bash
cp .env.template .env
```

### Required Variables
- `OPENAI_API_KEY`: OpenAI API key
- `ANTHROPIC_API_KEY`: Anthropic API key

### Optional Variables
- `PHILOSOPHY_PIPELINE_ENV`: Override environment ("development" or "production")
- `PHILOSOPHY_PIPELINE_CONFIG_PATH`: Override configuration directory path
- `PHILOSOPHY_PIPELINE_LOG_LEVEL`: Override logging level
- Many others (see `.env.template` for full list)

## Model Configurations

Each pipeline stage has its own model configuration:

```yaml
models:
  idea_generation:
    provider: anthropic
    model: claude-sonnet-4-20250514
    max_tokens: 8192
    temperature: 0.7
```

### Key Model Stages
- **Phase I**: `idea_generation`, `topic_evaluation`, `topic_selection`, etc.
- **Phase II**: `literature_processing`, `abstract_development`, `key_moves_development`, etc.
- **Phase III**: `section_writing`, `paper_integration`, etc.

## Path Management

All file paths are defined in the configuration:

```yaml
paths:
  base_dir: ./outputs
  papers_dir: ./papers
  generated_topics: conceptual_topics.json
  literature_output:
    synthesis:
      json: literature_synthesis.json
      markdown: literature_synthesis.md
```

Access paths using:
```python
# Simple paths
base_dir = config_manager.get_path_config("base_dir")

# Nested paths  
synthesis_json = config_manager.get_path_config("literature_output.synthesis.json")
```

## Parameters

Pipeline behavior is controlled by parameters:

```yaml
parameters:
  num_initial_topics: 6
  development_cycles:
    abstract_num_cycles: 3
    outline_num_cycles: 3
    key_moves_num_cycles: 3
  literature_processing:
    max_retries: 3
    min_wait: 4
    max_wait: 60
```

## Environment-Specific Settings

### Development Environment
- `debug: true` - Enable debugging
- `log_level: DEBUG` - Verbose logging
- Reduced token limits for faster development
- Fewer development cycles
- No backup creation

### Production Environment  
- `debug: false` - Disable debugging
- `log_level: INFO` - Standard logging
- Full token limits for comprehensive processing
- More development cycles for quality
- Backup creation enabled
- Performance monitoring

## Validation

Configuration validation includes:
- Required field checking
- Type validation (strings, integers, floats, booleans)
- Format validation (model names, file extensions)
- Range validation (token limits, temperature ranges)
- Business logic validation (min/max relationships)
- Environment-specific rules

Validate your configuration:
```python
config_manager = ConfigManager()
config = config_manager.load_config()  # Automatic validation

# Or validate explicitly
errors = config_manager.validate_config(config)
if errors:
    for error in errors:
        print(f"Validation error: {error}")
```

## Migration from Legacy Configuration

The system maintains backward compatibility with `conceptual_config.yaml`. To migrate:

1. Use the new configuration system alongside the legacy system
2. Gradually update code to use `ConfigManager` instead of direct YAML loading
3. Test thoroughly in development environment
4. Remove legacy configuration file when migration is complete

## Best Practices

### Development
- Use development environment for faster iterations
- Enable debug mode for troubleshooting
- Use smaller token limits to reduce API costs
- Test configuration changes thoroughly

### Production
- Use production environment for final runs
- Enable backups and monitoring
- Use conservative model settings for consistency
- Validate configuration before deployment

### Security
- Never commit `.env` files to version control
- Rotate API keys regularly
- Use environment variables for sensitive values
- Consider using secrets management systems in production

### Configuration Management
- Keep environment-specific settings minimal
- Document any custom configuration changes
- Test configuration in both environments
- Use validation to catch configuration errors early

## Troubleshooting

### Common Issues

1. **"Configuration directory not found"**
   - Ensure you're running from the project root directory
   - Check that `config/` directory exists
   - Verify `PHILOSOPHY_PIPELINE_CONFIG_PATH` if set

2. **"Required environment variable not set"**
   - Check that `.env` file exists and contains required API keys
   - Ensure `.env` file is in project root directory
   - Verify API key formats are correct

3. **"Model configuration not found for stage"**
   - Check that the stage name is correct
   - Ensure the model is defined in `models` or `workers` section
   - Verify environment-specific overrides aren't removing the model

4. **"Configuration validation failed"**
   - Check validation error messages for specific issues
   - Ensure all required fields are present
   - Verify data types and ranges are correct
   - Check environment-specific validation rules

### Debug Mode

Enable debug logging to troubleshoot configuration issues:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

config_manager = ConfigManager(environment="development")
config = config_manager.load_config()
```

### Validation Testing

Test your configuration:
```bash
python -c "
from src.config import ConfigManager
try:
    cm = ConfigManager()
    config = cm.load_config()
    print('Configuration loaded successfully!')
    print(f'Environment: {cm.get_current_environment()}')
    print(f'Debug enabled: {cm.is_debug_enabled()}')
except Exception as e:
    print(f'Configuration error: {e}')
"
```