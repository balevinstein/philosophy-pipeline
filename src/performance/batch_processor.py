"""Batch processing for multiple API calls with intelligent batching strategies."""

import asyncio
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Callable, Tuple, Union
from pathlib import Path
import threading

logger = logging.getLogger(__name__)


@dataclass
class BatchRequest:
    """Represents a single request in a batch."""
    id: str
    stage: str
    prompt: str
    model_config: Dict[str, Any]
    system_prompt: Optional[str] = None
    text_paths: Optional[List[Path]] = None
    pdf_path: Optional[Path] = None
    pdf_paths: Optional[List[Path]] = None
    priority: int = 1  # Higher number = higher priority
    estimated_tokens: Optional[int] = None


@dataclass
class BatchResult:
    """Result of a batch request."""
    request_id: str
    response: str
    duration: float
    success: bool
    error: Optional[str] = None
    cached: bool = False


class BatchProcessor:
    """Intelligent batch processor for API calls."""

    def __init__(
        self,
        max_concurrent: int = 5,
        batch_delay: float = 2.0,
        max_batch_size: int = 10,
        enable_adaptive_batching: bool = True,
        rate_limit_rpm: int = 60  # requests per minute
    ):
        """Initialize batch processor.
        
        Args:
            max_concurrent: Maximum concurrent API calls
            batch_delay: Delay to collect requests for batching (seconds)
            max_batch_size: Maximum requests per batch
            enable_adaptive_batching: Enable adaptive batching based on response times
            rate_limit_rpm: Rate limit in requests per minute
        """
        self.max_concurrent = max_concurrent
        self.batch_delay = batch_delay
        self.max_batch_size = max_batch_size
        self.enable_adaptive_batching = enable_adaptive_batching
        self.rate_limit_rpm = rate_limit_rpm
        
        # Request queue and processing
        self._request_queue: List[BatchRequest] = []
        self._results: Dict[str, BatchResult] = {}
        self._pending_requests: Dict[str, threading.Event] = {}
        self._queue_lock = threading.Lock()
        
        # Rate limiting
        self._request_timestamps: List[float] = []
        self._rate_limit_lock = threading.Lock()
        
        # Adaptive batching metrics
        self._response_times: List[float] = []
        self._batch_stats = {
            'processed_batches': 0,
            'total_requests': 0,
            'avg_response_time': 0.0,
            'cache_hits': 0
        }
        
        # Processing thread
        self._processing_thread = None
        self._stop_processing = threading.Event()
        
    def start_processing(self):
        """Start the batch processing thread."""
        if self._processing_thread is None or not self._processing_thread.is_alive():
            self._stop_processing.clear()
            self._processing_thread = threading.Thread(target=self._process_batches)
            self._processing_thread.daemon = True
            self._processing_thread.start()
            logger.info("Batch processor started")

    def stop_processing(self):
        """Stop the batch processing thread."""
        self._stop_processing.set()
        if self._processing_thread:
            self._processing_thread.join(timeout=5.0)
        logger.info("Batch processor stopped")

    def submit_request(
        self,
        request_id: str,
        stage: str,
        prompt: str,
        model_config: Dict[str, Any],
        system_prompt: Optional[str] = None,
        text_paths: Optional[List[Path]] = None,
        pdf_path: Optional[Path] = None,
        pdf_paths: Optional[List[Path]] = None,
        priority: int = 1
    ) -> BatchResult:
        """Submit a request for batch processing.
        
        Returns:
            BatchResult: The result of the API call (blocks until complete)
        """
        # Estimate token count for prioritization
        estimated_tokens = self._estimate_tokens(prompt, system_prompt)
        
        request = BatchRequest(
            id=request_id,
            stage=stage,
            prompt=prompt,
            model_config=model_config,
            system_prompt=system_prompt,
            text_paths=text_paths,
            pdf_path=pdf_path,
            pdf_paths=pdf_paths,
            priority=priority,
            estimated_tokens=estimated_tokens
        )
        
        # Create event for waiting
        result_event = threading.Event()
        
        with self._queue_lock:
            self._request_queue.append(request)
            self._pending_requests[request_id] = result_event
            
        # Start processing if not already running
        self.start_processing()
        
        # Wait for result
        result_event.wait()
        
        # Retrieve and cleanup result
        with self._queue_lock:
            result = self._results.get(request_id)
            if request_id in self._results:
                del self._results[request_id]
            if request_id in self._pending_requests:
                del self._pending_requests[request_id]
                
        return result

    def submit_batch(
        self,
        requests: List[Dict[str, Any]]
    ) -> List[BatchResult]:
        """Submit multiple requests as a batch.
        
        Args:
            requests: List of request dictionaries with required fields
            
        Returns:
            List of BatchResult objects
        """
        batch_requests = []
        result_events = {}
        
        for i, req_data in enumerate(requests):
            request_id = req_data.get('id', f"batch_{int(time.time())}_{i}")
            
            request = BatchRequest(
                id=request_id,
                stage=req_data['stage'],
                prompt=req_data['prompt'],
                model_config=req_data['model_config'],
                system_prompt=req_data.get('system_prompt'),
                text_paths=req_data.get('text_paths'),
                pdf_path=req_data.get('pdf_path'),
                pdf_paths=req_data.get('pdf_paths'),
                priority=req_data.get('priority', 1),
                estimated_tokens=self._estimate_tokens(
                    req_data['prompt'], 
                    req_data.get('system_prompt')
                )
            )
            
            batch_requests.append(request)
            result_events[request_id] = threading.Event()
            
        # Add to queue
        with self._queue_lock:
            self._request_queue.extend(batch_requests)
            self._pending_requests.update(result_events)
            
        # Start processing if not already running
        self.start_processing()
        
        # Wait for all results
        for event in result_events.values():
            event.wait()
            
        # Collect results
        results = []
        with self._queue_lock:
            for request in batch_requests:
                result = self._results.get(request.id)
                if result:
                    results.append(result)
                    del self._results[request.id]
                if request.id in self._pending_requests:
                    del self._pending_requests[request.id]
                    
        return results

    def _process_batches(self):
        """Main batch processing loop."""
        while not self._stop_processing.is_set():
            try:
                # Wait for requests or batch delay
                time.sleep(min(self.batch_delay, 1.0))
                
                if not self._request_queue:
                    continue
                    
                # Create batch
                with self._queue_lock:
                    if not self._request_queue:
                        continue
                        
                    # Sort by priority and estimated processing time
                    self._request_queue.sort(
                        key=lambda x: (-x.priority, x.estimated_tokens or 0)
                    )
                    
                    # Take batch
                    batch_size = min(self.max_batch_size, len(self._request_queue))
                    current_batch = self._request_queue[:batch_size]
                    self._request_queue = self._request_queue[batch_size:]
                    
                if current_batch:
                    self._process_batch(current_batch)
                    
            except Exception as e:
                logger.error(f"Error in batch processing loop: {e}")
                time.sleep(1.0)

    def _process_batch(self, batch: List[BatchRequest]):
        """Process a batch of requests."""
        logger.info(f"Processing batch of {len(batch)} requests")
        
        batch_start_time = time.time()
        
        # Group by model and similar characteristics for better batching
        model_groups = {}
        for request in batch:
            model = request.model_config.get('model', 'unknown')
            if model not in model_groups:
                model_groups[model] = []
            model_groups[model].append(request)
        
        # Process each model group concurrently
        with ThreadPoolExecutor(max_workers=self.max_concurrent) as executor:
            future_to_request = {}
            
            for model, requests in model_groups.items():
                for request in requests:
                    # Check rate limiting
                    if not self._check_rate_limit():
                        time.sleep(self._calculate_rate_limit_delay())
                    
                    future = executor.submit(self._process_single_request, request)
                    future_to_request[future] = request
            
            # Collect results
            for future in as_completed(future_to_request):
                request = future_to_request[future]
                try:
                    result = future.result()
                    
                    # Store result and notify waiting thread
                    with self._queue_lock:
                        self._results[request.id] = result
                        if request.id in self._pending_requests:
                            self._pending_requests[request.id].set()
                            
                except Exception as e:
                    logger.error(f"Error processing request {request.id}: {e}")
                    
                    # Store error result
                    error_result = BatchResult(
                        request_id=request.id,
                        response="",
                        duration=0.0,
                        success=False,
                        error=str(e)
                    )
                    
                    with self._queue_lock:
                        self._results[request.id] = error_result
                        if request.id in self._pending_requests:
                            self._pending_requests[request.id].set()
        
        # Update statistics
        batch_duration = time.time() - batch_start_time
        self._update_batch_stats(len(batch), batch_duration)

    def _process_single_request(self, request: BatchRequest) -> BatchResult:
        """Process a single request."""
        from src.utils.api import APIHandler  # Import here to avoid circular imports
        
        start_time = time.time()
        
        try:
            # Create API handler (could be injected as dependency)
            api_handler = APIHandler()
            
            # Make API call
            response, api_duration = api_handler.make_api_call(
                stage=request.stage,
                prompt=request.prompt,
                text_paths=request.text_paths,
                pdf_path=request.pdf_path,
                pdf_paths=request.pdf_paths,
                system_prompt=request.system_prompt
            )
            
            duration = time.time() - start_time
            
            # Record response time for adaptive batching
            self._response_times.append(api_duration)
            if len(self._response_times) > 100:  # Keep recent history
                self._response_times = self._response_times[-100:]
            
            return BatchResult(
                request_id=request.id,
                response=response,
                duration=duration,
                success=True
            )
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Request {request.id} failed: {e}")
            
            return BatchResult(
                request_id=request.id,
                response="",
                duration=duration,
                success=False,
                error=str(e)
            )

    def _estimate_tokens(self, prompt: str, system_prompt: Optional[str] = None) -> int:
        """Estimate token count for a request."""
        # Simple estimation: ~4 characters per token
        text_length = len(prompt)
        if system_prompt:
            text_length += len(system_prompt)
        return text_length // 4

    def _check_rate_limit(self) -> bool:
        """Check if we're within rate limits."""
        with self._rate_limit_lock:
            current_time = time.time()
            # Remove requests older than 1 minute
            self._request_timestamps = [
                ts for ts in self._request_timestamps
                if current_time - ts < 60
            ]
            
            return len(self._request_timestamps) < self.rate_limit_rpm

    def _calculate_rate_limit_delay(self) -> float:
        """Calculate delay needed to respect rate limits."""
        with self._rate_limit_lock:
            if not self._request_timestamps:
                return 0.0
                
            current_time = time.time()
            oldest_request = min(self._request_timestamps)
            
            # Calculate delay to stay within rate limit
            delay = max(0, 60 - (current_time - oldest_request))
            return delay / len(self._request_timestamps)

    def _record_request(self):
        """Record a request timestamp for rate limiting."""
        with self._rate_limit_lock:
            self._request_timestamps.append(time.time())

    def _update_batch_stats(self, batch_size: int, batch_duration: float):
        """Update batch processing statistics."""
        self._batch_stats['processed_batches'] += 1
        self._batch_stats['total_requests'] += batch_size
        
        # Update average response time
        if self._response_times:
            self._batch_stats['avg_response_time'] = sum(self._response_times) / len(self._response_times)

    def get_stats(self) -> Dict[str, Any]:
        """Get batch processing statistics."""
        queue_size = len(self._request_queue)
        pending_results = len(self._pending_requests)
        
        return {
            **self._batch_stats,
            'queue_size': queue_size,
            'pending_results': pending_results,
            'avg_batch_size': (
                self._batch_stats['total_requests'] / self._batch_stats['processed_batches']
                if self._batch_stats['processed_batches'] > 0 else 0
            )
        }

    def clear_queue(self):
        """Clear the request queue."""
        with self._queue_lock:
            self._request_queue.clear()
            logger.info("Batch queue cleared")

    def __enter__(self):
        """Context manager entry."""
        self.start_processing()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop_processing()