"""
Performance Profiling System for Philosophy Pipeline

Provides comprehensive performance monitoring including execution time tracking,
memory usage monitoring, API latency measurement, and bottleneck identification.
"""

import functools
import json
import threading
import time
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    # Create mock psutil for basic functionality
    class MockProcess:
        def memory_info(self):
            return MockMemoryInfo()
        def cpu_percent(self):
            return 0.0
        def memory_percent(self):
            return 0.0
        def num_threads(self):
            return 1
    
    class MockMemoryInfo:
        def __init__(self):
            self.rss = 0
    
    class MockVirtualMemory:
        def __init__(self):
            self.percent = 0.0
            self.available = 0
            self.total = 0
    
    class MockPsutil:
        @staticmethod
        def Process():
            return MockProcess()
        @staticmethod
        def cpu_percent(interval=None):
            return 0.0
        @staticmethod
        def virtual_memory():
            return MockVirtualMemory()
    
    psutil = MockPsutil()

try:
    import resource
    RESOURCE_AVAILABLE = True
except ImportError:
    RESOURCE_AVAILABLE = False
from collections import defaultdict, deque
from contextlib import contextmanager
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Callable, Tuple
import traceback


@dataclass
class ProfilerMetrics:
    """Container for profiler metrics"""
    
    # Execution metrics
    total_execution_time: float = 0.0
    cpu_time: float = 0.0
    wall_time: float = 0.0
    
    # Memory metrics
    peak_memory_mb: float = 0.0
    memory_delta_mb: float = 0.0
    memory_samples: List[Tuple[float, float]] = None  # (timestamp, memory_mb)
    
    # API metrics
    api_calls: int = 0
    api_latency_total: float = 0.0
    api_latency_avg: float = 0.0
    api_latency_max: float = 0.0
    api_latency_min: float = float('inf')
    
    # Operation counts
    operations_count: Dict[str, int] = None
    operation_times: Dict[str, List[float]] = None
    
    # Error metrics
    errors_count: int = 0
    warnings_count: int = 0
    
    def __post_init__(self):
        if self.memory_samples is None:
            self.memory_samples = []
        if self.operations_count is None:
            self.operations_count = {}
        if self.operation_times is None:
            self.operation_times = defaultdict(list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        # Convert defaultdict to regular dict
        if isinstance(data['operation_times'], defaultdict):
            data['operation_times'] = dict(data['operation_times'])
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProfilerMetrics':
        """Create from dictionary"""
        if 'operation_times' in data and data['operation_times']:
            data['operation_times'] = defaultdict(list, data['operation_times'])
        return cls(**data)


@dataclass
class ProfilingSession:
    """A profiling session with context information"""
    session_id: str
    name: str
    start_time: float
    end_time: Optional[float] = None
    parent_session: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    metrics: Optional[ProfilerMetrics] = None
    
    def __post_init__(self):
        if self.metrics is None:
            self.metrics = ProfilerMetrics()
    
    @property
    def duration(self) -> Optional[float]:
        """Get session duration"""
        if self.end_time is None:
            return None
        return self.end_time - self.start_time
    
    @property
    def is_active(self) -> bool:
        """Check if session is still active"""
        return self.end_time is None


class PerformanceProfiler:
    """Comprehensive performance profiler for the philosophy pipeline"""
    
    def __init__(
        self,
        save_dir: Optional[Union[str, Path]] = None,
        auto_save: bool = True,
        memory_sampling_interval: float = 1.0,
        enable_memory_monitoring: bool = True,
        enable_cpu_monitoring: bool = True,
        max_memory_samples: int = 1000
    ):
        """
        Initialize the performance profiler
        
        Args:
            save_dir: Directory to save profiling results
            auto_save: Automatically save results
            memory_sampling_interval: Interval for memory sampling (seconds)
            enable_memory_monitoring: Enable memory usage monitoring
            enable_cpu_monitoring: Enable CPU usage monitoring
            max_memory_samples: Maximum number of memory samples to keep
        """
        self.save_dir = Path(save_dir) if save_dir else None
        self.auto_save = auto_save
        self.memory_sampling_interval = memory_sampling_interval
        self.enable_memory_monitoring = enable_memory_monitoring
        self.enable_cpu_monitoring = enable_cpu_monitoring
        self.max_memory_samples = max_memory_samples
        
        # Session management
        self.sessions: Dict[str, ProfilingSession] = {}
        self.session_stack: List[str] = []
        self.current_session: Optional[str] = None
        
        # Memory monitoring
        self._memory_monitor_thread = None
        self._memory_monitoring_active = False
        self._memory_samples = deque(maxlen=max_memory_samples)
        
        # Process reference for system metrics
        self._process = psutil.Process()
        
        # Thread safety
        self._lock = threading.Lock()
        
        # Create save directory
        if self.save_dir:
            self.save_dir.mkdir(parents=True, exist_ok=True)
        
        # Start memory monitoring if enabled
        if self.enable_memory_monitoring:
            self._start_memory_monitoring()
    
    def _start_memory_monitoring(self):
        """Start background memory monitoring"""
        if self._memory_monitor_thread and self._memory_monitor_thread.is_alive():
            return
        
        self._memory_monitoring_active = True
        self._memory_monitor_thread = threading.Thread(
            target=self._memory_monitor_loop,
            daemon=True
        )
        self._memory_monitor_thread.start()
    
    def _stop_memory_monitoring(self):
        """Stop background memory monitoring"""
        self._memory_monitoring_active = False
        if self._memory_monitor_thread and self._memory_monitor_thread.is_alive():
            self._memory_monitor_thread.join(timeout=2.0)
    
    def _memory_monitor_loop(self):
        """Memory monitoring loop"""
        while self._memory_monitoring_active:
            try:
                memory_mb = self._process.memory_info().rss / 1024 / 1024
                timestamp = time.time()
                
                with self._lock:
                    self._memory_samples.append((timestamp, memory_mb))
                    
                    # Update current session metrics
                    if self.current_session and self.current_session in self.sessions:
                        session = self.sessions[self.current_session]
                        session.metrics.memory_samples.append((timestamp, memory_mb))
                        session.metrics.peak_memory_mb = max(
                            session.metrics.peak_memory_mb,
                            memory_mb
                        )
                
                time.sleep(self.memory_sampling_interval)
                
            except Exception as e:
                # Silently continue on monitoring errors
                time.sleep(self.memory_sampling_interval)
    
    def start_session(
        self,
        session_id: str,
        name: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Start a new profiling session
        
        Args:
            session_id: Unique session identifier
            name: Human-readable session name
            context: Additional context information
            
        Returns:
            Session ID
        """
        with self._lock:
            # End current session if exists
            parent_session = self.current_session
            
            # Create new session
            session = ProfilingSession(
                session_id=session_id,
                name=name,
                start_time=time.time(),
                parent_session=parent_session,
                context=context or {}
            )
            
            # Record initial memory
            if self.enable_memory_monitoring:
                initial_memory = self._process.memory_info().rss / 1024 / 1024
                session.metrics.memory_samples.append((session.start_time, initial_memory))
            
            self.sessions[session_id] = session
            self.session_stack.append(session_id)
            self.current_session = session_id
            
            return session_id
    
    def end_session(self, session_id: str) -> Optional[ProfilingSession]:
        """
        End a profiling session
        
        Args:
            session_id: Session to end
            
        Returns:
            Completed session or None if not found
        """
        with self._lock:
            if session_id not in self.sessions:
                return None
            
            session = self.sessions[session_id]
            if not session.is_active:
                return session
            
            session.end_time = time.time()
            
            # Calculate final metrics
            self._calculate_session_metrics(session)
            
            # Update session stack
            if session_id in self.session_stack:
                self.session_stack.remove(session_id)
            
            # Update current session
            if self.current_session == session_id:
                self.current_session = self.session_stack[-1] if self.session_stack else None
            
            # Auto-save if enabled
            if self.auto_save:
                self._save_session(session)
            
            return session
    
    def _calculate_session_metrics(self, session: ProfilingSession):
        """Calculate final metrics for a session"""
        if session.duration is None:
            return
        
        metrics = session.metrics
        
        # Calculate memory delta
        if metrics.memory_samples:
            initial_memory = metrics.memory_samples[0][1]
            final_memory = metrics.memory_samples[-1][1]
            metrics.memory_delta_mb = final_memory - initial_memory
        
        # Calculate API latency statistics
        if metrics.api_calls > 0:
            metrics.api_latency_avg = metrics.api_latency_total / metrics.api_calls
            if metrics.api_latency_min == float('inf'):
                metrics.api_latency_min = 0.0
        
        # Calculate operation statistics
        for operation, times in metrics.operation_times.items():
            if times:
                metrics.operations_count[operation] = len(times)
        
        # Total execution time
        metrics.total_execution_time = session.duration
        metrics.wall_time = session.duration
    
    @contextmanager
    def profile_operation(self, operation_name: str, **context):
        """
        Context manager for profiling specific operations
        
        Args:
            operation_name: Name of the operation
            **context: Additional context
        """
        start_time = time.time()
        start_memory = None
        
        if self.enable_memory_monitoring:
            start_memory = self._process.memory_info().rss / 1024 / 1024
        
        try:
            yield
            
        finally:
            end_time = time.time()
            duration = end_time - start_time
            
            # Record operation metrics
            with self._lock:
                if self.current_session and self.current_session in self.sessions:
                    session = self.sessions[self.current_session]
                    session.metrics.operation_times[operation_name].append(duration)
                    
                    # Update memory if monitoring
                    if start_memory is not None:
                        end_memory = self._process.memory_info().rss / 1024 / 1024
                        memory_delta = end_memory - start_memory
                        session.metrics.memory_delta_mb += memory_delta
    
    def record_api_call(self, duration: float, **context):
        """
        Record an API call
        
        Args:
            duration: API call duration in seconds
            **context: Additional context (provider, model, etc.)
        """
        with self._lock:
            if self.current_session and self.current_session in self.sessions:
                session = self.sessions[self.current_session]
                metrics = session.metrics
                
                metrics.api_calls += 1
                metrics.api_latency_total += duration
                metrics.api_latency_max = max(metrics.api_latency_max, duration)
                metrics.api_latency_min = min(metrics.api_latency_min, duration)
    
    def record_error(self, error_type: str = "error", **context):
        """Record an error or warning"""
        with self._lock:
            if self.current_session and self.current_session in self.sessions:
                session = self.sessions[self.current_session]
                
                if error_type.lower() == "warning":
                    session.metrics.warnings_count += 1
                else:
                    session.metrics.errors_count += 1
    
    def profile_function(self, func: Callable) -> Callable:
        """
        Decorator to profile function execution
        
        Args:
            func: Function to profile
            
        Returns:
            Wrapped function
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            operation_name = f"{func.__module__}.{func.__name__}"
            
            with self.profile_operation(operation_name):
                return func(*args, **kwargs)
        
        return wrapper
    
    def get_session(self, session_id: str) -> Optional[ProfilingSession]:
        """Get session by ID"""
        return self.sessions.get(session_id)
    
    def get_active_sessions(self) -> List[ProfilingSession]:
        """Get all active sessions"""
        return [session for session in self.sessions.values() if session.is_active]
    
    def get_completed_sessions(self) -> List[ProfilingSession]:
        """Get all completed sessions"""
        return [session for session in self.sessions.values() if not session.is_active]
    
    def get_current_session(self) -> Optional[ProfilingSession]:
        """Get current active session"""
        if self.current_session:
            return self.sessions.get(self.current_session)
        return None
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system performance metrics"""
        try:
            cpu_percent = self._process.cpu_percent()
            memory_info = self._process.memory_info()
            memory_mb = memory_info.rss / 1024 / 1024
            memory_percent = self._process.memory_percent()
            
            # System-wide metrics
            system_cpu = psutil.cpu_percent(interval=0.1)
            system_memory = psutil.virtual_memory()
            
            return {
                "process": {
                    "cpu_percent": cpu_percent,
                    "memory_mb": memory_mb,
                    "memory_percent": memory_percent,
                    "threads": self._process.num_threads()
                },
                "system": {
                    "cpu_percent": system_cpu,
                    "memory_percent": system_memory.percent,
                    "memory_available_mb": system_memory.available / 1024 / 1024,
                    "memory_total_mb": system_memory.total / 1024 / 1024
                }
            }
        except Exception as e:
            return {"error": str(e)}
    
    def generate_report(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a comprehensive performance report
        
        Args:
            session_id: Specific session to report on (None = all sessions)
            
        Returns:
            Performance report
        """
        if session_id:
            sessions = [self.sessions.get(session_id)] if session_id in self.sessions else []
        else:
            sessions = list(self.sessions.values())
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_sessions": len(sessions),
            "system_metrics": self.get_system_metrics(),
            "sessions": [],
            "summary": {
                "total_execution_time": 0.0,
                "total_api_calls": 0,
                "total_errors": 0,
                "total_warnings": 0,
                "peak_memory_mb": 0.0,
                "operation_counts": defaultdict(int),
                "slowest_operations": []
            }
        }
        
        all_operation_times = defaultdict(list)
        
        for session in sessions:
            if session is None:
                continue
            
            session_report = {
                "session_id": session.session_id,
                "name": session.name,
                "duration": session.duration,
                "is_active": session.is_active,
                "parent_session": session.parent_session,
                "context": session.context,
                "metrics": session.metrics.to_dict()
            }
            
            report["sessions"].append(session_report)
            
            # Update summary
            if session.duration:
                report["summary"]["total_execution_time"] += session.duration
            
            metrics = session.metrics
            report["summary"]["total_api_calls"] += metrics.api_calls
            report["summary"]["total_errors"] += metrics.errors_count
            report["summary"]["total_warnings"] += metrics.warnings_count
            report["summary"]["peak_memory_mb"] = max(
                report["summary"]["peak_memory_mb"],
                metrics.peak_memory_mb
            )
            
            # Collect operation data
            for operation, times in metrics.operation_times.items():
                report["summary"]["operation_counts"][operation] += len(times)
                all_operation_times[operation].extend(times)
        
        # Calculate slowest operations
        operation_averages = []
        for operation, times in all_operation_times.items():
            if times:
                avg_time = sum(times) / len(times)
                max_time = max(times)
                operation_averages.append({
                    "operation": operation,
                    "count": len(times),
                    "avg_time": avg_time,
                    "max_time": max_time,
                    "total_time": sum(times)
                })
        
        # Sort by total time descending
        report["summary"]["slowest_operations"] = sorted(
            operation_averages,
            key=lambda x: x["total_time"],
            reverse=True
        )[:10]  # Top 10
        
        # Convert defaultdict to regular dict
        report["summary"]["operation_counts"] = dict(report["summary"]["operation_counts"])
        
        return report
    
    def _save_session(self, session: ProfilingSession):
        """Save session to disk"""
        if not self.save_dir:
            return
        
        try:
            session_file = self.save_dir / f"session_{session.session_id}.json"
            with open(session_file, 'w') as f:
                json.dump({
                    "session_id": session.session_id,
                    "name": session.name,
                    "start_time": session.start_time,
                    "end_time": session.end_time,
                    "duration": session.duration,
                    "parent_session": session.parent_session,
                    "context": session.context,
                    "metrics": session.metrics.to_dict()
                }, f, indent=2, default=str)
                
        except Exception as e:
            print(f"Warning: Failed to save profiling session: {e}")
    
    def save_report(self, filename: Optional[str] = None, session_id: Optional[str] = None):
        """Save performance report to file"""
        if not self.save_dir:
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"performance_report_{timestamp}.json"
        
        report = self.generate_report(session_id)
        
        try:
            report_file = self.save_dir / filename
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2, default=str)
                
            print(f"Performance report saved to: {report_file}")
            
        except Exception as e:
            print(f"Error saving performance report: {e}")
    
    def clear_completed_sessions(self):
        """Remove completed sessions from memory"""
        with self._lock:
            completed = [
                session_id for session_id, session in self.sessions.items()
                if not session.is_active
            ]
            
            for session_id in completed:
                del self.sessions[session_id]
            
            return len(completed)
    
    def cleanup(self):
        """Clean up resources"""
        # Stop memory monitoring
        self._stop_memory_monitoring()
        
        # End all active sessions
        with self._lock:
            active_sessions = [s.session_id for s in self.sessions.values() if s.is_active]
            for session_id in active_sessions:
                self.end_session(session_id)


# Global profiler instance
_global_profiler: Optional[PerformanceProfiler] = None


def get_global_profiler(**kwargs) -> PerformanceProfiler:
    """Get or create the global profiler"""
    global _global_profiler
    if _global_profiler is None:
        _global_profiler = PerformanceProfiler(**kwargs)
    return _global_profiler


def set_global_profiler(profiler: PerformanceProfiler):
    """Set the global profiler"""
    global _global_profiler
    _global_profiler = profiler


# Convenience decorators
def profile(operation_name: Optional[str] = None):
    """Decorator to profile function execution using global profiler"""
    def decorator(func):
        name = operation_name or f"{func.__module__}.{func.__name__}"
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            profiler = get_global_profiler()
            with profiler.profile_operation(name):
                return func(*args, **kwargs)
        
        return wrapper
    return decorator