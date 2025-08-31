# Configuration Guide

The Philosophy Pipeline is highly configurable through YAML configuration files. This guide covers all configuration options and how to customize the system for your needs.

## Configuration Files

### Primary Configuration
- **`config/conceptual_config.yaml`** - Main pipeline configuration
- **`config/base.yaml`** - Base settings and defaults
- **`config/schema.yaml`** - Configuration schema validation

### Environment-Specific Configurations
- **`config/environments/development.yaml`** - Development settings
- **`config/environments/production.yaml`** - Production optimizations

## Configuration Structure

```yaml
# Main sections
api:           # API provider settings
  anthropic:   # Anthropic/Claude configuration
  openai:      # OpenAI configuration
  
phases:        # Phase-specific configurations
  phase_1:     # Topic generation settings
  phase_2:     # Framework development settings
  phase_3:     # Writing settings
  
models:        # Model selection and parameters
  default:     # Default model settings
  specialized: # Phase-specific model overrides
  
quality:       # Quality control settings
  heuristics:  # Hájek heuristics configuration
  standards:   # Analysis journal standards
  
pipeline:      # Pipeline-wide settings
  output:      # Output management
  monitoring:  # Logging and monitoring
```

## API Configuration

### Anthropic/Claude Settings

```yaml
api:
  anthropic:
    # Model selection
    default_model: "claude-sonnet-4"
    fallback_model: "claude-sonnet-3.5"
    
    # Rate limiting
    max_requests_per_minute: 50
    max_tokens_per_minute: 40000
    
    # Retry configuration
    max_retries: 3
    retry_delay: 1.0
    exponential_backoff: true
    
    # Temperature settings by task type
    temperatures:
      creative: 0.7      # Topic generation, creative writing
      analytical: 0.3    # Literature analysis, critique  
      structured: 0.1    # Outline generation, formatting
```

### OpenAI Settings

```yaml
api:
  openai:
    # Model for complex reasoning
    default_model: "o1-preview"
    fallback_model: "gpt-4"
    
    # When to use OpenAI vs Anthropic
    use_for_phases: ["2.3", "2.4"]  # Key moves, detailed outline
    
    # Rate limiting
    max_requests_per_minute: 30
    max_tokens_per_minute: 30000
```

## Phase Configuration

### Phase I: Topic Development

```yaml
phases:
  phase_1:
    topic_generation:
      # Number of topics to generate
      initial_topics: 20
      final_topics: 5
      
      # Topic criteria
      min_novelty_score: 7
      min_feasibility_score: 6
      
      # Word limits
      topic_description_words: 100
      topic_explanation_words: 300
    
    literature_search:
      # Search parameters
      max_papers_per_query: 10
      min_relevance_score: 0.7
      
      # Sources to search
      search_sources: ["arxiv", "philpapers", "jstor"]
```

### Phase II: Framework Development

```yaml
phases:
  phase_2:
    # Framework development (2.2)
    framework:
      # Iteration limits
      max_cycles: 3
      convergence_threshold: 0.8
      
      # Word targets
      abstract_words: 150
      outline_words: 800
      key_moves_words: 1200
    
    # Key moves development (2.3)  
    key_moves:
      # Development parameters
      moves_count: 3
      examples_per_move: 2
      literature_citations_per_move: 3
      
      # Quality thresholds
      min_argument_strength: 7
      min_literature_integration: 6
    
    # Quality control (2.5-2.7)
    quality_control:
      # Hájek heuristics
      enable_heuristics: true
      required_heuristic_tests: ["extreme_case", "self_undermining", "counterexample"]
      
      # Analysis standards
      enable_analysis_patterns: true
      require_immediate_engagement: true
      max_hedging_ratio: 0.1
```

### Phase III: Writing

