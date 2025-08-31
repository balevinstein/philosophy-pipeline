"""Performance optimization module for philosophy pipeline.

This module provides:
- API response caching with intelligent invalidation
- Batch processing for multiple API calls
- Memory optimization for large file processing
- Request/response compression and connection pooling
"""

from .api_cache import APICache
from .batch_processor import BatchProcessor
from .memory_manager import MemoryManager

__all__ = ['APICache', 'BatchProcessor', 'MemoryManager']