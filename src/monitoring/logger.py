"""
Structured Logging System for Philosophy Pipeline

Provides context-aware logging with multiple output formats,
log rotation, and development-friendly features.
"""

import json
import logging
import logging.handlers
import os
import sys
import time
from contextlib import contextmanager
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional, Union
from threading import Lock


class LogLevel(Enum):
    """Log levels with severity ordering"""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


@dataclass
class LogContext:
    """Context information for structured logging"""
    phase_id: Optional[str] = None
    step: Optional[str] = None
    worker: Optional[str] = None
    operation: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, filtering out None values"""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


class PipelineLogger:
    """Enhanced logger with structured logging and context awareness"""
    
    _instances = {}
    _lock = Lock()
    
    def __init__(
        self,
        name: str = "pipeline",
        log_level: LogLevel = LogLevel.INFO,
        log_dir: Optional[Union[str, Path]] = None,
        console_output: bool = True,
        json_output: bool = False,
        dev_mode: bool = False
    ):
        """
        Initialize the pipeline logger
        
        Args:
            name: Logger name
            log_level: Minimum log level
            log_dir: Directory for log files (None = no file logging)
            console_output: Enable console output
            json_output: Use JSON format for structured logging
            dev_mode: Enable development mode features
        """
        self.name = name
        self.log_level = log_level
        self.log_dir = Path(log_dir) if log_dir else None
        self.console_output = console_output
        self.json_output = json_output
        self.dev_mode = dev_mode
        
        # Create underlying logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level.value)
        
        # Clear any existing handlers
        self.logger.handlers.clear()
        
        # Context stack for nested operations
        self._context_stack = []
        self._current_context = LogContext()
        
        # Setup handlers
        self._setup_handlers()
        
        # Session tracking
        self._session_id = self._generate_session_id()
        
    @classmethod
    def get_logger(
        cls,
        name: str = "pipeline",
        **kwargs
    ) -> 'PipelineLogger':
        """Get or create a logger instance (singleton pattern)"""
        with cls._lock:
            if name not in cls._instances:
                cls._instances[name] = cls(name, **kwargs)
            return cls._instances[name]
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"session_{timestamp}_{os.getpid()}"
    
    def _setup_handlers(self):
        """Setup logging handlers"""
        # Console handler
        if self.console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.log_level.value)
            
            if self.json_output:
                console_handler.setFormatter(self._create_json_formatter())
            else:
                console_handler.setFormatter(self._create_console_formatter())
                
            self.logger.addHandler(console_handler)
        
        # File handlers
        if self.log_dir:
            self.log_dir.mkdir(parents=True, exist_ok=True)
            
            # Main log file with rotation
            main_log = self.log_dir / f"{self.name}.log"
            file_handler = logging.handlers.RotatingFileHandler(
                main_log,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5
            )
            file_handler.setLevel(self.log_level.value)
            file_handler.setFormatter(self._create_json_formatter())
            self.logger.addHandler(file_handler)
            
            # Error log file
            error_log = self.log_dir / f"{self.name}_errors.log"
            error_handler = logging.handlers.RotatingFileHandler(
                error_log,
                maxBytes=5 * 1024 * 1024,  # 5MB
                backupCount=3
            )
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(self._create_json_formatter())
            self.logger.addHandler(error_handler)
    
    def _create_console_formatter(self) -> logging.Formatter:
        """Create formatter for console output"""
        if self.dev_mode:
            # Detailed format for development
            fmt = (
                "%(asctime)s | %(levelname)-8s | %(name)s | "
                "%(phase_id)s | %(step)s | %(message)s"
            )
        else:
            # Clean format for production
            fmt = "%(asctime)s | %(levelname)-5s | %(message)s"
            
        return logging.Formatter(
            fmt,
            datefmt="%H:%M:%S"
        )
    
    def _create_json_formatter(self) -> 'JsonFormatter':
        """Create JSON formatter for structured logging"""
        return JsonFormatter()
    
    def _enrich_record(self, record: logging.LogRecord):
        """Enrich log record with context information"""
        # Add context information
        context = self._get_effective_context()
        for key, value in context.to_dict().items():
            setattr(record, key, value)
        
        # Add session ID
        record.session_id = self._session_id
        
        # Add timestamp in ISO format
        record.timestamp = datetime.fromtimestamp(record.created).isoformat()
        
        # Add module and function info in dev mode
        if self.dev_mode:
            record.module = record.module if hasattr(record, 'module') else record.filename
            record.function = record.funcName
    
    def _get_effective_context(self) -> LogContext:
        """Get the effective context by merging stack"""
        effective = LogContext()
        
        # Apply contexts from stack (bottom to top)
        for context in self._context_stack + [self._current_context]:
            if context.phase_id is not None:
                effective.phase_id = context.phase_id
            if context.step is not None:
                effective.step = context.step
            if context.worker is not None:
                effective.worker = context.worker
            if context.operation is not None:
                effective.operation = context.operation
            if context.session_id is not None:
                effective.session_id = context.session_id
            if context.metadata is not None:
                if effective.metadata is None:
                    effective.metadata = {}
                effective.metadata.update(context.metadata)
        
        return effective
    
    def set_context(self, **kwargs):
        """Set current logging context"""
        for key, value in kwargs.items():
            if hasattr(self._current_context, key):
                setattr(self._current_context, key, value)
            elif key == 'metadata':
                if self._current_context.metadata is None:
                    self._current_context.metadata = {}
                self._current_context.metadata.update(value)
    
    @contextmanager
    def context(self, **kwargs):
        """Context manager for temporary logging context"""
        temp_context = LogContext(**kwargs)
        self._context_stack.append(temp_context)
        try:
            yield
        finally:
            self._context_stack.pop()
    
    def _log(self, level: LogLevel, message: str, **kwargs):
        """Internal logging method"""
        record = self.logger.makeRecord(
            self.logger.name,
            level.value,
            "",  # pathname
            0,   # lineno
            message,
            (),  # args
            None,  # exc_info
            "",  # func
        )
        
        # Add keyword arguments as attributes
        for key, value in kwargs.items():
            setattr(record, key, value)
        
        # Enrich with context
        self._enrich_record(record)
        
        # Handle the record
        self.logger.handle(record)
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self._log(LogLevel.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        self._log(LogLevel.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self._log(LogLevel.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message"""
        self._log(LogLevel.ERROR, message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message"""
        self._log(LogLevel.CRITICAL, message, **kwargs)
    
    def exception(self, message: str, **kwargs):
        """Log exception with traceback"""
        kwargs['exc_info'] = True
        self.error(message, **kwargs)
    
    def log_phase_start(self, phase_id: str, description: str = ""):
        """Log the start of a phase"""
        with self.context(phase_id=phase_id):
            self.info(f"Phase {phase_id} started", description=description)
    
    def log_phase_end(self, phase_id: str, success: bool = True, duration: Optional[float] = None):
        """Log the end of a phase"""
        with self.context(phase_id=phase_id):
            status = "completed" if success else "failed"
            extra = {}
            if duration is not None:
                extra['duration'] = duration
            self.info(f"Phase {phase_id} {status}", **extra)
    
    def log_step_start(self, step: str, operation: str = ""):
        """Log the start of a step"""
        with self.context(step=step, operation=operation):
            self.debug(f"Step started: {step}", operation=operation)
    
    def log_step_end(self, step: str, success: bool = True, duration: Optional[float] = None):
        """Log the end of a step"""
        with self.context(step=step):
            status = "completed" if success else "failed"
            extra = {}
            if duration is not None:
                extra['duration'] = duration
            self.debug(f"Step {status}: {step}", **extra)
    
    def log_api_call(self, provider: str, model: str, tokens_used: int, cost: float):
        """Log API call information"""
        self.info(
            f"API call to {provider}",
            provider=provider,
            model=model,
            tokens_used=tokens_used,
            cost=cost,
            api_call=True
        )
    
    def log_performance_metric(self, metric_name: str, value: float, unit: str = ""):
        """Log performance metrics"""
        self.debug(
            f"Performance metric: {metric_name}",
            metric_name=metric_name,
            metric_value=value,
            unit=unit,
            performance=True
        )


class JsonFormatter(logging.Formatter):
    """JSON formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_entry = {
            "timestamp": getattr(record, 'timestamp', datetime.fromtimestamp(record.created).isoformat()),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        # Add context fields
        context_fields = ['phase_id', 'step', 'worker', 'operation', 'session_id']
        for field in context_fields:
            if hasattr(record, field) and getattr(record, field) is not None:
                log_entry[field] = getattr(record, field)
        
        # Add metadata if present
        if hasattr(record, 'metadata') and record.metadata:
            log_entry['metadata'] = record.metadata
        
        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
        
        # Add any extra fields
        extra_fields = set(record.__dict__.keys()) - {
            'name', 'msg', 'args', 'levelname', 'levelno', 'pathname',
            'filename', 'module', 'lineno', 'funcName', 'created',
            'msecs', 'relativeCreated', 'thread', 'threadName',
            'processName', 'process', 'getMessage', 'exc_info', 'exc_text',
            'stack_info', 'timestamp', 'phase_id', 'step', 'worker',
            'operation', 'session_id', 'metadata'
        }
        
        for field in extra_fields:
            value = getattr(record, field)
            if value is not None:
                log_entry[field] = value
        
        return json.dumps(log_entry, default=str, separators=(',', ':'))


# Convenience function to get default logger
def get_logger(name: str = "pipeline", **kwargs) -> PipelineLogger:
    """Get a logger instance with default settings"""
    return PipelineLogger.get_logger(name, **kwargs)