#!/usr/bin/env python3
"""
Demo script showing how phase scripts can integrate with monitoring
"""

import json
import os
import sys
import time
from pathlib import Path

def print_monitoring_data(data_type: str, **data):
    """Print monitoring data in a format the pipeline runner can parse"""
    monitoring_data = {
        "type": data_type,
        **data
    }
    print(f"[MONITORING]{json.dumps(monitoring_data)}")

def demo_api_call(provider: str, model: str, input_tokens: int, output_tokens: int):
    """Simulate an API call with monitoring"""
    start_time = time.time()
    
    # Simulate API call delay
    time.sleep(0.5)  
    
    latency = time.time() - start_time
    
    # Report API call to monitoring
    print_monitoring_data(
        "api_call",
        provider=provider,
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        latency=latency,
        success=True
    )
    
    print(f"Made API call to {provider}/{model}: {input_tokens} in, {output_tokens} out")

def demo_progress_update(increment: int, message: str):
    """Update progress with monitoring"""
    print_monitoring_data(
        "progress_update",
        increment=increment,
        message=message
    )
    
    print(f"Progress: {message}")

def demo_performance_metric(metric_name: str, value: float, unit: str):
    """Record performance metric"""
    print_monitoring_data(
        "performance_metric",
        metric_name=metric_name,
        value=value,
        unit=unit
    )
    
    print(f"Performance: {metric_name} = {value} {unit}")

def main():
    """Main demo function"""
    print("🧪 Demo: Phase Script with Monitoring Integration")
    print("=" * 60)
    
    # Check if monitoring is enabled
    monitoring_enabled = os.getenv('PIPELINE_MONITORING_ENABLED') == '1'
    dev_mode = os.getenv('PIPELINE_DEV_MODE') == '1'
    
    print(f"Monitoring enabled: {monitoring_enabled}")
    print(f"Development mode: {dev_mode}")
    print()
    
    # Simulate phase work with progress updates
    demo_progress_update(10, "Initializing phase")
    time.sleep(0.2)
    
    demo_progress_update(20, "Loading data")
    time.sleep(0.2)
    
    # Simulate API calls with cost tracking
    demo_api_call("anthropic", "claude-3-sonnet", 1500, 800)
    demo_progress_update(40, "Processed first batch")
    
    demo_api_call("anthropic", "claude-3-sonnet", 1200, 600)
    demo_progress_update(60, "Processed second batch")
    
    # Record some performance metrics
    demo_performance_metric("processing_rate", 125.5, "items/sec")
    demo_performance_metric("memory_usage", 256.8, "MB")
    
    demo_progress_update(80, "Generating output")
    time.sleep(0.3)
    
    demo_progress_update(100, "Phase completed successfully")
    
    print()
    print("✅ Demo phase script completed!")
    
    # Show integration features if in dev mode
    if dev_mode:
        print()
        print("🔧 Development Mode Features:")
        print("  - Detailed logging enabled")
        print("  - Performance profiling active")
        print("  - API cost tracking enabled")
        print("  - Progress monitoring active")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())