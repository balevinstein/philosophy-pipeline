# CLI Reference

Complete reference for the Philosophy Pipeline command-line interface. The CLI provides a unified interface for all pipeline operations through the `pipeline_cli.py` script.

## Overview

```bash
python pipeline_cli.py [GLOBAL_OPTIONS] COMMAND [COMMAND_OPTIONS]
```

## Global Options

These options apply to all commands:

| Option | Description | Default |
|--------|-------------|---------|
| `--config`, `-c` | Path to configuration file | `config/conceptual_config.yaml` |
| `--verbose`, `-v` | Enable verbose output | Disabled |
| `--debug` | Enable debug output with detailed logging | Disabled |
| `--log-dir` | Directory for log files (enables file logging) | None |
| `--log-format` | Log output format: `console` or `json` | `console` |

### Examples
```bash
# Enable verbose output
python pipeline_cli.py --verbose run --full

# Use custom configuration
python pipeline_cli.py --config my_config.yaml run --phase 2.3

# Enable debug logging with file output
python pipeline_cli.py --debug --log-dir logs run --phases 2.1-2.4
```

## Commands

### `run` - Execute Pipeline Phases

Execute one or more phases of the philosophy pipeline.

```bash
python pipeline_cli.py run [OPTIONS] [EXECUTION_MODE]
```

#### Execution Modes (required, mutually exclusive)

| Mode | Description | Example |
|------|-------------|---------|
| `--full` | Run the complete pipeline | `run --full` |
| `--phase PHASE` | Run a specific phase | `run --phase 2.3` |
| `--phases PHASES` | Run multiple phases | `run --phases 2.1-2.4` or `run --phases 2.1,2.3,2.5` |

#### Run Options

| Option | Description |
|--------|-------------|
| `--dev` | Run in development mode with enhanced logging |
| `--interactive`, `-i` | Enable interactive step-by-step execution |
| `--profile` | Enable performance profiling |
| `--track-costs` | Enable API cost tracking |
| `--budget AMOUNT` | Set budget limit for cost tracking |

#### Examples

```bash
# Complete pipeline with monitoring
python pipeline_cli.py run --full --track-costs --profile

# Interactive execution
python pipeline_cli.py run --full --interactive

# Run specific phase in development mode
python pipeline_cli.py run --phase 2.3 --dev --profile

# Run phase range
python pipeline_cli.py run --phases 2.1-2.8

# Run specific phases with budget limit
python pipeline_cli.py run --phases 2.1,2.3,2.5 --track-costs --budget 50.0
```

#### Phase Identification

Phases are identified by their number:

- **Phase I: Topic Development**
  - `1.1` - Topic generation and evaluation
  - `1.2` - Literature research

- **Phase II: Framework & Content Development**  
  - `2.1` - Literature processing
  - `2.2` - Framework development
  - `2.3` - Key moves development
  - `2.4` - Detailed outline development
  - `2.5` - Intelligent consolidation
  - `2.6` - Holistic review
  - `2.7` - Targeted refinement
  - `2.8` - Writing context optimization

- **Phase III: Writing & Integration**
  - `3.1` - Section-by-section writing
  - `3.2` - Global integration & final paper

### `status` - Show Pipeline Status

Display the current status of all phases.

```bash
python pipeline_cli.py status [OPTIONS]
```

#### Options
| Option | Description |
|--------|-------------|
| `--json` | Output status in JSON format |

#### Examples
```bash
# Human-readable status
python pipeline_cli.py status

# JSON output for scripting
python pipeline_cli.py status --json
```

#### Status Symbols
- ✅ `completed` - Phase completed successfully
- 🔶 `partial` - Phase partially completed
- ⭕ `pending` - Phase not started
- ❌ `failed` - Phase failed
- ❓ `unknown` - Status unknown

### `list` - List Available Phases

Show all available phases with their descriptions.

```bash
python pipeline_cli.py list [OPTIONS]
```

#### Options
| Option | Description |
|--------|-------------|
| `--detailed` | Show detailed phase information including dependencies |

#### Examples
```bash
# Simple phase list
python pipeline_cli.py list

# Detailed information
python pipeline_cli.py list --detailed
```

### `validate` - Validate Environment

Check that the pipeline environment is properly configured.

```bash
python pipeline_cli.py validate [OPTIONS]
```

#### Options
| Option | Description |
|--------|-------------|
| `--phase PHASE` | Validate specific phase dependencies |

#### Examples
```bash
# Validate entire environment
python pipeline_cli.py validate

# Validate specific phase requirements
python pipeline_cli.py validate --phase 2.3
```

#### Validation Checks
- API key configuration
- Required dependencies
- File system permissions
- Configuration file validity
- Phase-specific requirements

### `debug` - Interactive Debugging

Interactive debugging and step-by-step execution.

```bash
python pipeline_cli.py debug [OPTIONS] [TARGET]
```

#### Target Options (required, mutually exclusive)
| Option | Description |
|--------|-------------|
| `--phase PHASE` | Debug a specific phase |
| `--step STEP` | Debug a specific step within a phase |

#### Options
| Option | Description |
|--------|-------------|
| `--break-at OPERATION` | Set breakpoint at specific operation |

#### Examples
```bash
# Debug specific phase
python pipeline_cli.py debug --phase 2.3

# Step-by-step execution
python pipeline_cli.py debug --phase 2.3 --break-at api_call
```

### `profile` - Performance Profiling

Run phases with performance profiling and generate reports.

```bash
python pipeline_cli.py profile [OPTIONS] [TARGET]
```

