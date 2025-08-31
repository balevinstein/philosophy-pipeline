"""Memory optimization for large file processing and resource management."""

import gc
import logging
import mmap
import os
import psutil
import threading
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Optional, Dict, Any, List, Union
import weakref

logger = logging.getLogger(__name__)


@dataclass
class MemoryStats:
    """Memory usage statistics."""
    total_mb: float
    available_mb: float
    used_mb: float
    percent_used: float
    process_mb: float
    gc_collections: Dict[int, int]


class MemoryManager:
    """Memory optimization and monitoring for large file processing."""
    
    def __init__(
        self,
        memory_threshold_percent: float = 80.0,
        gc_threshold_mb: float = 100.0,
        enable_monitoring: bool = True,
        monitoring_interval: float = 5.0
    ):
        """Initialize memory manager.
        
        Args:
            memory_threshold_percent: Memory usage threshold for warnings
            gc_threshold_mb: Memory usage threshold for garbage collection
            enable_monitoring: Enable background memory monitoring
            monitoring_interval: Monitoring check interval in seconds
        """
        self.memory_threshold_percent = memory_threshold_percent
        self.gc_threshold_mb = gc_threshold_mb
        self.enable_monitoring = enable_monitoring
        self.monitoring_interval = monitoring_interval
        
        # Memory tracking
        self._memory_snapshots: List[MemoryStats] = []
        self._large_objects: List[weakref.ref] = []
        self._file_mappings: Dict[str, mmap.mmap] = {}
        
        # Monitoring thread
        self._monitoring_thread = None
        self._stop_monitoring = threading.Event()
        self._memory_lock = threading.Lock()
        
        # Statistics
        self.stats = {
            'gc_collections_forced': 0,
            'memory_warnings': 0,
            'peak_memory_mb': 0.0,
            'files_processed': 0,
            'bytes_processed': 0
        }
        
        if self.enable_monitoring:
            self.start_monitoring()

    def start_monitoring(self):
        """Start background memory monitoring."""
        if self._monitoring_thread is None or not self._monitoring_thread.is_alive():
            self._stop_monitoring.clear()
            self._monitoring_thread = threading.Thread(target=self._monitor_memory)
            self._monitoring_thread.daemon = True
            self._monitoring_thread.start()
            logger.info("Memory monitoring started")

    def stop_monitoring(self):
        """Stop background memory monitoring."""
        self._stop_monitoring.set()
        if self._monitoring_thread:
            self._monitoring_thread.join(timeout=2.0)
        logger.info("Memory monitoring stopped")

    def get_memory_stats(self) -> MemoryStats:
        """Get current memory statistics."""
        # System memory
        memory = psutil.virtual_memory()
        
        # Process memory
        process = psutil.Process()
        process_memory = process.memory_info()
        
        # Garbage collection stats
        gc_stats = {i: gc.get_count()[i] for i in range(3)}
        
        stats = MemoryStats(
            total_mb=memory.total / (1024 * 1024),
            available_mb=memory.available / (1024 * 1024),
            used_mb=memory.used / (1024 * 1024),
            percent_used=memory.percent,
            process_mb=process_memory.rss / (1024 * 1024),
            gc_collections=gc_stats
        )
        
        # Update peak memory
        if stats.process_mb > self.stats['peak_memory_mb']:
            self.stats['peak_memory_mb'] = stats.process_mb
            
        return stats

    def check_memory_usage(self) -> bool:
        """Check if memory usage is within safe limits."""
        stats = self.get_memory_stats()
        
        if stats.percent_used > self.memory_threshold_percent:
            self.stats['memory_warnings'] += 1
            logger.warning(
                f"High memory usage: {stats.percent_used:.1f}% "
                f"({stats.used_mb:.1f}MB used of {stats.total_mb:.1f}MB total)"
            )
            return False
            
        return True

    def force_garbage_collection(self, generation: Optional[int] = None) -> int:
        """Force garbage collection and return number of objects collected."""
        if generation is not None:
            collected = gc.collect(generation)
        else:
            collected = gc.collect()
            
        self.stats['gc_collections_forced'] += 1
        logger.info(f"Forced garbage collection: {collected} objects collected")
        
        return collected

    def optimize_memory(self):
        """Perform memory optimization operations."""
        # Force garbage collection
        self.force_garbage_collection()
        
        # Clean up file mappings
        self._cleanup_file_mappings()
        
        # Clean up weak references
        self._cleanup_weak_references()
        
        logger.info("Memory optimization completed")

    @contextmanager
    def stream_large_file(
        self, 
        file_path: Path, 
        chunk_size: int = 8192,
        use_mmap: bool = True
    ) -> Iterator[Union[Iterator[bytes], mmap.mmap]]:
        """Stream large file with memory optimization.
        
        Args:
            file_path: Path to the file
            chunk_size: Size of chunks to read (when not using mmap)
            use_mmap: Use memory mapping for efficient access
            
        Yields:
            File content iterator or memory map
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        file_size = file_path.stat().st_size
        self.stats['files_processed'] += 1
        self.stats['bytes_processed'] += file_size
        
        logger.info(f"Streaming file: {file_path} ({file_size / (1024*1024):.1f}MB)")
        
        # Check if we should use memory mapping for large files
        if use_mmap and file_size > 10 * 1024 * 1024:  # 10MB threshold
            try:
                with open(file_path, 'rb') as f:
                    with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                        # Store mapping for cleanup
                        mapping_key = str(file_path)
                        self._file_mappings[mapping_key] = mm
                        
                        try:
                            yield mm
                        finally:
                            # Cleanup
                            if mapping_key in self._file_mappings:
                                del self._file_mappings[mapping_key]
                                
            except (OSError, ValueError) as e:
                logger.warning(f"Could not memory map file {file_path}: {e}")
                # Fall back to chunk reading
                use_mmap = False
        
        if not use_mmap:
            def chunk_reader():
                with open(file_path, 'rb') as f:
                    while True:
                        chunk = f.read(chunk_size)
                        if not chunk:
                            break
                        yield chunk
                        
                        # Periodic memory check for very large files
                        if file_size > 100 * 1024 * 1024:  # 100MB
                            self._check_memory_and_gc()
            
            yield chunk_reader()

    @contextmanager
    def process_pdf_memory_optimized(self, pdf_path: Path):
        """Process PDF with memory optimization."""
        logger.info(f"Processing PDF with memory optimization: {pdf_path}")
        
        # Check initial memory
        initial_stats = self.get_memory_stats()
        
        try:
            # Yield control to PDF processing
            yield
            
        finally:
            # Clean up after PDF processing
            final_stats = self.get_memory_stats()
            memory_delta = final_stats.process_mb - initial_stats.process_mb
            
            if memory_delta > 50:  # More than 50MB increase
                logger.info(f"PDF processing increased memory by {memory_delta:.1f}MB")
                self.optimize_memory()

    def register_large_object(self, obj: Any, description: str = ""):
        """Register a large object for tracking."""
        weak_ref = weakref.ref(obj)
        self._large_objects.append(weak_ref)
        
        if description:
            logger.debug(f"Registered large object: {description}")

    def _monitor_memory(self):
        """Background memory monitoring loop."""
        while not self._stop_monitoring.is_set():
            try:
                stats = self.get_memory_stats()
                
                with self._memory_lock:
                    self._memory_snapshots.append(stats)
                    # Keep only recent snapshots
                    if len(self._memory_snapshots) > 100:
                        self._memory_snapshots = self._memory_snapshots[-100:]
                
                # Check for high memory usage
                if stats.percent_used > self.memory_threshold_percent:
                    logger.warning(f"High system memory usage: {stats.percent_used:.1f}%")
                    
                if stats.process_mb > self.gc_threshold_mb:
                    logger.info(f"Process memory usage: {stats.process_mb:.1f}MB")
                    self._check_memory_and_gc()
                
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Error in memory monitoring: {e}")
                time.sleep(self.monitoring_interval)

    def _check_memory_and_gc(self):
        """Check memory and perform garbage collection if needed."""
        stats = self.get_memory_stats()
        
        if stats.process_mb > self.gc_threshold_mb:
            logger.info(f"Process memory ({stats.process_mb:.1f}MB) above threshold, forcing GC")
            self.force_garbage_collection()

    def _cleanup_file_mappings(self):
        """Clean up file mappings."""
        to_remove = []
        for key, mapping in self._file_mappings.items():
            try:
                mapping.close()
                to_remove.append(key)
            except:
                pass  # Already closed
                
        for key in to_remove:
            del self._file_mappings[key]

    def _cleanup_weak_references(self):
        """Clean up dead weak references."""
        self._large_objects = [ref for ref in self._large_objects if ref() is not None]

    def get_memory_history(self, minutes: int = 10) -> List[MemoryStats]:
        """Get memory usage history."""
        cutoff_time = time.time() - (minutes * 60)
        
        with self._memory_lock:
            # For simplicity, return recent snapshots
            # In a real implementation, you'd filter by timestamp
            return self._memory_snapshots[-minutes*2:]  # Rough approximation

    def get_stats(self) -> Dict[str, Any]:
        """Get memory management statistics."""
        current_stats = self.get_memory_stats()
        
        return {
            **self.stats,
            'current_memory_mb': current_stats.process_mb,
            'memory_usage_percent': current_stats.percent_used,
            'tracked_objects': len([ref for ref in self._large_objects if ref() is not None]),
            'active_file_mappings': len(self._file_mappings)
        }

    def create_memory_report(self) -> str:
        """Create a detailed memory usage report."""
        stats = self.get_memory_stats()
        
        report = f"""
Memory Usage Report
==================
System Memory:
  Total: {stats.total_mb:.1f}MB
  Used: {stats.used_mb:.1f}MB ({stats.percent_used:.1f}%)
  Available: {stats.available_mb:.1f}MB

Process Memory:
  Current: {stats.process_mb:.1f}MB
  Peak: {self.stats['peak_memory_mb']:.1f}MB

Statistics:
  Files Processed: {self.stats['files_processed']}
  Bytes Processed: {self.stats['bytes_processed'] / (1024*1024*1024):.2f}GB
  GC Collections Forced: {self.stats['gc_collections_forced']}
  Memory Warnings: {self.stats['memory_warnings']}

Tracking:
  Active Large Objects: {len([ref for ref in self._large_objects if ref() is not None])}
  Active File Mappings: {len(self._file_mappings)}
"""
        return report

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.optimize_memory()
        if self.enable_monitoring:
            self.stop_monitoring()

    def __del__(self):
        """Cleanup on destruction."""
        try:
            self.stop_monitoring()
            self._cleanup_file_mappings()
        except:
            pass  # Ignore errors during cleanup