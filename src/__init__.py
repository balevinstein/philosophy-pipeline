"""
Philosophy Pipeline - AI-Driven Philosophy Paper Generator

A system that generates complete publishable-quality analytic philosophy papers 
through a structured multi-phase development pipeline.

This package provides the core functionality for generating philosophy papers
using large language models with sophisticated quality control mechanisms.
"""

__version__ = "1.0.0"
__author__ = "Philosophy Pipeline Team"
__email__ = "team@philosophy-pipeline.org"

# Core package imports
from . import pipeline
from . import config
from . import monitoring
from . import performance
from . import outputs
from . import utils
from . import phases

__all__ = [
    "pipeline",
    "config", 
    "monitoring",
    "performance",
    "outputs",
    "utils",
    "phases",
]
