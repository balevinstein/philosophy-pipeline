"""
Progress Tracking System for Philosophy Pipeline

Provides multi-level progress tracking with time estimates,
visual indicators, and resumption detection.
"""

import json
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from threading import Lock
import sys


class ProgressLevel(Enum):
    """Progress tracking levels"""
    PIPELINE = "pipeline"
    PHASE = "phase"
    STEP = "step"
    SUBTASK = "subtask"


@dataclass
class ProgressState:
    """State information for progress tracking"""
    id: str
    level: ProgressLevel
    name: str
    description: str = ""
    parent_id: Optional[str] = None
    
    # Progress metrics
    total_items: int = 100
    completed_items: int = 0
    failed_items: int = 0
    
    # Timing
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    estimated_duration: Optional[float] = None
    
    # Status
    status: str = "pending"  # pending, running, completed, failed, paused
    
    # Metadata
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['level'] = self.level.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProgressState':
        """Create from dictionary"""
        data['level'] = ProgressLevel(data['level'])
        return cls(**data)
    
    @property
    def progress_percentage(self) -> float:
        """Calculate progress percentage"""
        if self.total_items == 0:
            return 0.0
        return (self.completed_items / self.total_items) * 100
    
    @property
    def is_running(self) -> bool:
        """Check if currently running"""
        return self.status == "running"
    
    @property
    def is_completed(self) -> bool:
        """Check if completed"""
        return self.status in ["completed", "failed"]
    
    @property
    def duration(self) -> Optional[float]:
        """Calculate duration if available"""
        if self.start_time is None:
            return None
        end = self.end_time or time.time()
        return end - self.start_time
    
    @property
    def estimated_completion_time(self) -> Optional[datetime]:
        """Estimate completion time"""
        if not self.is_running or self.progress_percentage <= 0:
            return None
            
        duration = self.duration
        if duration is None or duration <= 0:
            return None
        
        progress_rate = self.progress_percentage / duration
        if progress_rate <= 0:
            return None
        
        remaining_percentage = 100 - self.progress_percentage
        estimated_remaining = remaining_percentage / progress_rate
        
        return datetime.now() + timedelta(seconds=estimated_remaining)


