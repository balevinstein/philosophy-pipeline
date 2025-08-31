"""
Philosophy Pipeline CLI Core Module

This module provides the core functionality for the unified CLI system,
including phase discovery, dependency validation, and pipeline execution.
"""

from .phase_registry import PhaseRegistry, PhaseMetadata
from .pipeline_runner import PipelineRunner
from .exceptions import PipelineError, PhaseError, DependencyError

__all__ = [
    'PhaseRegistry',
    'PhaseMetadata', 
    'PipelineRunner',
    'PipelineError',
    'PhaseError',
    'DependencyError'
]

__version__ = "1.0.0"