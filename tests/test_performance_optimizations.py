#!/usr/bin/env python3
"""Test script for performance optimizations in the philosophy pipeline."""

import time
import tempfile
from pathlib import Path
import sys
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_dependency_structure():
    """Test that the new dependency structure works correctly."""
    print("Testing dependency structure...")
    
    # Check if requirement files exist
    req_dir = Path(__file__).parent / "requirements"
    
    required_files = ["base.txt", "dev.txt", "optional.txt"]
    for req_file in required_files:
        req_path = req_dir / req_file
        if req_path.exists():
            print(f"✓ {req_file} exists")
            
            # Basic validation - check it contains some dependencies
            content = req_path.read_text()
            if len(content.strip().split('\n')) > 5:
                print(f"  ✓ Contains {len(content.strip().split('\n'))} dependencies")
            else:
                print(f"  ⚠ Only contains {len(content.strip().split('\n'))} dependencies")
        else:
            print(f"✗ {req_file} missing")
    
    print()

def test_performance_modules():
    """Test that performance modules can be imported and initialized."""
    print("Testing performance module imports...")
    
    try:
        from src.performance import APICache, BatchProcessor, MemoryManager
        print("✓ Performance modules imported successfully")
        
        # Test APICache
        try:
            cache = APICache(cache_dir=Path(tempfile.gettempdir()) / "test_cache")
            print("✓ APICache initialized")
            
            # Test basic cache operations
            test_prompt = "This is a test prompt"
            test_config = {"model": "test-model", "temperature": 0.7, "max_tokens": 1000}
            test_response = "This is a test response"
            
            # Cache miss
            result = cache.get(test_prompt, test_config)
            if result is None:
                print("✓ Cache miss handled correctly")
            
            # Cache put
            cache.put(test_prompt, test_config, test_response)
            print("✓ Cache put successful")
            
            # Cache hit
            result = cache.get(test_prompt, test_config)
            if result == test_response:
                print("✓ Cache hit successful")
            
            # Get stats
            stats = cache.get_stats()
            print(f"✓ Cache stats: {stats['cache_entries']} entries, {stats['hit_rate']:.1%} hit rate")
            
        except Exception as e:
            print(f"✗ APICache test failed: {e}")
        
        # Test MemoryManager
        try:
            mem_manager = MemoryManager(enable_monitoring=False)
            print("✓ MemoryManager initialized")
            
            stats = mem_manager.get_memory_stats()
            print(f"✓ Memory stats: {stats.process_mb:.1f}MB used, {stats.percent_used:.1f}% system usage")
            
        except Exception as e:
            print(f"✗ MemoryManager test failed: {e}")
        
        # Test BatchProcessor
        try:
            batch_processor = BatchProcessor(max_concurrent=2, batch_delay=0.1)
            print("✓ BatchProcessor initialized")
            
            # Don't start processing thread for test
            batch_stats = batch_processor.get_stats()
            print(f"✓ Batch stats: {batch_stats['queue_size']} queued")
            
        except Exception as e:
            print(f"✗ BatchProcessor test failed: {e}")
            
    except ImportError as e:
        print(f"✗ Could not import performance modules: {e}")
        print("  This is expected if psutil is not installed")
    
    print()

def test_api_handler_integration():
    """Test that the API handler integrates performance optimizations."""
    print("Testing API handler integration...")
    
    try:
        # Test imports
        from src.utils.api import APIHandler
        print("✓ APIHandler imported successfully")
        
        # Test initialization with performance features disabled (to avoid needing API keys)
        try:
            # This will fail due to missing API keys, but we can catch that
            handler = APIHandler(
                config={"models": {"test": {"provider": "anthropic", "model": "test"}}},
                enable_caching=False,
                enable_batching=False, 
                enable_memory_management=False
            )
        except ValueError as e:
            if "API_KEY" in str(e):
                print("✓ API handler properly checks for API keys")
            else:
                print(f"✗ Unexpected error: {e}")
        except Exception as e:
            print(f"✗ Unexpected error during APIHandler init: {e}")
        
        # Test that performance methods exist
        handler_methods = [
            'make_api_call_cached',
            'make_batch_api_calls',
            'process_large_pdf_optimized',
            'get_performance_stats',
            'optimize_performance',
            'clear_cache',
            'invalidate_model_cache'
        ]
        
        for method in handler_methods:
            if hasattr(APIHandler, method):
                print(f"✓ Method {method} exists")
            else:
                print(f"✗ Method {method} missing")
        
    except Exception as e:
        print(f"✗ API handler integration test failed: {e}")
    
    print()

