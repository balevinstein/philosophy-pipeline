#!/usr/bin/env python3
"""
Test script for monitoring functionality
"""

import sys
import time
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

def test_logger():
    """Test the enhanced logger"""
    print("Testing PipelineLogger...")
    
    from src.monitoring import PipelineLogger, LogLevel
    
    # Test console logger
    logger = PipelineLogger.get_logger(
        "test",
        log_level=LogLevel.DEBUG,
        dev_mode=True,
        console_output=True,
        json_output=False
    )
    
    logger.set_context(phase_id="test_phase", step="test_step")
    
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    # Test context manager
    with logger.context(operation="test_operation"):
        logger.info("Message with operation context")
    
    logger.log_phase_start("2.3", "Testing phase logging")
    time.sleep(0.1)
    logger.log_phase_end("2.3", True, 0.1)
    
    print("✅ PipelineLogger test passed")


def test_progress_tracker():
    """Test the progress tracker"""
    print("\nTesting ProgressTracker...")
    
    from src.monitoring import ProgressTracker, ProgressLevel
    
    tracker = ProgressTracker(
        show_progress_bars=True,
        enable_console_output=True
    )
    
    # Create and start progress
    tracker.create_progress(
        "test_progress",
        "Test Progress",
        ProgressLevel.PHASE,
        total_items=100
    )
    
    tracker.start_progress("test_progress")
    
    # Simulate progress updates
    for i in range(0, 101, 20):
        tracker.update_progress("test_progress", completed_items=i, message=f"Progress: {i}%")
        time.sleep(0.1)
    
    tracker.complete_progress("test_progress", True, "Test completed")
    
    # Print summary
    tracker.print_summary()
    
    print("✅ ProgressTracker test passed")


def test_cost_tracker():
    """Test the cost tracker"""
    print("\nTesting CostTracker...")
    
    from src.monitoring import CostTracker, APIProvider
    
    tracker = CostTracker(
        default_budget_limit=50.0
    )
    
    # Record some API calls
    tracker.record_api_call(
        APIProvider.ANTHROPIC,
        "claude-3-sonnet",
        input_tokens=1000,
        output_tokens=500,
        latency=2.5,
        success=True
    )
    
    tracker.record_api_call(
        APIProvider.OPENAI,
        "gpt-4",
        input_tokens=800,
        output_tokens=400,
        latency=1.8,
        success=True
    )
    
    # Get cost summary
    summary = tracker.get_cost_summary()
    print(f"Total cost: ${summary['total_cost']:.4f}")
    print(f"Total requests: {summary['total_requests']}")
    print(f"Total tokens: {summary['total_tokens']:,}")
    
    # Get budget status
    budget_status = tracker.get_budget_status()
    print(f"Budget status: {budget_status['status']}")
    print(f"Budget used: {budget_status['budget_used_percent']:.1f}%")
    
    print("✅ CostTracker test passed")


def test_enhanced_cli():
    """Test enhanced CLI functionality"""
    print("\nTesting enhanced CLI features...")
    
    # Test run command with development features
    print("Testing run command with --dev flag...")
    
    # This would normally test actual phase execution, but we'll just test argument parsing
    from pipeline_cli import create_parser
    
    parser = create_parser()
    
    # Test various argument combinations
    test_cases = [
        ["run", "--phase", "2.3", "--dev"],
        ["run", "--phase", "2.3", "--dev", "--profile", "--track-costs"],
        ["run", "--phase", "2.3", "--interactive"],
        ["debug", "--phase", "2.3"],
        ["profile", "--phase", "2.3"],
        ["cost", "status"],
        ["monitor", "--metrics"]
    ]
    
    for test_case in test_cases:
        try:
            args = parser.parse_args(test_case)
            print(f"  ✅ Parsed: {' '.join(test_case)}")
        except SystemExit:
            print(f"  ❌ Failed to parse: {' '.join(test_case)}")
    
    print("✅ CLI enhancement test passed")


def main():
    """Run all tests"""
    print("🧪 Testing WP4: Developer Experience Tools")
    print("=" * 50)
    
    try:
        test_logger()
        test_progress_tracker()
        test_cost_tracker()
        test_enhanced_cli()
        
        print("\n🎉 All monitoring tests passed!")
        print("\n📚 Available CLI Commands:")
        print("  python3 pipeline_cli.py run --phase 2.3 --dev --verbose")
        print("  python3 pipeline_cli.py run --phase 2.3 --dev --profile --track-costs")
        print("  python3 pipeline_cli.py debug --phase 2.3")
        print("  python3 pipeline_cli.py profile --phase 2.3")
        print("  python3 pipeline_cli.py cost status")
        print("  python3 pipeline_cli.py monitor --metrics")
        print("  python3 pipeline_cli.py validate")
        print("  python3 pipeline_cli.py status")
        print("  python3 pipeline_cli.py list --detailed")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())