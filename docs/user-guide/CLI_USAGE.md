# Philosophy Pipeline CLI Usage Guide

The Philosophy Pipeline CLI provides a unified interface for executing all phases of the philosophy pipeline project. This replaces the individual runner scripts with a single, comprehensive tool.

## Installation

No additional installation is required. The CLI uses the existing project structure and dependencies.

## Basic Usage

```bash
python3 pipeline_cli.py <command> [options]
```

## Available Commands

### 1. Run Commands

Execute pipeline phases individually or in groups:

```bash
# Run the complete pipeline
python3 pipeline_cli.py run --full

# Run a specific phase
python3 pipeline_cli.py run --phase 2.3

# Run a range of phases
python3 pipeline_cli.py run --phases 2.1-2.4

# Run specific phases (comma-separated)
python3 pipeline_cli.py run --phases 2.1,2.3,2.5

# Run with development mode
python3 pipeline_cli.py run --phase 2.3 --dev
```

### 2. Status Command

Check the current pipeline status:

```bash
# Show status in table format
python3 pipeline_cli.py status

# Show status in JSON format
python3 pipeline_cli.py status --json
```

### 3. List Command

List available phases:

```bash
# Simple phase listing
python3 pipeline_cli.py list

# Detailed phase information
python3 pipeline_cli.py list --detailed
```

### 4. Validate Command

Validate the pipeline environment:

```bash
python3 pipeline_cli.py validate
```

## Phase Identification

Phases are organized by major phase and sub-phase:

- **Phase I (Conceptual Development)**
  - 1.1: Conceptual Topic Generation
  - 1.2: Literature Research

- **Phase II (Framework and Analysis)**
  - 2.1: Literature Processing
  - 2.2: Framework Development
  - 2.3: Key Moves Development
  - 2.4: Detailed Outline
  - 2.5: Intelligent Consolidation
  - 2.6: Holistic Review
  - 2.7: Targeted Refinement
  - 2.8: Writing Optimization

- **Phase III (Writing and Integration)**
  - 3.1: Section Writing
  - 3.2: Paper Integration

## Global Options

```bash
# Use custom configuration file
python3 pipeline_cli.py --config path/to/config.yaml <command>

# Enable verbose output
python3 pipeline_cli.py --verbose <command>

# Show help
python3 pipeline_cli.py --help
python3 pipeline_cli.py <command> --help
```

## Dependency Management

The CLI automatically:
- Validates phase dependencies before execution
- Prevents execution of phases with unmet dependencies
- Provides clear error messages for missing dependencies

## Error Handling

The CLI provides comprehensive error handling:
- Invalid phase IDs are caught and reported
- Missing dependencies are clearly identified
- Execution errors are logged with context
- Proper exit codes are returned for scripting

## Examples

```bash
# Check what phases are available
python3 pipeline_cli.py list

# Validate environment before starting
python3 pipeline_cli.py validate

# Check current status
python3 pipeline_cli.py status

# Run phases 2.1 through 2.3 in sequence
python3 pipeline_cli.py run --phases 2.1-2.3

# Run the complete pipeline with verbose output
python3 pipeline_cli.py --verbose run --full
```

## Migration from Legacy Scripts

The CLI replaces the following scripts:
- `scripts/phases/run_phase_*.py` → `python3 pipeline_cli.py run --phase X.Y`
- Multiple individual executions → `python3 pipeline_cli.py run --phases X.Y-Z.W`

## Troubleshooting

1. **"No phases discovered"**: Check that you're running from the project root
2. **"Configuration file not found"**: Ensure `config/conceptual_config.yaml` exists
3. **"Module not found" errors**: Install required dependencies (openai, anthropic, etc.)
4. **Permission errors**: Ensure the script is executable (`chmod +x pipeline_cli.py`)

## Status Indicators

- ✅ **completed**: Phase has run successfully and outputs exist
- 🔶 **partial**: Some but not all expected outputs exist
- ⭕ **pending**: Phase has not been run or outputs are missing
- ❌ **failed**: Phase execution failed
- ❓ **unknown**: Status cannot be determined