# WP4: Developer Experience Tools

## Overview

WP4 implements comprehensive developer experience tools for the philosophy pipeline, including enhanced CLI capabilities, structured logging, progress tracking, performance profiling, and API cost monitoring.

## Key Features Implemented

### 1. Enhanced CLI with Development Mode

The CLI now supports advanced development features:

```bash
# Enhanced development commands
python pipeline_cli.py run --phase 2.3 --dev --verbose --debug
python pipeline_cli.py run --phase 2.3 --dev --profile --track-costs --budget 50.0
python pipeline_cli.py run --phase 2.3 --interactive  # Step-by-step execution
```

**New Global Flags:**
- `--debug`: Enable debug-level logging with detailed output
- `--log-dir DIR`: Enable file logging to specified directory  
- `--log-format {console,json}`: Choose log output format

**Enhanced Run Command Flags:**
- `--dev`: Development mode with enhanced logging and monitoring
- `--interactive`: Interactive step-by-step execution with user prompts
- `--profile`: Enable performance profiling during execution
- `--track-costs`: Enable API cost tracking
- `--budget AMOUNT`: Set budget limit for cost tracking

### 2. Interactive Debug Command

```bash
# Debug specific phases with interactive execution
python pipeline_cli.py debug --phase 2.3
python pipeline_cli.py debug --step abstract_critic --break-at validation
```

Features:
- Interactive phase inspection before execution
- Step-by-step execution with pause points
- Breakpoint support (planned)
- Real-time state inspection

### 3. Performance Profiling Command

```bash
# Profile specific phases or full pipeline
python pipeline_cli.py profile --phase 2.3 --report performance_report.json
python pipeline_cli.py profile --full --report full_pipeline_profile.json
```

Features:
- Execution time tracking at multiple levels
- Memory usage monitoring (with psutil)
- API call latency measurement
- Bottleneck identification
- Detailed performance reports

### 4. Cost Tracking and Budget Management

```bash
# Monitor API costs and set budgets
python pipeline_cli.py cost status
python pipeline_cli.py cost report --period day --save daily_costs.json
python pipeline_cli.py cost budget --set 100.0
python pipeline_cli.py cost budget --alert 50.0 day warning
```

Features:
- Real-time API cost calculation
- Multi-provider support (Anthropic, OpenAI, Google)
- Budget alerts and warnings
- Cost reporting by time period
- Historical cost analysis

### 5. Real-time Monitoring Command

```bash
# Monitor pipeline execution in real-time
python pipeline_cli.py monitor --follow --metrics
```

Features:
- Real-time log tailing
- Live performance metrics (CPU, memory, cost)
- Active session monitoring
- System resource tracking

## Core Monitoring Modules

### 1. Structured Logging (`src/monitoring/logger.py`)

**Key Features:**
- Context-aware logging with phase/step/worker information
- Multiple output formats (console, JSON)
- Log rotation and archiving
- Development-friendly formatting
- Session tracking

**Usage Examples:**
```python
from src.monitoring import PipelineLogger, LogLevel

logger = PipelineLogger.get_logger(
    "phase_2_3",
    log_level=LogLevel.DEBUG,
    dev_mode=True,
    log_dir="outputs/logs"
)

logger.set_context(phase_id="2.3", step="abstract_critic")
logger.info("Starting abstract criticism")

with logger.context(operation="api_call"):
    logger.log_api_call("anthropic", "claude-3-sonnet", 1500, 800, 2.5)
```

### 2. Progress Tracking (`src/monitoring/progress.py`)

**Key Features:**
- Multi-level progress (pipeline → phase → step → subtask)
- Visual progress bars with time estimates
- Resume detection for interrupted runs
- Hierarchical progress organization

**Usage Examples:**
```python
from src.monitoring import ProgressTracker, ProgressLevel

tracker = ProgressTracker(
    save_dir="outputs/progress",
    show_progress_bars=True
)

tracker.create_progress("phase_2_3", "Phase 2.3", ProgressLevel.PHASE, 100)
tracker.start_progress("phase_2_3")
tracker.update_progress("phase_2_3", increment=25, message="Processing abstracts")
tracker.complete_progress("phase_2_3", success=True)
```

### 3. Performance Profiling (`src/monitoring/profiler.py`)

**Key Features:**
- Execution time tracking with context
- Memory usage monitoring (optional psutil)
- API latency measurement
- Operation-level profiling
- Comprehensive performance reports

**Usage Examples:**
```python
from src.monitoring import PerformanceProfiler

profiler = PerformanceProfiler(
    save_dir="outputs/profiling",
    enable_memory_monitoring=True
)

session_id = profiler.start_session("phase_2_3", "Phase 2.3 Execution")

with profiler.profile_operation("abstract_generation"):
    # Your code here
    pass

profiler.record_api_call(2.5, provider="anthropic", model="claude-3-sonnet")
profiler.end_session(session_id)

report = profiler.generate_report()
profiler.save_report("phase_2_3_profile.json")
```

### 4. API Cost Tracking (`src/monitoring/cost_tracker.py`)

**Key Features:**
- Multi-provider cost calculation
- Real-time budget monitoring
- Cost alerts and warnings
- Usage analytics and reporting
- Historical cost tracking