```yaml
phases:
  phase_3:
    writing:
      # Target specifications
      target_words: 4000
      target_journal: "analysis"
      
      # Section allocation
      section_weights:
        introduction: 0.15
        main_argument: 0.60
        objections: 0.15
        conclusion: 0.10
      
      # Writing style
      tone: "conversational_rigorous"
      citation_style: "philosophy"
      examples_style: "concrete_cases"
```

## Model Configuration

### Default Model Settings

```yaml
models:
  default:
    provider: "anthropic"
    model: "claude-sonnet-4"
    temperature: 0.5
    max_tokens: 8000
    
    # Cost optimization
    use_caching: true
    cache_ttl: 3600
    
    # Quality settings
    top_p: 0.9
    frequency_penalty: 0.1
```

### Phase-Specific Model Overrides

```yaml
models:
  specialized:
    # Complex reasoning tasks
    "2.3":  # Key moves development
      provider: "openai"
      model: "o1-preview"
      temperature: 0.3
    
    # Creative tasks
    "1.1":  # Topic generation
      provider: "anthropic"
      model: "claude-sonnet-4"
      temperature: 0.8
    
    # Structured tasks
    "2.4":  # Detailed outline
      provider: "anthropic"
      model: "claude-sonnet-4"
      temperature: 0.2
```

## Quality Control Configuration

### Hájek Heuristics

```yaml
quality:
  heuristics:
    enabled: true
    
    # Required tests
    tests:
      extreme_case:
        enabled: true
        severity_threshold: 6
      
      self_undermining:
        enabled: true
        check_recursion: true
      
      counterexample:
        enabled: true
        require_response: true
      
      hidden_assumptions:
        enabled: true
        assumption_types: ["metaphysical", "epistemological", "semantic"]
      
      domain_transfer:
        enabled: true
        test_domains: ["ethics", "epistemology", "metaphysics"]
```

### Analysis Journal Standards

```yaml
quality:
  standards:
    analysis_patterns:
      enabled: true
      
      # Structural requirements
      require_hook_thesis_roadmap: true
      require_claim_example_analysis: true
      max_introduction_words: 600
      
      # Style requirements
      conversational_tone: true
      immediate_engagement: true
      example_driven: true
      
      # Anti-patterns
      max_hedging_ratio: 0.15
      avoid_both_sidesism: true
      avoid_equivocation: true
```

## Pipeline Settings

### Output Management

```yaml
pipeline:
  output:
    # Directory structure
    base_directory: "outputs"
    archive_directory: "outputs/archive"
    
    # File naming
    timestamp_format: "%Y-%m-%d_%H-%M-%S"
    include_run_id: true
    
    # Auto-archiving
    auto_archive: true
    max_current_runs: 3
    
    # Export formats
    default_export_format: "md"
    include_metadata: true
```

### Monitoring and Logging

```yaml
pipeline:
  monitoring:
    # Logging levels
    console_level: "INFO"
    file_level: "DEBUG"
    
    # Performance tracking
    enable_profiling: false
    profile_memory: true
    profile_api_calls: true
    
    # Cost tracking
    enable_cost_tracking: true
    budget_alerts: true
    default_budget: 100.0
    
    # Progress reporting
    show_progress_bars: true
    progress_update_interval: 10
```

## Environment-Specific Configuration

### Development Environment

```yaml
# config/environments/development.yaml
extends: "../base.yaml"

# Development overrides
models:
  default:
    temperature: 0.7  # Higher creativity for testing
    
pipeline:
  monitoring:
    console_level: "DEBUG"
    enable_profiling: true
    
phases:
  phase_2:
    framework:
      max_cycles: 2  # Faster iteration for development
```

### Production Environment

```yaml
# config/environments/production.yaml
extends: "../base.yaml"

# Production optimizations
models:
  default:
    use_caching: true
    temperature: 0.3  # More consistent output
    
pipeline:
  monitoring:
    console_level: "INFO"
    enable_cost_tracking: true
    
quality:
  standards:
    analysis_patterns:
      enabled: true  # Full quality checks
```