def test_performance_dashboard():
    """Test the performance dashboard functionality."""
    print("Testing performance dashboard...")
    
    try:
        from src.performance.dashboard import PerformanceDashboard
        
        # Create dashboard with temporary metrics file
        temp_file = Path(tempfile.gettempdir()) / "test_metrics.json"
        dashboard = PerformanceDashboard(temp_file)
        print("✓ Performance dashboard initialized")
        
        # Record some test API calls
        dashboard.record_api_call("test_stage", 1.5, cached=False, model="test-model", tokens_estimated=500)
        dashboard.record_api_call("test_stage", 0.1, cached=True, model="test-model", tokens_estimated=500)
        print("✓ API calls recorded")
        
        # Test stats
        session_stats = dashboard.get_current_session_stats()
        print(f"✓ Session stats: {session_stats['total_calls']} calls, {session_stats['cache_hit_rate']:.1%} hit rate")
        
        overall_stats = dashboard.get_overall_stats()
        print(f"✓ Overall stats: {overall_stats['api_calls']} total calls")
        
        # Test report generation
        report = dashboard.generate_performance_report()
        if len(report) > 100:
            print("✓ Performance report generated")
            print(f"  Report length: {len(report)} characters")
        else:
            print("✗ Performance report seems too short")
            
        # Cleanup
        if temp_file.exists():
            temp_file.unlink()
            
    except Exception as e:
        print(f"✗ Performance dashboard test failed: {e}")
    
    print()

def test_memory_optimization():
    """Test memory optimization features."""
    print("Testing memory optimization...")
    
    try:
        from src.performance.memory_manager import MemoryManager
        
        with MemoryManager(enable_monitoring=False) as mem_manager:
            print("✓ Memory manager context manager works")
            
            # Test memory stats
            stats = mem_manager.get_memory_stats()
            print(f"✓ Memory stats: {stats.process_mb:.1f}MB process memory")
            
            # Test garbage collection
            collected = mem_manager.force_garbage_collection()
            print(f"✓ Garbage collection: {collected} objects collected")
            
            # Test file streaming (create a temporary file)
            test_file = Path(tempfile.gettempdir()) / "test_large_file.txt"
            test_content = "This is test content for memory optimization.\n" * 1000
            test_file.write_text(test_content)
            
            try:
                with mem_manager.stream_large_file(test_file, use_mmap=False) as file_stream:
                    chunk_count = 0
                    for chunk in file_stream:
                        chunk_count += 1
                        if chunk_count > 10:  # Don't process entire file
                            break
                    print(f"✓ File streaming: processed {chunk_count} chunks")
                    
            finally:
                test_file.unlink()
                
            # Test memory report
            report = mem_manager.create_memory_report()
            if "Memory Usage Report" in report:
                print("✓ Memory report generated")
            
    except Exception as e:
        print(f"✗ Memory optimization test failed: {e}")
    
    print()

def benchmark_cache_performance():
    """Benchmark cache performance improvement."""
    print("Benchmarking cache performance...")
    
    try:
        from src.performance.api_cache import APICache
        
        cache = APICache(cache_dir=Path(tempfile.gettempdir()) / "benchmark_cache")
        
        # Test data
        test_prompts = [
            f"This is test prompt number {i} for benchmarking cache performance."
            for i in range(10)
        ]
        test_config = {"model": "test-model", "temperature": 0.7, "max_tokens": 1000}
        
        # Simulate cache misses (first time)
        start_time = time.time()
        for prompt in test_prompts:
            result = cache.get(prompt, test_config)
            if result is None:
                # Simulate API response
                time.sleep(0.01)  # Simulate API call delay
                response = f"Response for: {prompt[:50]}..."
                cache.put(prompt, test_config, response)
        
        miss_time = time.time() - start_time
        print(f"✓ Cache misses: {miss_time:.3f}s for {len(test_prompts)} requests")
        
        # Simulate cache hits (second time)
        start_time = time.time()
        hit_count = 0
        for prompt in test_prompts:
            result = cache.get(prompt, test_config)
            if result is not None:
                hit_count += 1
        
        hit_time = time.time() - start_time
        print(f"✓ Cache hits: {hit_time:.3f}s for {hit_count} requests")
        
        if hit_count > 0:
            speedup = miss_time / hit_time if hit_time > 0 else float('inf')
            print(f"✓ Performance improvement: {speedup:.1f}x faster with cache")
            
        # Cache statistics
        stats = cache.get_stats()
        print(f"✓ Cache efficiency: {stats['hit_rate']:.1%} hit rate, {stats['cache_entries']} entries")
        
    except Exception as e:
        print(f"✗ Cache performance benchmark failed: {e}")
    
    print()

def run_all_tests():
    """Run all performance optimization tests."""
    print("=" * 60)
    print("Philosophy Pipeline Performance Optimization Tests")
    print("=" * 60)
    print()
    
    test_dependency_structure()
    test_performance_modules()
    test_api_handler_integration()
    test_performance_dashboard()
    test_memory_optimization()
    benchmark_cache_performance()
    
    print("=" * 60)
    print("Performance optimization tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()