class ProgressTracker:
    """Multi-level progress tracker with time estimation and visual feedback"""
    
    def __init__(
        self,
        save_dir: Optional[Union[str, Path]] = None,
        auto_save: bool = True,
        show_progress_bars: bool = True,
        enable_console_output: bool = True
    ):
        """
        Initialize progress tracker
        
        Args:
            save_dir: Directory to save progress state (None = no persistence)
            auto_save: Automatically save state changes
            show_progress_bars: Show visual progress bars
            enable_console_output: Enable console progress updates
        """
        self.save_dir = Path(save_dir) if save_dir else None
        self.auto_save = auto_save
        self.show_progress_bars = show_progress_bars
        self.enable_console_output = enable_console_output
        
        # State management
        self._states: Dict[str, ProgressState] = {}
        self._lock = Lock()
        
        # Progress display
        self._last_console_update = 0
        self._console_update_interval = 1.0  # seconds
        
        # Load existing state if available
        self._load_state()
        
        # Create save directory
        if self.save_dir:
            self.save_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_state(self):
        """Load progress state from disk"""
        if not self.save_dir or not (self.save_dir / "progress_state.json").exists():
            return
        
        try:
            with open(self.save_dir / "progress_state.json", 'r') as f:
                data = json.load(f)
            
            for state_id, state_data in data.items():
                self._states[state_id] = ProgressState.from_dict(state_data)
                
        except Exception as e:
            print(f"Warning: Failed to load progress state: {e}")
    
    def _save_state(self):
        """Save progress state to disk"""
        if not self.save_dir:
            return
        
        try:
            data = {
                state_id: state.to_dict()
                for state_id, state in self._states.items()
            }
            
            with open(self.save_dir / "progress_state.json", 'w') as f:
                json.dump(data, f, indent=2, default=str)
                
        except Exception as e:
            print(f"Warning: Failed to save progress state: {e}")
    
    def create_progress(
        self,
        progress_id: str,
        name: str,
        level: ProgressLevel,
        total_items: int = 100,
        description: str = "",
        parent_id: Optional[str] = None,
        **metadata
    ) -> ProgressState:
        """
        Create a new progress tracker
        
        Args:
            progress_id: Unique identifier
            name: Human-readable name
            level: Progress level
            total_items: Total number of items to track
            description: Description of the progress
            parent_id: Parent progress ID for hierarchical tracking
            **metadata: Additional metadata
            
        Returns:
            Created progress state
        """
        with self._lock:
            state = ProgressState(
                id=progress_id,
                name=name,
                level=level,
                description=description,
                parent_id=parent_id,
                total_items=total_items,
                metadata=metadata or None
            )
            
            self._states[progress_id] = state
            
            if self.auto_save:
                self._save_state()
            
            return state
    
    def start_progress(self, progress_id: str) -> bool:
        """
        Start tracking progress
        
        Args:
            progress_id: Progress identifier
            
        Returns:
            True if started successfully
        """
        with self._lock:
            if progress_id not in self._states:
                return False
            
            state = self._states[progress_id]
            state.status = "running"
            state.start_time = time.time()
            
            if self.auto_save:
                self._save_state()
            
            self._update_console_display(progress_id)
            return True
    
    def update_progress(
        self,
        progress_id: str,
        completed_items: Optional[int] = None,
        increment: Optional[int] = None,
        failed_items: Optional[int] = None,
        message: Optional[str] = None,
        **metadata
    ) -> bool:
        """
        Update progress state
        
        Args:
            progress_id: Progress identifier
            completed_items: Set completed items count
            increment: Increment completed items by this amount
            failed_items: Set failed items count
            message: Status message
            **metadata: Additional metadata
            
        Returns:
            True if updated successfully
        """
        with self._lock:
            if progress_id not in self._states:
                return False
            
            state = self._states[progress_id]
            
            # Update counts
            if completed_items is not None:
                state.completed_items = completed_items
            elif increment is not None:
                state.completed_items += increment
            
            if failed_items is not None:
                state.failed_items = failed_items
            
            # Update metadata
            if metadata:
                if state.metadata is None:
                    state.metadata = {}
                state.metadata.update(metadata)
            
            # Add message to metadata
            if message:
                if state.metadata is None:
                    state.metadata = {}
                state.metadata['last_message'] = message
                state.metadata['message_time'] = time.time()
            
            if self.auto_save:
                self._save_state()
            
            self._update_console_display(progress_id)
            return True
    
    def complete_progress(
        self,
        progress_id: str,
        success: bool = True,
        message: Optional[str] = None
    ) -> bool:
        """
        Mark progress as completed
        
        Args:
            progress_id: Progress identifier
            success: Whether completed successfully
            message: Completion message
            
        Returns:
            True if completed successfully
        """
        with self._lock:
            if progress_id not in self._states:
                return False
            
            state = self._states[progress_id]
            state.status = "completed" if success else "failed"
            state.end_time = time.time()
            
            if not success:
                state.failed_items = state.total_items - state.completed_items
            else:
                state.completed_items = state.total_items
            
            if message:
                if state.metadata is None:
                    state.metadata = {}
                state.metadata['completion_message'] = message
                state.metadata['completion_time'] = time.time()
            
            if self.auto_save:
                self._save_state()
            
            self._update_console_display(progress_id, force=True)
            return True
    
    def pause_progress(self, progress_id: str) -> bool:
        """Pause progress tracking"""
        with self._lock:
            if progress_id not in self._states:
                return False
            
            state = self._states[progress_id]
            state.status = "paused"
            
            if self.auto_save:
                self._save_state()
            
            return True
    
    def resume_progress(self, progress_id: str) -> bool:
        """Resume paused progress tracking"""
        with self._lock:
            if progress_id not in self._states:
                return False
            
            state = self._states[progress_id]
            if state.status == "paused":
                state.status = "running"
            
            if self.auto_save:
                self._save_state()
            
            return True
    
    def get_progress(self, progress_id: str) -> Optional[ProgressState]:
        """Get progress state"""
        return self._states.get(progress_id)
    
    def get_all_progress(self) -> Dict[str, ProgressState]:
        """Get all progress states"""
        return self._states.copy()
    
    def get_hierarchical_progress(self) -> Dict[str, Any]:
        """Get progress organized hierarchically"""
        # Build hierarchy
        roots = []
        children_map = {}
        
        for state in self._states.values():
            if state.parent_id is None:
                roots.append(state)
            else:
                if state.parent_id not in children_map:
                    children_map[state.parent_id] = []
                children_map[state.parent_id].append(state)
        
        def build_tree(state: ProgressState) -> Dict[str, Any]:
            node = {
                'state': state,
                'children': []
            }
            
            if state.id in children_map:
                for child in children_map[state.id]:
                    node['children'].append(build_tree(child))
            
            return node
        
        return {
            'roots': [build_tree(root) for root in roots],
            'total_states': len(self._states)
        }
    
    def _update_console_display(self, progress_id: str, force: bool = False):
        """Update console progress display"""
        if not self.enable_console_output:
            return
        
        current_time = time.time()
        if not force and current_time - self._last_console_update < self._console_update_interval:
            return
        
        state = self._states.get(progress_id)
        if not state:
            return
        
        self._last_console_update = current_time
        
        if self.show_progress_bars:
            self._display_progress_bar(state)
        else:
            self._display_progress_text(state)
    
    def _display_progress_bar(self, state: ProgressState):
        """Display progress bar"""
        percentage = state.progress_percentage
        completed = int(percentage / 2)  # 50 chars max
        remaining = 50 - completed
        
        bar = '█' * completed + '░' * remaining
        
        # Time estimates
        duration_str = ""
        if state.duration:
            duration_str = f" | {self._format_duration(state.duration)}"
        
        eta_str = ""
        if state.estimated_completion_time and state.is_running:
            eta = state.estimated_completion_time.strftime("%H:%M:%S")
            eta_str = f" | ETA: {eta}"
        
        # Status symbol
        if state.is_completed:
            symbol = "✅" if state.status == "completed" else "❌"
        elif state.is_running:
            symbol = "🔄"
        else:
            symbol = "⭕"
        
        message = f"\r{symbol} {state.name}: [{bar}] {percentage:5.1f}%{duration_str}{eta_str}"
        
        # Add last message if available
        if state.metadata and 'last_message' in state.metadata:
            message += f" | {state.metadata['last_message']}"
        
        # Print with carriage return for updating same line
        if not state.is_completed:
            print(message, end='', flush=True)
        else:
            print(message)  # New line for completed tasks
    
    def _display_progress_text(self, state: ProgressState):
        """Display simple text progress"""
        percentage = state.progress_percentage
        
        status_map = {
            "pending": "⭕",
            "running": "🔄", 
            "completed": "✅",
            "failed": "❌",
            "paused": "⏸️"
        }
        
        symbol = status_map.get(state.status, "❓")
        
        message = f"{symbol} {state.name}: {percentage:5.1f}%"
        
        if state.metadata and 'last_message' in state.metadata:
            message += f" - {state.metadata['last_message']}"
        
        print(message)
    
    def _format_duration(self, duration: float) -> str:
        """Format duration in human-readable format"""
        if duration < 60:
            return f"{duration:.1f}s"
        elif duration < 3600:
            minutes = duration / 60
            return f"{minutes:.1f}m"
        else:
            hours = duration / 3600
            return f"{hours:.1f}h"
    
    def print_summary(self):
        """Print a summary of all progress"""
        if not self._states:
            print("No active progress tracking")
            return
        
        print("\nProgress Summary:")
        print("=" * 60)
        
        hierarchy = self.get_hierarchical_progress()
        
        def print_state(state: ProgressState, indent: int = 0):
            prefix = "  " * indent
            percentage = state.progress_percentage
            
            status_map = {
                "pending": "⭕",
                "running": "🔄",
                "completed": "✅", 
                "failed": "❌",
                "paused": "⏸️"
            }
            
            symbol = status_map.get(state.status, "❓")
            
            duration_str = ""
            if state.duration:
                duration_str = f" ({self._format_duration(state.duration)})"
            
            print(f"{prefix}{symbol} {state.name}: {percentage:5.1f}%{duration_str}")
            
            if state.description:
                print(f"{prefix}   {state.description}")
        
        def print_tree(node: Dict[str, Any], indent: int = 0):
            print_state(node['state'], indent)
            for child in node['children']:
                print_tree(child, indent + 1)
        
        for root in hierarchy['roots']:
            print_tree(root)
        
        print(f"\nTotal tracked items: {hierarchy['total_states']}")
    
    def clear_completed(self):
        """Clear completed progress states"""
        with self._lock:
            to_remove = [
                state_id for state_id, state in self._states.items()
                if state.is_completed
            ]
            
            for state_id in to_remove:
                del self._states[state_id]
            
            if self.auto_save:
                self._save_state()
            
            return len(to_remove)
    
    def reset(self):
        """Reset all progress tracking"""
        with self._lock:
            self._states.clear()
            
            if self.auto_save:
                self._save_state()


# Global progress tracker instance
_global_tracker: Optional[ProgressTracker] = None


def get_global_tracker(**kwargs) -> ProgressTracker:
    """Get or create the global progress tracker"""
    global _global_tracker
    if _global_tracker is None:
        _global_tracker = ProgressTracker(**kwargs)
    return _global_tracker


def set_global_tracker(tracker: ProgressTracker):
    """Set the global progress tracker"""
    global _global_tracker
    _global_tracker = tracker