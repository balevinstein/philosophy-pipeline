#!/usr/bin/env python3
"""
Philosophy Pipeline CLI

A unified command-line interface for the philosophy pipeline project that replaces
the individual runner scripts with a single, comprehensive tool.

Usage:
    python pipeline_cli.py run --full                    # Run complete pipeline
    python pipeline_cli.py run --phase 2.3              # Run specific phase
    python pipeline_cli.py run --phases 2.1-2.4         # Run phase range
    python pipeline_cli.py run --phases 2.1,2.3,2.5     # Run specific phases
    python pipeline_cli.py status                        # Show pipeline status
    python pipeline_cli.py list                          # List available phases
    python pipeline_cli.py validate                      # Validate environment
"""

import argparse
import sys
import os
from pathlib import Path
from typing import List

# Add project root to Python path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

from src.pipeline import PipelineRunner, PhaseRegistry, PipelineError, PhaseError, DependencyError


def create_parser() -> argparse.ArgumentParser:
    """Create the command-line parser"""
    parser = argparse.ArgumentParser(
        description="Philosophy Pipeline CLI - Unified interface for pipeline execution",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s setup --interactive           Interactive setup wizard for first-time users
  %(prog)s run --full                    Run the complete pipeline
  %(prog)s run --phase 2.3              Run only Phase II.3
  %(prog)s run --phases 2.1-2.4         Run phases 2.1 through 2.4
  %(prog)s run --phases 2.1,2.3,2.5     Run specific phases
  %(prog)s status                        Show current pipeline status
  %(prog)s list                          List all available phases
  %(prog)s validate                      Validate pipeline environment

Phase Identification:
  Phases are identified by their number (e.g., 1.1, 2.3, 3.2)
  - Phase I: Conceptual development (1.1, 1.2)
  - Phase II: Framework and analysis (2.1 through 2.8)  
  - Phase III: Writing and integration (3.1, 3.2)
        """
    )
    
    # Global options
    parser.add_argument(
        '--config', '-c',
        help='Path to configuration file (default: config/conceptual_config.yaml)',
        default=None
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug output with detailed logging'
    )
    parser.add_argument(
        '--log-dir',
        help='Directory for log files (enables file logging)'
    )
    parser.add_argument(
        '--log-format',
        choices=['console', 'json'],
        default='console',
        help='Log output format'
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Run command
    run_parser = subparsers.add_parser(
        'run',
        help='Execute pipeline phases',
        description='Execute one or more phases of the philosophy pipeline'
    )
    
    run_group = run_parser.add_mutually_exclusive_group(required=True)
    run_group.add_argument(
        '--full',
        action='store_true', 
        help='Run the complete pipeline from start to finish'
    )
    run_group.add_argument(
        '--phase',
        help='Run a specific phase (e.g., 2.3)'
    )
    run_group.add_argument(
        '--phases',
        help='Run multiple phases. Supports ranges (2.1-2.4) or comma-separated (2.1,2.3,2.5)'
    )
    
    run_parser.add_argument(
        '--dev',
        action='store_true',
        help='Run in development mode with enhanced logging and monitoring'
    )
    run_parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Enable interactive step-by-step execution'
    )
    run_parser.add_argument(
        '--profile',
        action='store_true',
        help='Enable performance profiling'
    )
    run_parser.add_argument(
        '--track-costs',
        action='store_true',
        help='Enable API cost tracking'
    )
    run_parser.add_argument(
        '--budget',
        type=float,
        help='Set budget limit for cost tracking'
    )
    
    # Status command
    status_parser = subparsers.add_parser(
        'status',
        help='Show pipeline status',
        description='Display the current status of all phases'
    )
    status_parser.add_argument(
        '--json',
        action='store_true',
        help='Output status in JSON format'
    )
    
    # List command
    list_parser = subparsers.add_parser(
        'list',
        help='List available phases',
        description='Show all available phases with their descriptions'
    )
    list_parser.add_argument(
        '--detailed',
        action='store_true',
        help='Show detailed phase information including dependencies'
    )
    
    # Validate command
    validate_parser = subparsers.add_parser(
        'validate',
        help='Validate environment',
        description='Check that the pipeline environment is properly configured'
    )
    validate_parser.add_argument(
        '--phase',
        help='Validate specific phase dependencies'
    )
    
    # Setup command
    setup_parser = subparsers.add_parser(
        'setup',
        help='Interactive setup wizard',
        description='Guide you through initial setup and configuration'
    )
    setup_parser.add_argument(
        '--interactive',
        action='store_true',
        default=True,
        help='Run interactive setup wizard (default)'
    )
    setup_parser.add_argument(
        '--quick',
        action='store_true',
        help='Quick setup with minimal prompts'
    )
    setup_parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate existing setup'
    )
    
    # Debug command
    debug_parser = subparsers.add_parser(
        'debug',
        help='Interactive debugging',
        description='Interactive debugging and step-by-step execution'
    )
    debug_group = debug_parser.add_mutually_exclusive_group(required=True)
    debug_group.add_argument(
        '--phase',
        help='Debug a specific phase (e.g., 2.3)'
    )
    debug_group.add_argument(
        '--step',
        help='Debug a specific step within a phase'
    )
    debug_parser.add_argument(
        '--break-at',
        help='Set breakpoint at specific operation'
    )
    
    # Profile command
    profile_parser = subparsers.add_parser(
        'profile',
        help='Performance profiling',
        description='Run phases with performance profiling and generate reports'
    )
    profile_group = profile_parser.add_mutually_exclusive_group(required=True)
    profile_group.add_argument(
        '--phase',
        help='Profile a specific phase'
    )
    profile_group.add_argument(
        '--phases',
        help='Profile multiple phases'
    )
    profile_group.add_argument(
        '--full',
        action='store_true',
        help='Profile the complete pipeline'
    )
    profile_parser.add_argument(
        '--report',
        help='Generate profiling report file'
    )
    
    # Cost command
    cost_parser = subparsers.add_parser(
        'cost',
        help='Cost tracking and reporting',
        description='Monitor and report API usage costs'
    )
    cost_subparsers = cost_parser.add_subparsers(dest='cost_action', help='Cost actions')
    
    # Cost status
    cost_status_parser = cost_subparsers.add_parser(
        'status',
        help='Show current cost status'
    )
    
    # Cost report
    cost_report_parser = cost_subparsers.add_parser(
        'report',
        help='Generate cost report'
    )
    cost_report_parser.add_argument(
        '--period',
        choices=['hour', 'day', 'week', 'month', 'total'],
        default='day',
        help='Report period'
    )
    cost_report_parser.add_argument(
        '--save',
        help='Save report to file'
    )
    
    # Cost budget
    cost_budget_parser = cost_subparsers.add_parser(
        'budget',
        help='Manage budget settings'
    )
    cost_budget_parser.add_argument(
        '--set',
        type=float,
        help='Set budget limit'
    )
    cost_budget_parser.add_argument(
        '--alert',
        nargs=3,
        metavar=('THRESHOLD', 'PERIOD', 'TYPE'),
        help='Add budget alert (threshold, period, type)'
    )
    
    # Monitor command
    monitor_parser = subparsers.add_parser(
        'monitor',
        help='Real-time monitoring',
        description='Monitor pipeline execution in real-time'
    )
    monitor_parser.add_argument(
        '--follow', '-f',
        action='store_true',
        help='Follow log output in real-time'
    )
    monitor_parser.add_argument(
        '--metrics',
        action='store_true',
        help='Show performance metrics'
    )
    
    # Outputs command
    outputs_parser = subparsers.add_parser(
        'outputs',
        help='Manage pipeline outputs',
        description='Manage, archive, and export pipeline outputs'
    )
    outputs_group = outputs_parser.add_mutually_exclusive_group(required=True)
    outputs_group.add_argument(
        '--list',
        action='store_true',
        help='List current and archived outputs'
    )
    outputs_group.add_argument(
        '--archive',
        action='store_true',
        help='Archive current run outputs'
    )
    outputs_group.add_argument(
        '--clean',
        type=int,
        metavar='COUNT',
        help='Clean old archives, keeping COUNT most recent'
    )
    outputs_group.add_argument(
        '--export-paper',
        choices=['md', 'json', 'html', 'txt'],
        help='Export final paper in specified format'
    )
    outputs_group.add_argument(
        '--statistics',
        action='store_true',
        help='Show comprehensive output statistics'
    )
    outputs_parser.add_argument(
        '--output-file', '-o',
        help='Output file path (for export operations)'
    )
    outputs_parser.add_argument(
        '--json',
        action='store_true',
        help='Output results in JSON format'
    )
    
    return parser


def handle_run_command(args, runner: PipelineRunner) -> int:
    """Handle the run command"""
    try:
        # Initialize monitoring components if requested
        profiler = None
        cost_tracker = None
        progress_tracker = None
        
        if getattr(args, 'profile', False):
            from src.monitoring import PerformanceProfiler
            profiler = PerformanceProfiler(
                save_dir="outputs/profiling",
                auto_save=True
            )
        
        if getattr(args, 'track_costs', False):
            from src.monitoring import CostTracker
            cost_tracker = CostTracker(
                save_dir="outputs/cost_tracking",
                auto_save=True,
                default_budget_limit=getattr(args, 'budget', 100.0)
            )
        
        if args.dev or getattr(args, 'interactive', False):
            from src.monitoring import ProgressTracker
            progress_tracker = ProgressTracker(
                save_dir="outputs/progress",
                auto_save=True,
                show_progress_bars=True
            )
        
        # Interactive mode handling
        if getattr(args, 'interactive', False):
            print("🔍 Interactive mode enabled - you'll be prompted before each phase")
        
        # Execute with monitoring
        session_id = None
        if profiler:
            if args.full:
                session_id = profiler.start_session("full_pipeline", "Full Pipeline Execution")
            elif args.phase:
                session_id = profiler.start_session(f"phase_{args.phase}", f"Phase {args.phase} Execution")
            elif args.phases:
                session_id = profiler.start_session("multi_phase", f"Phases {args.phases} Execution")
        
        if cost_tracker:
            if args.full:
                cost_tracker.start_session("full_pipeline")
            elif args.phase:
                cost_tracker.start_session(f"phase_{args.phase}")
            elif args.phases:
                cost_tracker.start_session("multi_phase")
        
        try:
            # Execute pipeline
            if args.full:
                print("🚀 Starting full pipeline execution...")
                if progress_tracker:
                    progress_tracker.create_progress("full_pipeline", "Full Pipeline", "pipeline", 100)
                    progress_tracker.start_progress("full_pipeline")
                
                success = runner.run_full_pipeline(dev_mode=args.dev)
                
                if progress_tracker:
                    progress_tracker.complete_progress("full_pipeline", success)
                
            elif args.phase:
                print(f"🚀 Running Phase {args.phase}...")
                if progress_tracker:
                    progress_tracker.create_progress(f"phase_{args.phase}", f"Phase {args.phase}", "phase", 100)
                    progress_tracker.start_progress(f"phase_{args.phase}")
                
                # Interactive confirmation
                if getattr(args, 'interactive', False):
                    metadata = runner.registry.get_phase_metadata(args.phase)
                    print(f"Phase: {metadata.name}")
                    print(f"Description: {metadata.description}")
                    response = input("Continue? (y/n): ").lower()
                    if response != 'y':
                        print("Execution cancelled")
                        return 0
                
                success = runner.run_phase(args.phase, dev_mode=args.dev)
                
                if progress_tracker:
                    progress_tracker.complete_progress(f"phase_{args.phase}", success)
                
            elif args.phases:
                print(f"🚀 Running phases: {args.phases}")
                if progress_tracker:
                    progress_tracker.create_progress("multi_phase", f"Phases {args.phases}", "pipeline", 100)
                    progress_tracker.start_progress("multi_phase")
                
                success = runner.run_phases(args.phases, dev_mode=args.dev)
                
                if progress_tracker:
                    progress_tracker.complete_progress("multi_phase", success)
                    
            else:
                print("❌ No execution mode specified")
                return 1
            
            # Show monitoring results
            if success:
                print("✅ Execution completed successfully!")
                
                # Show profiling summary
                if profiler and session_id:
                    profiler.end_session(session_id)
                    report = profiler.generate_report(session_id)
                    print("\n📊 Performance Summary:")
                    print(f"  Duration: {report['sessions'][0]['duration']:.2f}s")
                    if report['sessions'][0]['metrics']['peak_memory_mb'] > 0:
                        print(f"  Peak Memory: {report['sessions'][0]['metrics']['peak_memory_mb']:.1f} MB")
                    profiler.cleanup()
                
                # Show cost summary
                if cost_tracker:
                    cost_session = cost_tracker.end_session(session_id or "default")
                    if cost_session:
                        print("\n💰 Cost Summary:")
                        print(f"  Total Cost: ${cost_session.total_cost:.4f}")
                        if cost_session.requests > 0:
                            print(f"  API Calls: {cost_session.requests}")
                        if cost_session.total_tokens > 0:
                            print(f"  Tokens Used: {cost_session.total_tokens:,}")
                
                # Show progress summary
                if progress_tracker:
                    progress_tracker.print_summary()
                
                return 0
            else:
                print("❌ Execution failed!")
                return 1
                
        finally:
            # Cleanup monitoring
            if profiler and session_id:
                profiler.end_session(session_id)
                profiler.cleanup()
            
            if cost_tracker:
                cost_tracker.end_session(session_id or "default")
            
    except (PhaseError, DependencyError, PipelineError) as e:
        print(f"❌ Pipeline error: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        if getattr(args, 'debug', False) or getattr(args, 'verbose', False):
            import traceback
            traceback.print_exc()
        return 1


def handle_status_command(args, runner: PipelineRunner) -> int:
    """Handle the status command"""
    try:
        status = runner.get_pipeline_status()
        
        if args.json:
            import json
            print(json.dumps(status, indent=2))
        else:
            print_status_table(status)
            
        return 0
        
    except Exception as e:
        print(f"❌ Error getting status: {e}")
        return 1


def handle_list_command(args, registry: PhaseRegistry) -> int:
    """Handle the list command"""
    try:
        phases = registry.list_phases()
        
        if not phases:
            print("No phases found")
            return 1
            
        print_phases_table(phases, detailed=args.detailed)
        return 0
        
    except Exception as e:
        print(f"❌ Error listing phases: {e}")
        return 1


def handle_validate_command(args, runner: PipelineRunner) -> int:
    """Handle the validate command"""
    try:
        checks = runner.validate_environment()
        
        print("Environment Validation:")
        print("=" * 50)
        
        all_passed = True
        for check, passed in checks.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{check.replace('_', ' ').title():<20} {status}")
            if not passed:
                all_passed = False
                
        print("=" * 50)
        
        if all_passed:
            print("✅ All validation checks passed!")
            return 0
        else:
            print("❌ Some validation checks failed!")
            return 1
            
    except Exception as e:
        print(f"❌ Error validating environment: {e}")
        return 1


def print_status_table(status: dict) -> None:
    """Print a formatted status table"""
    print("Pipeline Status:")
    print("=" * 80)
    print(f"Total Phases: {status['total_phases']}")
    print(f"Completed: {status['completed_phases']}")
    print(f"Failed: {status['failed_phases']}")
    print(f"Pending: {status['total_phases'] - status['completed_phases'] - status['failed_phases']}")
    print()
    
    # Status symbols
    status_symbols = {
        'completed': '✅',
        'partial': '🔶', 
        'pending': '⭕',
        'failed': '❌',
        'unknown': '❓'
    }
    
    print(f"{'Phase':<8} {'Status':<12} {'Name':<30} {'Description'}")
    print("-" * 80)
    
    # Sort phases by ID
    sorted_phases = sorted(status['phases'].items(), key=lambda x: x[0])
    
    for phase_id, phase_info in sorted_phases:
        symbol = status_symbols.get(phase_info['status'], '❓')
        name = phase_info['name'][:28] + '...' if len(phase_info['name']) > 28 else phase_info['name']
        desc = phase_info['description'][:30] + '...' if len(phase_info['description']) > 30 else phase_info['description']
        
        print(f"{phase_id:<8} {symbol} {phase_info['status']:<10} {name:<30} {desc}")


def print_phases_table(phases: dict, detailed: bool = False) -> None:
    """Print a formatted phases table"""
    print("Available Phases:")
    print("=" * 80)
    
    if detailed:
        for phase_id in sorted(phases.keys()):
            metadata = phases[phase_id]
            print(f"\nPhase {phase_id}: {metadata.name}")
            print(f"  Description: {metadata.description}")
            print(f"  Dependencies: {', '.join(metadata.dependencies) if metadata.dependencies else 'None'}")
            print(f"  Outputs: {', '.join(metadata.outputs) if metadata.outputs else 'None'}")
            print(f"  Script: {metadata.script_path}")
    else:
        print(f"{'Phase':<8} {'Name':<30} {'Description'}")
        print("-" * 80)
        
        for phase_id in sorted(phases.keys()):
            metadata = phases[phase_id]
            name = metadata.name[:28] + '...' if len(metadata.name) > 28 else metadata.name
            desc = metadata.description[:40] + '...' if len(metadata.description) > 40 else metadata.description
            print(f"{phase_id:<8} {name:<30} {desc}")


def handle_debug_command(args, runner: PipelineRunner) -> int:
    """Handle the debug command"""
    try:
        from src.monitoring import PipelineLogger, get_global_profiler, get_global_tracker
        
        # Setup enhanced logging for debug mode
        logger = PipelineLogger.get_logger(
            "debug",
            log_level="DEBUG",
            dev_mode=True,
            console_output=True,
            json_output=getattr(args, 'log_format', 'console') == 'json'
        )
        
        if args.phase:
            print(f"🐛 Starting interactive debug for Phase {args.phase}")
            
            # Get phase metadata
            metadata = runner.registry.get_phase_metadata(args.phase)
            
            print(f"Phase: {metadata.name}")
            print(f"Description: {metadata.description}")
            print(f"Dependencies: {', '.join(metadata.dependencies)}")
            print(f"Script: {metadata.script_path}")
            print()
            
            # Interactive confirmation
            response = input("Continue with execution? (y/n/s for step-by-step): ").lower()
            
            if response == 's':
                print("🔍 Step-by-step execution mode enabled")
                # In a full implementation, this would enable breakpoints
                success = runner.run_phase(args.phase, dev_mode=True)
            elif response == 'y':
                success = runner.run_phase(args.phase, dev_mode=True)
            else:
                print("Debug session cancelled")
                return 0
            
            return 0 if success else 1
            
        elif args.step:
            print(f"🐛 Debug step: {args.step}")
            print("Step-level debugging not yet implemented")
            return 1
            
    except Exception as e:
        print(f"❌ Debug error: {e}")
        return 1


def handle_profile_command(args, runner: PipelineRunner) -> int:
    """Handle the profile command"""
    try:
        from src.monitoring import PerformanceProfiler
        
        # Initialize profiler
        profiler = PerformanceProfiler(
            save_dir="outputs/profiling",
            auto_save=True
        )
        
        print("🔬 Starting performance profiling...")
        
        if args.full:
            session_id = profiler.start_session("full_pipeline", "Full Pipeline Profile")
            success = runner.run_full_pipeline(dev_mode=True)
            profiler.end_session(session_id)
        elif args.phase:
            session_id = profiler.start_session(f"phase_{args.phase}", f"Phase {args.phase} Profile")
            success = runner.run_phase(args.phase, dev_mode=True)
            profiler.end_session(session_id)
        elif args.phases:
            session_id = profiler.start_session("multi_phase", f"Phases {args.phases} Profile")
            success = runner.run_phases(args.phases, dev_mode=True)
            profiler.end_session(session_id)
        else:
            print("❌ No profiling target specified")
            return 1
        
        # Generate report
        report = profiler.generate_report()
        
        print("\n📊 Performance Profile Summary:")
        print("=" * 50)
        print(f"Total Execution Time: {report['summary']['total_execution_time']:.2f}s")
        print(f"Total API Calls: {report['summary']['total_api_calls']}")
        print(f"Peak Memory: {report['summary']['peak_memory_mb']:.1f} MB")
        print(f"Total Errors: {report['summary']['total_errors']}")
        
        if report['summary']['slowest_operations']:
            print("\nSlowest Operations:")
            for i, op in enumerate(report['summary']['slowest_operations'][:5], 1):
                print(f"  {i}. {op['operation']}: {op['avg_time']:.3f}s avg ({op['count']} calls)")
        
        # Save report if requested
        if args.report:
            profiler.save_report(args.report)
        else:
            profiler.save_report()
        
        profiler.cleanup()
        
        return 0 if success else 1
        
    except Exception as e:
        print(f"❌ Profiling error: {e}")
        return 1


def handle_cost_command(args) -> int:
    """Handle the cost command"""
    try:
        from src.monitoring import CostTracker, BudgetAlert
        
        # Initialize cost tracker
        tracker = CostTracker(
            save_dir="outputs/cost_tracking",
            auto_save=True
        )
        
        if args.cost_action == 'status':
            status = tracker.get_budget_status()
            
            print("💰 Budget Status:")
            print("=" * 40)
            print(f"Budget Limit: ${status['budget_limit']:.2f}")
            print(f"Total Spent: ${status['total_spent']:.2f}")
            print(f"Remaining: ${status['remaining_budget']:.2f}")
            print(f"Used: {status['budget_used_percent']:.1f}%")
            print(f"Today: ${status['today_spent']:.2f}")
            
            status_symbols = {
                'ok': '✅',
                'warning': '⚠️',
                'critical': '🚨',
                'over_budget': '🚫'
            }
            symbol = status_symbols.get(status['status'], '❓')
            print(f"Status: {symbol} {status['status'].upper()}")
            
        elif args.cost_action == 'report':
            summary = tracker.get_cost_summary(args.period)
            
            print(f"💰 Cost Report - {args.period.title()}:")
            print("=" * 50)
            print(f"Total Cost: ${summary['total_cost']:.2f}")
            print(f"Total Requests: {summary['total_requests']}")
            print(f"Total Tokens: {summary['total_tokens']:,}")
            
            if summary['total_requests'] > 0:
                print(f"Avg Cost/Request: ${summary['avg_cost_per_request']:.4f}")
                print(f"Avg Cost/1K Tokens: ${summary['avg_cost_per_1k_tokens']:.4f}")
            
            if summary['by_provider']:
                print("\nBy Provider:")
                for provider, metrics in summary['by_provider'].items():
                    print(f"  {provider}: ${metrics['total_cost']:.2f} ({metrics['requests']} calls)")
            
            # Save report if requested
            if args.save:
                tracker.save_cost_report(args.save)
            
        elif args.cost_action == 'budget':
            if args.set:
                tracker.set_budget_limit(args.set)
                print(f"✅ Budget limit set to ${args.set:.2f}")
            
            if args.alert:
                threshold, period, alert_type = args.alert
                alert = BudgetAlert(
                    threshold=float(threshold),
                    period=period,
                    alert_type=alert_type
                )
                tracker.add_budget_alert(alert)
                print(f"✅ Added budget alert: ${threshold} ({period}, {alert_type})")
        
        return 0
        
    except Exception as e:
        print(f"❌ Cost tracking error: {e}")
        return 1


def handle_monitor_command(args) -> int:
    """Handle the monitor command"""
    try:
        from src.monitoring import get_global_profiler, get_global_cost_tracker
        import time
        
        print("📊 Pipeline Monitor")
        print("=" * 50)
        
        if args.follow:
            print("Following logs... (Press Ctrl+C to stop)")
            try:
                # In a full implementation, this would tail log files
                while True:
                    if args.metrics:
                        # Show real-time metrics
                        profiler = get_global_profiler()
                        cost_tracker = get_global_cost_tracker()
                        
                        system_metrics = profiler.get_system_metrics()
                        cost_status = cost_tracker.get_budget_status()
                        
                        print(f"\r🖥️  CPU: {system_metrics.get('process', {}).get('cpu_percent', 0):.1f}% "
                              f"MEM: {system_metrics.get('process', {}).get('memory_mb', 0):.0f}MB "
                              f"COST: ${cost_status.get('total_spent', 0):.2f}", end='', flush=True)
                    
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                print("\n📊 Monitoring stopped")
                return 0
        
        else:
            # Show current status
            profiler = get_global_profiler()
            active_sessions = profiler.get_active_sessions()
            
            if active_sessions:
                print("Active Profiling Sessions:")
                for session in active_sessions:
                    duration = session.duration or (time.time() - session.start_time)
                    print(f"  - {session.name}: {duration:.1f}s")
            else:
                print("No active profiling sessions")
        
        return 0
        
    except Exception as e:
        print(f"❌ Monitor error: {e}")
        return 1


def handle_outputs_command(args) -> int:
    """Handle the outputs command"""
    try:
        from src.outputs import OutputManager
        
        # Initialize output manager
        manager = OutputManager()
        
        if args.list:
            # List current and archived outputs
            current_info = manager.list_current_outputs()
            archived_info = manager.list_archived_runs()
            
            if args.json:
                import json
                output = {
                    "current_run": current_info,
                    "archived_runs": archived_info
                }
                print(json.dumps(output, indent=2))
            else:
                print("📁 Pipeline Outputs")
                print("=" * 50)
                
                # Current run info
                print("Current Run:")
                if current_info["status"] == "no_current_run":
                    print("  ❌ No current run")
                else:
                    print(f"  ✅ {current_info['status']}")
                    print(f"  📄 Files: {current_info['total_files']}")
                    print(f"  💾 Size: {current_info['total_size'] / 1024:.1f} KB")
                    
                    if current_info.get('metadata', {}).get('run_id'):
                        print(f"  🏷️  ID: {current_info['metadata']['run_id']}")
                
                print()
                
                # Archived runs info
                print(f"Archived Runs ({len(archived_info)}):")
                if not archived_info:
                    print("  📭 No archived runs")
                else:
                    for i, archive in enumerate(archived_info[:5], 1):  # Show last 5
                        size_kb = archive.get("total_size", 0) / 1024
                        compressed = "🗜️" if archive.get("compressed", False) else "📁"
                        print(f"  {i}. {compressed} {archive['archive_id']} ({size_kb:.1f} KB)")
                    
                    if len(archived_info) > 5:
                        print(f"  ... and {len(archived_info) - 5} more")
        
        elif args.archive:
            # Archive current run
            print("📦 Archiving current run...")
            success = manager.archive_current_run()
            
            if success:
                print("✅ Successfully archived current run")
                return 0
            else:
                print("❌ Failed to archive current run")
                return 1
        
        elif args.clean is not None:
            # Clean old archives
            keep_count = args.clean
            print(f"🧹 Cleaning old archives, keeping {keep_count} most recent...")
            
            removed_count = manager.clean_old_archives(keep_count)
            
            if removed_count > 0:
                print(f"✅ Cleaned {removed_count} old archives")
            else:
                print("ℹ️  No archives to clean")
            
            return 0
        
        elif args.export_paper:
            # Export final paper
            format = args.export_paper
            output_file = None
            
            if args.output_file:
                from pathlib import Path
                output_file = Path(args.output_file)
            
            print(f"📄 Exporting final paper in {format.upper()} format...")
            
            exported_path = manager.export_final_paper(format, output_file)
            
            if exported_path:
                print(f"✅ Successfully exported to: {exported_path}")
                return 0
            else:
                print("❌ Failed to export final paper")
                return 1
        
        elif args.statistics:
            # Show comprehensive statistics
            stats = manager.get_run_statistics()
            
            if args.json:
                import json
                print(json.dumps(stats, indent=2))
            else:
                print("📊 Output Statistics")
                print("=" * 50)
                
                # Current run stats
                current = stats["current_run"]
                print("Current Run:")
                print(f"  Status: {current['status']}")
                print(f"  Files: {current['file_count']}")
                print(f"  Size: {current['total_size'] / 1024:.1f} KB")
                print()
                
                # Archive stats
                archives = stats["archives"]
                print("Archives:")
                print(f"  Total: {archives['total_count']}")
                print(f"  Size: {archives['total_size'] / 1024:.1f} KB")
                print(f"  Recent (24h): {archives['recent_runs_today']}")
                print()
                
                # Disk usage
                usage = stats["disk_usage"]
                print("Disk Usage:")
                print(f"  Current: {usage['current_size'] / 1024:.1f} KB")
                print(f"  Archived: {usage['archive_size'] / 1024:.1f} KB")
                print(f"  Total: {usage['total_size'] / 1024:.1f} KB")
        
        return 0
        
    except Exception as e:
        print(f"❌ Outputs error: {e}")
        if hasattr(args, 'verbose') and args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def handle_setup_command(args) -> int:
    """Handle the interactive setup wizard"""
    import os
    import sys
    from pathlib import Path
    import subprocess
    
    print("🚀 Philosophy Pipeline Setup Wizard")
    print("=" * 50)
    
    if args.validate_only:
        print("📋 Validating existing setup...")
        try:
            runner = PipelineRunner(config_path=args.config)
            checks = runner.validate_environment()
            
            all_passed = True
            for check, passed in checks.items():
                status = "✅" if passed else "❌"
                print(f"{check.replace('_', ' ').title():<20} {status}")
                if not passed:
                    all_passed = False
            
            return 0 if all_passed else 1
        except Exception as e:
            print(f"❌ Validation failed: {e}")
            return 1
    
    # Welcome message
    print("\nWelcome to the AI-Driven Philosophy Paper Generator!")
    print("This wizard will help you set up the pipeline for the first time.\n")
    
    if not args.quick:
        response = input("Would you like to proceed with the setup? (y/n): ").lower()
        if response != 'y':
            print("Setup cancelled.")
            return 0
    
    setup_steps = []
    
    # Step 1: Check Python environment
    print("\n📍 Step 1: Python Environment")
    print("-" * 30)
    
    python_version = sys.version_info
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("❌ Python 3.8+ required. Please upgrade Python.")
        return 1
    else:
        print("✅ Python version OK")
    
    # Check virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    if in_venv:
        print("✅ Running in virtual environment")
    else:
        print("⚠️  Not in virtual environment. Consider using: python -m venv venv && source venv/bin/activate")
        if not args.quick:
            response = input("Continue anyway? (y/n): ").lower()
            if response != 'y':
                print("Setup cancelled. Please activate virtual environment first.")
                return 1
    
    setup_steps.append("✅ Python environment checked")
    
    # Step 2: Check dependencies
    print("\n📍 Step 2: Python Dependencies")
    print("-" * 30)
    
    required_packages = ['anthropic', 'openai', 'pyyaml', 'requests', 'python-dotenv']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (missing)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        if not args.quick:
            response = input("Install missing packages now? (y/n): ").lower()
            if response == 'y':
                try:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
                    print("✅ Dependencies installed")
                except subprocess.CalledProcessError:
                    print("❌ Failed to install dependencies. Please install manually:")
                    print(f"pip install {' '.join(missing_packages)}")
                    return 1
        else:
            print("❌ Missing dependencies. Please install with: pip install -r requirements.txt")
            return 1
    
    setup_steps.append("✅ Dependencies verified")
    
    # Step 3: API Keys setup
    print("\n📍 Step 3: API Keys Configuration")
    print("-" * 30)
    
    env_file = Path('.env')
    env_content = {}
    
    if env_file.exists():
        print("✅ .env file exists")
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    env_content[key] = value
    else:
        print("📝 Creating .env file")
    
    # Check required API keys
    api_keys = {
        'ANTHROPIC_API_KEY': 'Anthropic API key (required for all phases)',
        'OPENAI_API_KEY': 'OpenAI API key (optional, for complex reasoning)',
        'TAVILY_API_KEY': 'Tavily Search API key (required for Phase I.2)'
    }
    
    keys_configured = 0
    for key, description in api_keys.items():
        current_value = env_content.get(key, '').strip('"\'')
        
        if current_value and len(current_value) > 10:
            print(f"✅ {key} configured")
            keys_configured += 1
        else:
            print(f"❌ {key} not configured - {description}")
            
            if not args.quick:
                new_value = input(f"Enter {key} (or press Enter to skip): ").strip()
                if new_value:
                    env_content[key] = new_value
                    keys_configured += 1
                    print(f"✅ {key} configured")
    
    # Write updated .env file
    if env_content:
        with open(env_file, 'w') as f:
            for key, value in env_content.items():
                f.write(f"{key}={value}\n")
    
    if keys_configured < 1:
        print("⚠️  No API keys configured. At least Anthropic API key is required.")
        if not args.quick:
            print("You can configure them later by editing the .env file")
    
    setup_steps.append(f"✅ API keys configured ({keys_configured}/3)")
    
    # Step 4: Test API connectivity
    print("\n📍 Step 4: API Connectivity Test")
    print("-" * 30)
    
    if env_content.get('ANTHROPIC_API_KEY'):
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=env_content['ANTHROPIC_API_KEY'])
            # Simple test call
            response = client.messages.create(
                model="claude-sonnet-4",
                max_tokens=10,
                messages=[{"role": "user", "content": "Hello"}]
            )
            print("✅ Anthropic API connection successful")
            setup_steps.append("✅ Anthropic API tested")
        except Exception as e:
            print(f"❌ Anthropic API test failed: {e}")
            print("   Please check your API key and account credits")
    
    # Step 5: Directory structure
    print("\n📍 Step 5: Directory Structure")
    print("-" * 30)
    
    required_dirs = ['papers', 'outputs', 'config', 'src']
    for directory in required_dirs:
        dir_path = Path(directory)
        if dir_path.exists():
            print(f"✅ {directory}/ exists")
        else:
            print(f"📁 Creating {directory}/")
            dir_path.mkdir(exist_ok=True)
    
    setup_steps.append("✅ Directory structure verified")
    
    # Step 6: Sample literature
    print("\n📍 Step 6: Sample Literature Setup")
    print("-" * 30)
    
    papers_dir = Path('papers')
    existing_pdfs = list(papers_dir.glob('*.pdf'))
    
    if existing_pdfs:
        print(f"✅ Found {len(existing_pdfs)} PDF files in papers/")
        setup_steps.append("✅ Literature files ready")
    else:
        print("📚 No PDF files found in papers/")
        
        sample_papers_dir = Path('sample_output_papers/paper_1/papers')
        if sample_papers_dir.exists():
            sample_pdfs = list(sample_papers_dir.glob('*.pdf'))
            if sample_pdfs and not args.quick:
                print(f"Found {len(sample_pdfs)} sample papers")
                response = input("Copy sample papers to papers/ directory? (y/n): ").lower()
                if response == 'y':
                    import shutil
                    for pdf in sample_pdfs:
                        shutil.copy2(pdf, papers_dir)
                    print("✅ Sample papers copied")
                    setup_steps.append("✅ Sample literature copied")
        
        if not list(papers_dir.glob('*.pdf')):
            print("⚠️  No literature available. You'll need to add PDF files to papers/ before running the pipeline")
            setup_steps.append("⚠️  No literature files (manual setup needed)")
    
    # Step 7: Configuration validation
    print("\n📍 Step 7: Configuration Validation")
    print("-" * 30)
    
    config_file = Path('config/conceptual_config.yaml')
    if config_file.exists():
        try:
            import yaml
            with open(config_file) as f:
                config = yaml.safe_load(f)
            print("✅ Configuration file valid")
            setup_steps.append("✅ Configuration validated")
        except Exception as e:
            print(f"❌ Configuration file error: {e}")
            setup_steps.append("❌ Configuration needs fixing")
    else:
        print("❌ Configuration file not found")
        setup_steps.append("❌ Configuration missing")
    
    # Setup Summary
    print("\n🎉 Setup Summary")
    print("=" * 50)
    
    for step in setup_steps:
        print(f"  {step}")
    
    all_good = all("✅" in step for step in setup_steps)
    
    if all_good:
        print("\n🚀 Setup complete! You're ready to generate philosophy papers.")
        print("\nNext steps:")
        print("  1. python pipeline_cli.py validate    # Final validation")
        print("  2. python pipeline_cli.py run --full  # Generate your first paper")
        print("\nFor help: python pipeline_cli.py --help")
        
        if not args.quick:
            response = input("\nRun validation now? (y/n): ").lower()
            if response == 'y':
                try:
                    runner = PipelineRunner(config_path=args.config)
                    checks = runner.validate_environment()
                    
                    print("\n📋 Final Validation:")
                    for check, passed in checks.items():
                        status = "✅" if passed else "❌"
                        print(f"  {check.replace('_', ' ').title():<20} {status}")
                except Exception as e:
                    print(f"❌ Validation failed: {e}")
        
        return 0
    else:
        print("\n⚠️  Setup completed with issues. Please resolve the items marked with ❌ before using the pipeline.")
        return 1


def main() -> int:
    """Main CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    # If no command specified, show help
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        # Setup enhanced logging based on arguments
        log_level = "DEBUG" if args.debug else ("INFO" if args.verbose else "WARNING")
        
        # Initialize monitoring if needed
        if hasattr(args, 'profile') and args.profile:
            from src.monitoring import PerformanceProfiler, set_global_profiler
            profiler = PerformanceProfiler(
                save_dir="outputs/profiling",
                auto_save=True
            )
            set_global_profiler(profiler)
        
        if hasattr(args, 'track_costs') and args.track_costs:
            from src.monitoring import CostTracker, set_global_cost_tracker
            cost_tracker = CostTracker(
                save_dir="outputs/cost_tracking",
                auto_save=True,
                default_budget_limit=getattr(args, 'budget', 100.0)
            )
            set_global_cost_tracker(cost_tracker)
        
        # Handle commands that don't need pipeline initialization
        if args.command == 'cost':
            return handle_cost_command(args)
        elif args.command == 'monitor':
            return handle_monitor_command(args)
        elif args.command == 'outputs':
            return handle_outputs_command(args)
        elif args.command == 'setup':
            return handle_setup_command(args)
        
        # Initialize components for pipeline commands
        runner = PipelineRunner(config_path=args.config)
        registry = runner.registry
        
        # Setup enhanced logging for runner
        if hasattr(args, 'log_dir') and args.log_dir:
            from src.monitoring import PipelineLogger
            logger = PipelineLogger.get_logger(
                "pipeline",
                log_level=log_level,
                log_dir=args.log_dir,
                dev_mode=getattr(args, 'dev', False),
                json_output=getattr(args, 'log_format', 'console') == 'json'
            )
            runner.logger = logger
        
        # Discover phases
        phases = registry.discover_phases()
        if not phases:
            print("❌ No phases discovered. Check project structure.")
            return 1
            
        if args.verbose or args.debug:
            print(f"Discovered {len(phases)} phases")
        
        # Handle commands
        if args.command == 'run':
            return handle_run_command(args, runner)
        elif args.command == 'status':
            return handle_status_command(args, runner)
        elif args.command == 'list':
            return handle_list_command(args, registry)
        elif args.command == 'validate':
            return handle_validate_command(args, runner)
        elif args.command == 'debug':
            return handle_debug_command(args, runner)
        elif args.command == 'profile':
            return handle_profile_command(args, runner)
        else:
            print(f"❌ Unknown command: {args.command}")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️  Execution interrupted by user")
        return 130
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        if hasattr(args, 'debug') and args.debug:
            import traceback
            traceback.print_exc()
        elif hasattr(args, 'verbose') and args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def main() -> int:
    """Main entry point for the CLI"""
    try:
        args = create_parser().parse_args()
        
        # Handle global options
        if args.verbose or args.debug:
            logging.basicConfig(
                level=logging.DEBUG if args.debug else logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        
        # Initialize pipeline runner
        try:
            runner = PipelineRunner(config_path=args.config)
        except Exception as e:
            print(f"❌ Failed to initialize pipeline: {e}")
            return 1
        
        # Route to appropriate command handler
        if args.command == 'run':
            return handle_run_command(args, runner)
        elif args.command == 'status':
            return handle_status_command(args, runner)
        elif args.command == 'list':
            return handle_list_command(args, runner)
        elif args.command == 'validate':
            return handle_validate_command(args, runner)
        elif args.command == 'setup':
            return handle_setup_command(args)
        elif args.command == 'debug':
            return handle_debug_command(args, runner)
        elif args.command == 'profile':
            return handle_profile_command(args, runner)
        elif args.command == 'cost':
            return handle_cost_command(args, runner)
        elif args.command == 'monitor':
            return handle_monitor_command(args, runner)
        elif args.command == 'outputs':
            return handle_outputs_command(args, runner)
        else:
            print("❌ No command specified")
            return 1
            
    except KeyboardInterrupt:
        print("\n\n❌ Execution cancelled by user")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())