#### Target Options (required, mutually exclusive)
| Option | Description |
|--------|-------------|
| `--phase PHASE` | Profile a specific phase |
| `--phases PHASES` | Profile multiple phases |
| `--full` | Profile the complete pipeline |

#### Options
| Option | Description |
|--------|-------------|
| `--report FILE` | Generate profiling report file |

#### Examples
```bash
# Profile complete pipeline
python pipeline_cli.py profile --full

# Profile specific phase with report
python pipeline_cli.py profile --phase 2.3 --report profile_report.json

# Profile multiple phases
python pipeline_cli.py profile --phases 2.1-2.4
```

### `cost` - Cost Tracking and Reporting

Monitor and report API usage costs.

```bash
python pipeline_cli.py cost SUBCOMMAND [OPTIONS]
```

#### Subcommands

##### `status` - Show Current Cost Status
```bash
python pipeline_cli.py cost status
```

##### `report` - Generate Cost Report
```bash
python pipeline_cli.py cost report [OPTIONS]
```

| Option | Description | Default |
|--------|-------------|---------|
| `--period PERIOD` | Report period: `hour`, `day`, `week`, `month`, `total` | `day` |
| `--save FILE` | Save report to file | None |

##### `budget` - Manage Budget Settings
```bash
python pipeline_cli.py cost budget [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--set AMOUNT` | Set budget limit |
| `--alert THRESHOLD PERIOD TYPE` | Add budget alert |

#### Examples
```bash
# Check current budget status
python pipeline_cli.py cost status

# Generate daily cost report
python pipeline_cli.py cost report --period day --save daily_costs.json

# Set budget limit
python pipeline_cli.py cost budget --set 100.0

# Add budget alert
python pipeline_cli.py cost budget --alert 50.0 day warning
```

### `monitor` - Real-time Monitoring

Monitor pipeline execution in real-time.

```bash
python pipeline_cli.py monitor [OPTIONS]
```

#### Options
| Option | Description |
|--------|-------------|
| `--follow`, `-f` | Follow log output in real-time |
| `--metrics` | Show performance metrics |

#### Examples
```bash
# Monitor with metrics
python pipeline_cli.py monitor --metrics

# Follow logs in real-time
python pipeline_cli.py monitor --follow
```

### `outputs` - Manage Pipeline Outputs

Manage, archive, and export pipeline outputs.

```bash
python pipeline_cli.py outputs [ACTION] [OPTIONS]
```

#### Actions (required, mutually exclusive)

| Action | Description |
|--------|-------------|
| `--list` | List current and archived outputs |
| `--archive` | Archive current run outputs |
| `--clean COUNT` | Clean old archives, keeping COUNT most recent |
| `--export-paper FORMAT` | Export final paper in specified format |
| `--statistics` | Show comprehensive output statistics |

#### Options
| Option | Description |
|--------|-------------|
| `--output-file`, `-o` | Output file path (for export operations) |
| `--json` | Output results in JSON format |

#### Export Formats
- `md` - Markdown format
- `json` - JSON format with metadata
- `html` - HTML format  
- `txt` - Plain text format

#### Examples
```bash
# List all outputs
python pipeline_cli.py outputs --list

# Archive current run
python pipeline_cli.py outputs --archive

# Clean old archives, keep 5 most recent
python pipeline_cli.py outputs --clean 5

# Export paper as HTML
python pipeline_cli.py outputs --export-paper html --output-file paper.html

# Show statistics in JSON
python pipeline_cli.py outputs --statistics --json
```

## Advanced Usage Patterns

### Batch Processing
```bash
# Run multiple configurations
for config in config/*.yaml; do
    python pipeline_cli.py --config "$config" run --full
done
```

### Automated Testing
```bash
# Validate and run with cost tracking
python pipeline_cli.py validate && \
python pipeline_cli.py run --full --track-costs --budget 20.0
```

### Development Workflow
```bash
# Interactive development with profiling
python pipeline_cli.py run --phases 2.1-2.4 --interactive --profile --dev
```

### Production Pipeline
```bash
# Full production run with monitoring
python pipeline_cli.py run --full \
    --track-costs --budget 50.0 \
    --profile \
    --log-dir logs \
    --log-format json
```

## Exit Codes

The CLI uses standard exit codes:

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | General error |
| `130` | Interrupted by user (Ctrl+C) |

## Configuration Integration

All commands respect the configuration file settings. See [Configuration Guide](configuration.md) for details on:

- Model selection and parameters
- Phase-specific settings
- API rate limiting
- Output formatting
- Quality thresholds

## Getting Help

Use the `--help` flag with any command:

```bash
# General help
python pipeline_cli.py --help

# Command-specific help
python pipeline_cli.py run --help
python pipeline_cli.py cost --help
```

## Common Workflows

### First-Time Setup
```bash
python pipeline_cli.py validate
python pipeline_cli.py list --detailed
python pipeline_cli.py run --full --interactive
```

### Regular Use
```bash
python pipeline_cli.py run --full --track-costs
python pipeline_cli.py outputs --archive
python pipeline_cli.py cost report --period day
```

### Development  
```bash
python pipeline_cli.py debug --phase 2.3
python pipeline_cli.py profile --phase 2.3
python pipeline_cli.py monitor --metrics
```

### Production
```bash
python pipeline_cli.py validate
python pipeline_cli.py run --full --profile --track-costs --budget 100.0
python pipeline_cli.py outputs --export-paper html
```

For more advanced configurations and examples, see the [Examples Guide](../examples/)