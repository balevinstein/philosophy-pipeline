"""
Pipeline Runner for executing phases and managing the pipeline workflow
"""

import json
import logging
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from .exceptions import PhaseError, ConfigurationError, DependencyError
from .phase_registry import PhaseRegistry, PhaseMetadata

# Import monitoring components
try:
    from ..monitoring import (
        PipelineLogger, LogLevel,
        PerformanceProfiler, get_global_profiler,
        CostTracker, get_global_cost_tracker,
        ProgressTracker, get_global_tracker
    )
    MONITORING_AVAILABLE = True
except ImportError:
    MONITORING_AVAILABLE = False


class PipelineRunner:
    """Main runner for executing pipeline phases"""
    
    def __init__(self, config_path: str = None, project_root: str = None):
        """
        Initialize the pipeline runner
        
        Args:
            config_path: Path to configuration file
            project_root: Root directory of the project
        """
        self.project_root = Path(project_root or self._detect_project_root())
        self.config_path = config_path or str(self.project_root / "config" / "conceptual_config.yaml")
        self.registry = PhaseRegistry(str(self.project_root))
        self.config = self._load_config()
        
        # Setup logging
        self.logger = self._setup_logging()
        
    def _detect_project_root(self) -> str:
        """Auto-detect project root"""
        current = Path.cwd()
        while current.parent != current:
            if (current / "src" / "phases").exists() and (current / "config").exists():
                return str(current)
            current = current.parent
        return str(Path.cwd())
    
    def _load_config(self) -> Dict[str, Any]:
        """Load pipeline configuration"""
        if not os.path.exists(self.config_path):
            raise ConfigurationError(f"Configuration file not found: {self.config_path}")
            
        try:
            # For now, return a minimal config since we're focusing on CLI structure
            # In a full implementation, this would parse YAML
            return {
                "paths": {
                    "base_dir": "./outputs",
                    "papers_dir": "./papers"
                }
            }
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {e}")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for pipeline execution"""
        logger = logging.getLogger("pipeline")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def run_phase(self, phase_id: str, dev_mode: bool = False) -> bool:
        """
        Run a specific phase
        
        Args:
            phase_id: Phase identifier (e.g., '2.3')
            dev_mode: Whether to run in development mode
            
        Returns:
            True if phase completed successfully
            
        Raises:
            PhaseError: If phase execution fails
        """
        start_time = time.time()
        
        # Enhanced logging for development mode
        if dev_mode and MONITORING_AVAILABLE:
            # Use enhanced logger if available
            enhanced_logger = PipelineLogger.get_logger(
                "pipeline",
                log_level=LogLevel.DEBUG,
                dev_mode=True
            )
            enhanced_logger.set_context(phase_id=phase_id)
            enhanced_logger.log_phase_start(phase_id)
        else:
            self.logger.info(f"Starting Phase {phase_id}")
        
        # Initialize monitoring
        profiler = None
        progress_tracker = None
        
        if MONITORING_AVAILABLE:
            try:
                profiler = get_global_profiler()
                progress_tracker = get_global_tracker()
                
                if progress_tracker:
                    progress_tracker.update_progress(
                        f"phase_{phase_id}",
                        message=f"Starting Phase {phase_id}"
                    )
            except:
                # Continue without monitoring if it fails
                pass
        
        try:
            # Get phase metadata
            metadata = self.registry.get_phase_metadata(phase_id)
            
            # Validate dependencies
            self._check_phase_dependencies(metadata)
            
            # Start profiling session if available
            if profiler:
                profiler.start_session(f"phase_{phase_id}_execution", f"Phase {phase_id} Execution", {
                    "phase_id": phase_id,
                    "name": metadata.name,
                    "dependencies": metadata.dependencies
                })
            
            # Execute the phase
            success = self._execute_phase(metadata, dev_mode)
            
            # Update progress and log completion
            duration = time.time() - start_time
            
            if success:
                if dev_mode and MONITORING_AVAILABLE:
                    enhanced_logger.log_phase_end(phase_id, True, duration)
                else:
                    self.logger.info(f"Phase {phase_id} completed successfully in {duration:.2f}s")
                
                if progress_tracker:
                    progress_tracker.update_progress(
                        f"phase_{phase_id}",
                        completed_items=100,
                        message=f"Phase {phase_id} completed successfully"
                    )
                
                # Mark phase as completed in output management
                try:
                    from ..outputs import OutputManager
                    output_manager = OutputManager()
                    output_manager.mark_phase_complete(phase_id)
                except Exception as e:
                    self.logger.warning(f"Failed to mark phase {phase_id} as completed: {e}")
                
                return True
            else:
                if progress_tracker:
                    progress_tracker.update_progress(
                        f"phase_{phase_id}",
                        failed_items=100,
                        message=f"Phase {phase_id} failed"
                    )
                
                raise PhaseError(phase_id, "Phase execution returned failure")
                
        except Exception as e:
            duration = time.time() - start_time
            
            if dev_mode and MONITORING_AVAILABLE:
                enhanced_logger.log_phase_end(phase_id, False, duration)
                enhanced_logger.exception(f"Phase {phase_id} failed")
            
            if profiler:
                profiler.record_error()
            
            if progress_tracker:
                progress_tracker.update_progress(
                    f"phase_{phase_id}",
                    failed_items=100,
                    message=f"Phase {phase_id} failed: {str(e)}"
                )
            
            if isinstance(e, PhaseError):
                raise
            else:
                raise PhaseError(phase_id, str(e), e)
                
        finally:
            # End profiling session
            if profiler:
                try:
                    profiler.end_session(f"phase_{phase_id}_execution")
                except:
                    pass
    
    def run_phases(self, phase_range: str, dev_mode: bool = False) -> bool:
        """
        Run a range of phases
        
        Args:
            phase_range: Range specifier like '2.1-2.4' or '2.1,2.3,2.5'
            dev_mode: Whether to run in development mode
            
        Returns:
            True if all phases completed successfully
        """
        phase_ids = self._parse_phase_range(phase_range)
        self.logger.info(f"Running phase sequence: {', '.join(phase_ids)}")
        
        # Validate dependencies for entire sequence
        self.registry.validate_dependencies(phase_ids)
        
        for phase_id in phase_ids:
            if not self.run_phase(phase_id, dev_mode):
                return False
                
        self.logger.info("Phase sequence completed successfully")
        return True
    
    def run_full_pipeline(self, dev_mode: bool = False) -> bool:
        """
        Run the complete pipeline from start to finish
        
        Args:
            dev_mode: Whether to run in development mode
            
        Returns:
            True if pipeline completed successfully
        """
        self.logger.info("Starting full pipeline execution")
        
        # Initialize output management for new pipeline run
        try:
            from ..outputs import OutputManager
            
            output_manager = OutputManager()
            run_dir = output_manager.create_run_directory()
            self.logger.info(f"Created new run directory: {run_dir}")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize output management: {e}")
            # Continue without output management if it fails
            output_manager = None
        
        # Get all phases in order
        all_phases = self.registry.get_ordered_phases()
        
        if not all_phases:
            self.logger.warning("No phases discovered")
            return False
            
        # Run all phases
        for phase_id in all_phases:
            if not self.run_phase(phase_id, dev_mode):
                return False
                
        self.logger.info("Full pipeline completed successfully")
        
        # Automatic archiving after successful pipeline completion
        try:
            from ..outputs import OutputManager
            
            output_manager = OutputManager()
            self.logger.info("Performing automatic archiving of completed run...")
            
            if output_manager.archive_current_run():
                self.logger.info("Successfully archived completed pipeline run")
            else:
                self.logger.warning("Failed to archive pipeline run - outputs remain in current/")
                
        except Exception as e:
            self.logger.error(f"Error during automatic archiving: {e}")
            # Don't fail the pipeline just because archiving failed
            
        return True
    
    def _parse_phase_range(self, phase_range: str) -> List[str]:
        """Parse phase range specification into list of phase IDs"""
        if '-' in phase_range:
            # Handle range like '2.1-2.4'
            start, end = phase_range.split('-', 1)
            return self.registry.get_ordered_phases(start.strip(), end.strip())
        elif ',' in phase_range:
            # Handle comma-separated list like '2.1,2.3,2.5'
            return [p.strip() for p in phase_range.split(',')]
        else:
            # Single phase
            return [phase_range.strip()]
    
    def _check_phase_dependencies(self, metadata: PhaseMetadata) -> bool:
        """
        Check if phase dependencies are satisfied
        
        Args:
            metadata: Phase metadata
            
        Returns:
            True if dependencies are satisfied
            
        Raises:
            DependencyError: If dependencies are not met
        """
        missing_outputs = []
        
        for dep_phase_id in metadata.dependencies:
            try:
                dep_metadata = self.registry.get_phase_metadata(dep_phase_id)
                
                # Check if expected outputs exist
                for output in dep_metadata.outputs:
                    output_path = self.project_root / "outputs" / output
                    if not output_path.exists():
                        missing_outputs.append(f"{dep_phase_id}:{output}")
                        
            except Exception:
                missing_outputs.append(dep_phase_id)
        
        if missing_outputs:
            raise DependencyError(
                metadata.phase_id, 
                missing_outputs
            )
            
        return True
    
    def _execute_phase(self, metadata: PhaseMetadata, dev_mode: bool = False) -> bool:
        """
        Execute a specific phase
        
        Args:
            metadata: Phase metadata
            dev_mode: Development mode flag
            
        Returns:
            True if execution succeeded
        """
        script_path = metadata.script_path
        execution_start = time.time()
        
        # Initialize monitoring
        profiler = None
        progress_tracker = None
        
        if MONITORING_AVAILABLE:
            try:
                profiler = get_global_profiler()
                progress_tracker = get_global_tracker()
            except:
                pass
        
        # Change to project root directory for execution
        original_cwd = os.getcwd()
        
        try:
            os.chdir(str(self.project_root))
            
            # Prepare environment
            env = os.environ.copy()
            env['PYTHONPATH'] = str(self.project_root)
            
            if dev_mode:
                env['PIPELINE_DEV_MODE'] = '1'
            
            # Enable monitoring in environment if available
            if MONITORING_AVAILABLE:
                env['PIPELINE_MONITORING_ENABLED'] = '1'
                env['PIPELINE_PROFILING_ENABLED'] = '1' if profiler else '0'
                env['PIPELINE_COST_TRACKING_ENABLED'] = '1'
            
            # Start operation profiling
            operation_name = f"execute_script_{metadata.phase_id}"
            if profiler:
                profiler_context = profiler.profile_operation(operation_name, 
                                                            phase_id=metadata.phase_id,
                                                            script_path=script_path)
                profiler_context.__enter__()
            else:
                profiler_context = None
            
            # Update progress
            if progress_tracker:
                progress_tracker.update_progress(
                    f"phase_{metadata.phase_id}",
                    increment=20,
                    message=f"Executing script: {script_path}"
                )
            
            # Execute the phase script
            self.logger.info(f"Executing: python {script_path}")
            
            result = subprocess.run(
                [sys.executable, script_path],
                env=env,
                capture_output=True,
                text=True,
                timeout=3600  # 1 hour timeout
            )
            
            execution_duration = time.time() - execution_start
            
            # Process output with enhanced logging
            if result.stdout:
                for line in result.stdout.split('\n'):
                    if line.strip():
                        # Try to parse monitoring information from output
                        if dev_mode and MONITORING_AVAILABLE and line.startswith('[MONITORING]'):
                            try:
                                # Parse monitoring data from script output
                                monitoring_data = json.loads(line[12:])  # Remove [MONITORING] prefix
                                self._process_monitoring_data(monitoring_data, metadata.phase_id)
                            except:
                                # If parsing fails, just log normally
                                self.logger.info(f"[{metadata.phase_id}] {line}")
                        else:
                            self.logger.info(f"[{metadata.phase_id}] {line}")
                        
            if result.stderr:
                for line in result.stderr.split('\n'):
                    if line.strip():
                        self.logger.error(f"[{metadata.phase_id}] {line}")
            
            # Update progress based on result
            if progress_tracker:
                if result.returncode == 0:
                    progress_tracker.update_progress(
                        f"phase_{metadata.phase_id}",
                        increment=60,
                        message=f"Script completed successfully"
                    )
                else:
                    progress_tracker.update_progress(
                        f"phase_{metadata.phase_id}",
                        failed_items=20,
                        message=f"Script failed with exit code {result.returncode}"
                    )
            
            # Record performance metrics
            if profiler:
                profiler.record_performance_metric("script_execution_time", execution_duration, "seconds")
            
            if result.returncode != 0:
                self.logger.error(f"Phase {metadata.phase_id} failed with exit code {result.returncode}")
                if profiler:
                    profiler.record_error("script_execution_failure")
                return False
                
            return True
            
        except subprocess.TimeoutExpired:
            self.logger.error(f"Phase {metadata.phase_id} timed out")
            if profiler:
                profiler.record_error("script_timeout")
            if progress_tracker:
                progress_tracker.update_progress(
                    f"phase_{metadata.phase_id}",
                    failed_items=50,
                    message="Script execution timed out"
                )
            return False
        except Exception as e:
            self.logger.error(f"Error executing phase {metadata.phase_id}: {e}")
            if profiler:
                profiler.record_error("script_execution_error")
            return False
        finally:
            # End profiling
            if profiler_context:
                try:
                    profiler_context.__exit__(None, None, None)
                except:
                    pass
            
            os.chdir(original_cwd)
    
    def _process_monitoring_data(self, data: dict, phase_id: str):
        """Process monitoring data from phase script output"""
        if not MONITORING_AVAILABLE:
            return
        
        try:
            if data.get('type') == 'api_call':
                cost_tracker = get_global_cost_tracker()
                if cost_tracker:
                    cost_tracker.record_api_call(
                        provider=data.get('provider', 'unknown'),
                        model=data.get('model', 'unknown'),
                        input_tokens=data.get('input_tokens', 0),
                        output_tokens=data.get('output_tokens', 0),
                        latency=data.get('latency', 0.0),
                        success=data.get('success', True),
                        context={'phase_id': phase_id}
                    )
            
            elif data.get('type') == 'progress_update':
                progress_tracker = get_global_tracker()
                if progress_tracker:
                    progress_tracker.update_progress(
                        f"phase_{phase_id}",
                        increment=data.get('increment', 0),
                        message=data.get('message', '')
                    )
            
            elif data.get('type') == 'performance_metric':
                profiler = get_global_profiler()
                if profiler:
                    profiler.record_performance_metric(
                        data.get('metric_name', 'unknown'),
                        data.get('value', 0.0),
                        data.get('unit', '')
                    )
                    
        except Exception as e:
            # Don't fail the pipeline if monitoring data processing fails
            self.logger.warning(f"Failed to process monitoring data: {e}")
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """
        Get the current status of the pipeline
        
        Returns:
            Dictionary with pipeline status information
        """
        phases = self.registry.list_phases()
        status = {
            "total_phases": len(phases),
            "completed_phases": 0,
            "failed_phases": 0,
            "phases": {}
        }
        
        for phase_id, metadata in phases.items():
            phase_status = self._check_phase_status(metadata)
            status["phases"][phase_id] = phase_status
            
            if phase_status["status"] == "completed":
                status["completed_phases"] += 1
            elif phase_status["status"] == "failed":
                status["failed_phases"] += 1
                
        return status
    
    def _check_phase_status(self, metadata: PhaseMetadata) -> Dict[str, Any]:
        """Check the status of a specific phase"""
        outputs_dir = self.project_root / "outputs"
        
        # Check if expected outputs exist
        outputs_exist = []
        for output in metadata.outputs:
            output_path = outputs_dir / output
            outputs_exist.append(output_path.exists())
        
        if not metadata.outputs:
            # No specific outputs to check
            status = "unknown"
        elif all(outputs_exist):
            status = "completed"
        elif any(outputs_exist):
            status = "partial"
        else:
            status = "pending"
            
        return {
            "status": status,
            "name": metadata.name,
            "description": metadata.description,
            "dependencies": metadata.dependencies,
            "outputs": metadata.outputs,
            "outputs_exist": outputs_exist
        }
    
    def validate_environment(self) -> Dict[str, bool]:
        """
        Validate the pipeline environment
        
        Returns:
            Dictionary with validation results
        """
        checks = {
            "project_structure": False,
            "config_file": False,
            "output_directory": False,
            "python_path": False,
            "dependencies": False
        }
        
        # Check project structure
        checks["project_structure"] = all([
            (self.project_root / "src" / "phases").exists(),
            (self.project_root / "scripts" / "phases").exists()
        ])
        
        # Check config file
        checks["config_file"] = Path(self.config_path).exists()
        
        # Check output directory
        outputs_dir = self.project_root / "outputs"
        checks["output_directory"] = outputs_dir.exists()
        if not outputs_dir.exists():
            outputs_dir.mkdir(parents=True, exist_ok=True)
            checks["output_directory"] = True
        
        # Check Python path
        checks["python_path"] = str(self.project_root) in sys.path
        
        # TODO: Add more dependency checks (anthropic API, etc.)
        checks["dependencies"] = True
        
        return checks