**Usage Examples:**
```python
from src.monitoring import CostTracker, APIProvider

tracker = CostTracker(
    save_dir="outputs/cost_tracking",
    default_budget_limit=100.0
)

cost = tracker.record_api_call(
    APIProvider.ANTHROPIC,
    "claude-3-sonnet",
    input_tokens=1500,
    output_tokens=800,
    latency=2.5,
    success=True
)

budget_status = tracker.get_budget_status()
cost_report = tracker.generate_cost_report()
```

## Integration with Phase Scripts

Phase scripts can integrate with monitoring by outputting structured monitoring data:

```python
import json
import os

def print_monitoring_data(data_type: str, **data):
    """Print monitoring data for pipeline runner"""
    if os.getenv('PIPELINE_MONITORING_ENABLED') == '1':
        monitoring_data = {"type": data_type, **data}
        print(f"[MONITORING]{json.dumps(monitoring_data)}")

# In your phase script:
print_monitoring_data("api_call", 
                     provider="anthropic", 
                     model="claude-3-sonnet",
                     input_tokens=1500, 
                     output_tokens=800,
                     latency=2.5,
                     success=True)

print_monitoring_data("progress_update",
                     increment=25,
                     message="Processed 25% of abstracts")
```

## Enhanced Pipeline Runner Integration

The `PipelineRunner` now automatically integrates monitoring when `dev_mode=True`:

**Automatic Features:**
- Enhanced logging with context
- Progress tracking for all phases
- Performance profiling integration
- API cost monitoring
- Error tracking and reporting

**Environment Variables Set by Runner:**
- `PIPELINE_DEV_MODE=1`: Indicates development mode
- `PIPELINE_MONITORING_ENABLED=1`: Enables monitoring features
- `PIPELINE_PROFILING_ENABLED=1`: Enables profiling
- `PIPELINE_COST_TRACKING_ENABLED=1`: Enables cost tracking

## Development Workflow Examples

### 1. Development Mode Execution
```bash
# Run with full development features
python pipeline_cli.py run --phase 2.3 \
    --dev \
    --verbose \
    --profile \
    --track-costs \
    --budget 25.0 \
    --log-dir outputs/logs
```

### 2. Interactive Debugging
```bash
# Debug with step-by-step execution
python pipeline_cli.py debug --phase 2.3
# Output: Phase info, dependency check, user confirmation prompts
```

### 3. Performance Analysis
```bash
# Profile a phase range with detailed report
python pipeline_cli.py profile --phases 2.1-2.4 --report phase2_profile.json
```

### 4. Cost Management
```bash
# Set budget and monitor costs
python pipeline_cli.py cost budget --set 50.0
python pipeline_cli.py cost budget --alert 25.0 day warning
python pipeline_cli.py run --phase 2.3 --track-costs
python pipeline_cli.py cost status
```

### 5. Real-time Monitoring
```bash
# Monitor active pipeline execution
python pipeline_cli.py monitor --follow --metrics
# Shows: CPU usage, memory, active costs, log output
```

## File Structure

```
src/monitoring/
├── __init__.py          # Module exports
├── logger.py            # Structured logging system
├── progress.py          # Progress tracking with visual bars
├── profiler.py          # Performance profiling
└── cost_tracker.py      # API cost tracking and budgeting

outputs/
├── logs/                # Log files (when --log-dir used)
├── profiling/           # Performance reports
├── cost_tracking/       # Cost data and reports
└── progress/            # Progress state (for resumption)
```

## Testing and Validation

Run the comprehensive test suite:

```bash
python test_monitoring.py
```

**Test Coverage:**
- ✅ PipelineLogger with context awareness
- ✅ ProgressTracker with visual indicators  
- ✅ CostTracker with budget alerts
- ✅ Enhanced CLI argument parsing
- ✅ Integration with existing pipeline

**CLI Validation:**
- ✅ All new command arguments parse correctly
- ✅ Help text is comprehensive and accurate
- ✅ Error handling works properly
- ✅ Monitoring integration doesn't break existing functionality

## Benefits for Developers

### 1. Enhanced Debugging
- Interactive execution with pause points
- Structured logging with searchable context
- Real-time progress feedback
- Detailed error reporting

### 2. Performance Optimization
- Identify bottlenecks across pipeline phases
- Track memory usage and API latency
- Compare performance across runs
- Optimize resource-intensive operations

### 3. Cost Management
- Real-time cost tracking prevents overruns
- Budget alerts enable proactive management
- Historical analysis guides optimization
- Multi-provider cost comparison

### 4. Development Efficiency
- Faster debugging with enhanced logging
- Progress indicators reduce uncertainty
- Automated monitoring reduces manual work
- Comprehensive reporting aids decision making

## Future Enhancements

**Planned Features:**
- Breakpoint debugging in individual steps
- Web-based monitoring dashboard
- Integration with external monitoring systems
- Advanced cost optimization recommendations
- Distributed execution monitoring

**Configuration Extensions:**
- Custom alert configurations
- Advanced logging rules
- Performance baseline comparisons
- Cost prediction models

## Summary

WP4 provides a comprehensive developer experience toolkit that significantly improves:

- **Debugging**: Interactive execution, structured logging, and detailed error reporting
- **Performance**: Real-time profiling, bottleneck identification, and optimization insights  
- **Cost Management**: Budget monitoring, usage tracking, and cost optimization
- **Developer Productivity**: Enhanced CLI, progress feedback, and automated monitoring

The implementation is backward-compatible and gracefully degrades when optional dependencies (like psutil) are unavailable, ensuring the pipeline works in all environments while providing enhanced capabilities where possible.