## Using Configuration Files

### Default Configuration
```bash
# Uses config/conceptual_config.yaml
python pipeline_cli.py run --full
```

### Custom Configuration
```bash
# Use specific config file
python pipeline_cli.py --config my_config.yaml run --full

# Use environment-specific config
python pipeline_cli.py --config config/environments/production.yaml run --full
```

### Configuration Validation

```bash
# Validate configuration syntax
python pipeline_cli.py validate

# Test specific configuration
python pipeline_cli.py --config my_config.yaml validate
```

## Configuration Examples

### High-Quality Academic Mode
```yaml
# Focus on maximum quality
quality:
  heuristics:
    enabled: true
    tests:
      extreme_case: { enabled: true, severity_threshold: 8 }
      counterexample: { enabled: true, require_response: true }
  
models:
  default:
    temperature: 0.2  # Very consistent
    
phases:
  phase_2:
    framework:
      max_cycles: 4  # More refinement
```

### Fast Development Mode
```yaml
# Optimize for speed
phases:
  phase_1:
    topic_generation:
      initial_topics: 10  # Fewer topics
  
  phase_2:
    framework:
      max_cycles: 2  # Less refinement
  
models:
  default:
    temperature: 0.6
    max_tokens: 4000  # Shorter responses
```

### Cost-Optimized Mode
```yaml
# Minimize API costs
models:
  default:
    use_caching: true
    model: "claude-sonnet-3.5"  # Cheaper model
    
phases:
  phase_2:
    key_moves:
      moves_count: 2  # Fewer moves
      examples_per_move: 1
      
pipeline:
  monitoring:
    enable_cost_tracking: true
    budget_alerts: true
```

## Dynamic Configuration

### Runtime Configuration Override

You can override specific settings at runtime:

```bash
# Override model temperature
PIPELINE_TEMP=0.8 python pipeline_cli.py run --phase 1.1

# Override word targets
PIPELINE_TARGET_WORDS=3000 python pipeline_cli.py run --phases 3.1,3.2

# Override quality settings
PIPELINE_MAX_CYCLES=5 python pipeline_cli.py run --phase 2.2
```

### Configuration Templates

Create reusable configuration templates:

```yaml
# templates/quick_test.yaml
extends: "../base.yaml"

phases:
  phase_2:
    framework: { max_cycles: 1 }
    key_moves: { moves_count: 2 }

# templates/high_quality.yaml  
extends: "../base.yaml"

quality:
  heuristics: { enabled: true }
  standards: { analysis_patterns: { enabled: true } }

phases:
  phase_2:
    framework: { max_cycles: 4 }
```

## Troubleshooting Configuration

### Common Configuration Issues

1. **Invalid YAML Syntax**
   ```bash
   python -c "import yaml; yaml.safe_load(open('config/my_config.yaml'))"
   ```

2. **Missing Required Fields**
   ```bash
   python pipeline_cli.py --config my_config.yaml validate
   ```

3. **API Key Issues**
   ```bash
   # Check .env file
   cat .env | grep API_KEY
   ```

4. **Model Availability**
   ```bash
   # Test API access
   python -c "
   import os
   from anthropic import Anthropic
   client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
   print('API access OK')
   "
   ```

### Configuration Debugging

Enable configuration debug mode:

```bash
python pipeline_cli.py --debug --config my_config.yaml validate
```

This shows:
- Configuration loading process
- Resolved settings after inheritance
- Validation results for each section

## Best Practices

1. **Use Environment Files**: Separate development and production configurations
2. **Version Control**: Keep configuration files in version control (but not `.env`)
3. **Validate Early**: Run validation before long pipeline executions
4. **Test Incrementally**: Test configuration changes on single phases first
5. **Monitor Costs**: Use budget limits and cost tracking in production
6. **Document Changes**: Comment configuration changes for team collaboration

For more examples, see the [Advanced Configuration Guide](../examples/advanced-configuration.md).