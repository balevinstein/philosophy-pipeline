"""
Philosophy Pipeline Monitoring Module

This module provides comprehensive monitoring, logging, and profiling
capabilities for the philosophy pipeline including:

- Structured logging with context awareness
- Progress tracking with time estimates
- Performance profiling and bottleneck identification
- API cost monitoring and budgeting
"""

from .logger import PipelineLogger, LogLevel, LogContext
from .progress import ProgressTracker, ProgressLevel, get_global_tracker, set_global_tracker
from .profiler import PerformanceProfiler, ProfilerMetrics, get_global_profiler, set_global_profiler
from .cost_tracker import CostTracker, CostMetrics, APIProvider, BudgetAlert, get_global_cost_tracker, set_global_cost_tracker

__all__ = [
    'PipelineLogger',
    'LogLevel', 
    'LogContext',
    'ProgressTracker',
    'ProgressLevel',
    'get_global_tracker',
    'set_global_tracker',
    'PerformanceProfiler',
    'ProfilerMetrics',
    'get_global_profiler',
    'set_global_profiler',
    'CostTracker',
    'CostMetrics',
    'APIProvider',
    'BudgetAlert',
    'get_global_cost_tracker',
    'set_global_cost_tracker'
]

__version__ = "1.0.0"