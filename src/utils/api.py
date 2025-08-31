# src/utils/api.py
from typing import Dict, Any, Optional, Callable, List
import os
import logging
import base64
from pathlib import Path
import openai
import anthropic
import yaml
from dotenv import load_dotenv
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    wait_random,
    retry_if_exception_type,
    RetryCallState,
)
import time

# Import performance optimization modules
try:
    from src.performance.api_cache import APICache
    from src.performance.memory_manager import MemoryManager
    from src.performance.batch_processor import BatchProcessor
    PERFORMANCE_AVAILABLE = True
except ImportError:
    APICache = None
    MemoryManager = None
    BatchProcessor = None
    PERFORMANCE_AVAILABLE = False


def create_retry_decorator(
    max_attempts: int = 5, min_wait: int = 4, max_wait: int = 60
) -> Callable:
    """Create a retry decorator with custom settings"""

    def before_sleep_handler(retry_state: RetryCallState):
        """Handle logging before sleep"""
        exception = retry_state.outcome.exception()
        if isinstance(exception, anthropic.RateLimitError):
            print(
                f"\nRate limit hit, waiting {retry_state.next_action.sleep} seconds..."
            )
        else:
            print(f"\nAPI error: {str(exception)}")
            print(f"Retrying in {retry_state.next_action.sleep} seconds...")

    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=2, min=min_wait, max=max_wait)
        + wait_random(0, 2),  # Add jitter
        retry=retry_if_exception_type(
            (
                anthropic.RateLimitError,  # Handle rate limits
                anthropic.APIError,  # Handle API errors
                anthropic.APIConnectionError,  # Handle connection issues
                Exception,  # Handle unexpected errors
            )
        ),
        before_sleep=before_sleep_handler,
    )


def load_config() -> Dict[str, Any]:
    """Load configuration from yaml file (legacy function)"""
    try:
        # Try new configuration system first
        from src.config import ConfigManager
        config_manager = ConfigManager()
        return config_manager.load_config()
    except ImportError:
        # Fall back to legacy configuration loading
        with open("config/conceptual_config.yaml", "r") as f:
            return yaml.safe_load(f)


class APIHandler:
    def __init__(self, config: Dict[str, Any] = None, config_manager=None, 
                 enable_caching: bool = True, enable_batching: bool = False,
                 enable_memory_management: bool = True):
        load_dotenv()
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")

        if not self.openai_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        if not self.anthropic_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

        self.openai_client = openai.OpenAI(api_key=self.openai_key)
        # In APIHandler.__init__
        self.anthropic_client = anthropic.Client(
            api_key=self.anthropic_key,
            # We no longer need the beta header for PDFs
        )
        
        # Configuration management with backward compatibility
        self.config_manager = config_manager
        if config is None:
            self.config = self.load_config()  # Load default if none provided
        else:
            self.config = config
        self.o1_calls = 0

        self.logger = logging.getLogger(__name__)

        self._retry_with_rate_limit = create_retry_decorator(
            max_attempts=5, min_wait=4, max_wait=60
        )

        self._retry_standard = create_retry_decorator(
            max_attempts=3, min_wait=2, max_wait=30
        )
        
        # Initialize performance optimization components
        self._init_performance_components(
            enable_caching, enable_batching, enable_memory_management
        )
        
    def _init_performance_components(self, enable_caching: bool, 
                                   enable_batching: bool, enable_memory_management: bool):
        """Initialize performance optimization components."""
        if not PERFORMANCE_AVAILABLE:
            self.logger.warning("Performance optimization modules not available")
            self.cache = None
            self.memory_manager = None
            self.batch_processor = None
            return
            
        # API Cache
        if enable_caching and APICache:
            try:
                self.cache = APICache(
                    default_ttl=3600,  # 1 hour cache
                    max_cache_size_mb=50,
                    enable_compression=True
                )
                self.logger.info("API caching enabled")
            except Exception as e:
                self.logger.warning(f"Could not initialize API cache: {e}")
                self.cache = None
        else:
            self.cache = None
            
        # Memory Manager
        if enable_memory_management and MemoryManager:
            try:
                self.memory_manager = MemoryManager(
                    memory_threshold_percent=80.0,
                    gc_threshold_mb=100.0,
                    enable_monitoring=True
                )
                self.logger.info("Memory management enabled")
            except Exception as e:
                self.logger.warning(f"Could not initialize memory manager: {e}")
                self.memory_manager = None
        else:
            self.memory_manager = None
            
        # Batch Processor (optional, not enabled by default)
        if enable_batching and BatchProcessor:
            try:
                self.batch_processor = BatchProcessor(
                    max_concurrent=3,
                    batch_delay=1.0,
                    rate_limit_rpm=50
                )
                self.logger.info("Batch processing enabled")
            except Exception as e:
                self.logger.warning(f"Could not initialize batch processor: {e}")
                self.batch_processor = None
        else:
            self.batch_processor = None

    # To make loading the config easier in the run_phase_one script.
    # Check there are no problems when loading a different config for tests.
    def load_config(self) -> Dict[str, Any]:
        """Load configuration with new system support and legacy fallback"""
        if self.config_manager:
            return self.config_manager.load_config()
        
        try:
            # Try new configuration system first
            from src.config import ConfigManager
            config_manager = ConfigManager()
            self.config_manager = config_manager  # Cache for future use
            return config_manager.load_config()
        except (ImportError, Exception):
            # Fall back to legacy configuration loading
            with open("config/conceptual_config.yaml", "r") as f:
                return yaml.safe_load(f)

    def _encode_pdf(self, pdf_path: Path) -> str:
        """Convert PDF to base64 encoding"""
        with open(pdf_path, "rb") as file:
            return base64.b64encode(file.read()).decode("utf-8")

    def _call_anthropic_with_pdf(
        self, prompt: str, pdf_path: Path, config: Dict[str, Any], system_prompt: Optional[str] = None
    ) -> str:
        """Make Anthropic API call with PDF support"""

        @self._retry_with_rate_limit
        def make_call():
            try:
                # Encode PDF
                pdf_data = self._encode_pdf(pdf_path)

                # Construct message content
                content = [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": pdf_data,
                        },
                    },
                    {"type": "text", "text": prompt},
                ]

                # Make API call with optional system prompt
                kwargs = {
                    "model": config["model"],
                    "max_tokens": config["max_tokens"],
                    "messages": [{"role": "user", "content": content}],
                }
                
                if system_prompt:
                    kwargs["system"] = system_prompt
                
                response = self.anthropic_client.messages.create(**kwargs)
                return response.content[0].text

            except Exception as e:
                print(f"Anthropic API call with PDF failed: {e}")
                raise

        return make_call()

    def _call_anthropic_with_pdfs(
        self, prompt: str, pdf_paths: list[Path], config: Dict[str, Any], system_prompt: Optional[str] = None
    ) -> str:
        """Make Anthropic API call with multiple PDF support"""

        @self._retry_with_rate_limit
        def make_call():
            try:
                # Construct message content with multiple PDFs
                content = []
                
                # Add each PDF as a document
                for pdf_path in pdf_paths:
                    pdf_data = self._encode_pdf(pdf_path)
                    content.append({
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": pdf_data,
                        },
                    })
                
                # Add the text prompt last
                content.append({"type": "text", "text": prompt})

                # Make API call with optional system prompt
                kwargs = {
                    "model": config["model"],
                    "max_tokens": config["max_tokens"],
                    "messages": [{"role": "user", "content": content}],
                }
                
                if system_prompt:
                    kwargs["system"] = system_prompt
                
                response = self.anthropic_client.messages.create(**kwargs)
                return response.content[0].text

            except Exception as e:
                print(f"Anthropic API call with PDFs failed: {e}")
                raise

        return make_call()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception, openai.APIError)),
    )
    def _call_openai(self, prompt: str, config: Dict[str, Any], system_prompt: Optional[str] = None) -> str:
        """Make OpenAI API call with retries"""
        try:
            print(f"\nMaking API call to {config['model']}")

            # Track o1 usage
            if "o1" in config["model"]:
                self.o1_calls += 1
                print(f"o1 calls this session: {self.o1_calls}")

            # For o1 models
            if "o1" in config["model"]:
                messages = [{"role": "user", "content": prompt}]
                response = self.openai_client.chat.completions.create(
                    model=config["model"],
                    messages=messages,
                    temperature=1,  # TODO: This should probably not that high
                )
                content = response.choices[0].message.content
                if not content.strip():  # If empty response
                    print("Received empty response, retrying...")
                    raise Exception("Empty response from API")
                return content

            # For other OpenAI models
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            else:
                messages.append({"role": "system", "content": "You are a helpful assistant."})
            messages.append({"role": "user", "content": prompt})
            
            response = self.openai_client.chat.completions.create(
                model=config["model"],
                messages=messages,
                max_tokens=config["max_tokens"],
                temperature=config["temperature"],
            )
            return response.choices[0].message.content

        except Exception as e:
            print(f"\nAPI call failed: {str(e)}")
            print(f"Model: {config['model']}")
            print(f"Config: {config}")
            raise

    def _call_anthropic(self, prompt: str, config: Dict[str, Any], system_prompt: Optional[str] = None) -> str:
        """Make standard Anthropic API call"""

        @self._retry_standard  # Use standard retry for normal calls
        def make_call():
            """Make Anthropic API call without PDF"""
            try:
                print(f"\nMaking API call to {config['model']}")

                # Add a delay between retries to avoid rate limits
                time.sleep(1)

                # Try with a smaller max_tokens if we're getting errors
                max_tokens = config["max_tokens"]

                # Try with a smaller prompt if needed
                current_prompt = prompt

                # Build kwargs with optional system prompt
                kwargs = {
                    "model": config["model"],
                    "max_tokens": max_tokens,
                    "messages": [{"role": "user", "content": current_prompt}],
                }
                
                if system_prompt:
                    kwargs["system"] = system_prompt

                response = self.anthropic_client.messages.create(**kwargs)
                return response.content[0].text
            except anthropic.InternalServerError as e:
                print(f"Anthropic Internal Server Error: {e}")
                print("This is likely a temporary issue with the Anthropic API.")
                print("Retrying with a shorter prompt and fewer tokens...")

                # Try with a much smaller prompt and fewer tokens
                shortened_prompt = prompt[:20000] if len(prompt) > 20000 else prompt
                try:
                    kwargs_shortened = {
                        "model": config["model"],
                        "max_tokens": min(config["max_tokens"], 4000),
                        "messages": [{"role": "user", "content": shortened_prompt}],
                    }
                    
                    if system_prompt:
                        kwargs_shortened["system"] = system_prompt
                        
                    response = self.anthropic_client.messages.create(**kwargs_shortened)
                    return response.content[0].text
                except Exception as inner_e:
                    print(f"Still failed with shortened prompt: {inner_e}")
                    raise
            except Exception as e:
                print(f"Anthropic API call failed: {e}")
                raise

        return make_call()

    def _call_anthropic_with_texts(
        self, prompt: str, text_paths: list[Path], config: Dict[str, Any], system_prompt: Optional[str] = None
    ) -> str:
        """Make Anthropic API call with multiple text file support"""
        
        full_prompt = ""
        for i, text_path in enumerate(text_paths):
            with open(text_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
            full_prompt += f"<analysis_paper_example_{i+1}>\n{text_content}\n</analysis_paper_example_{i+1}>\n\n"

        full_prompt += prompt

        # This now becomes a standard call, since the text is in the prompt
        return self._call_anthropic(full_prompt, config, system_prompt)

    def make_api_call(
        self, stage: str, prompt: str, text_paths: Optional[list[Path]] = None, pdf_path: Optional[Path] = None, pdf_paths: Optional[list[Path]] = None, system_prompt: Optional[str] = None
    ) -> tuple[str, float]:
        """Make API call to appropriate provider based on stage and return duration."""
        start_time = time.time()
        model_config = self.config["models"][stage]

        if model_config["provider"] == "openai":
            if text_paths or pdf_path or pdf_paths:
                print("Warning: OpenAI provider doesn't support text/PDF file inputs, ignoring file parameters")
            response_text = self._call_openai(prompt, model_config, system_prompt)
        elif model_config["provider"] == "anthropic":
            if pdf_path:
                response_text = self._call_anthropic_with_pdf(prompt, pdf_path, model_config, system_prompt)
            elif pdf_paths:
                response_text = self._call_anthropic_with_pdfs(prompt, pdf_paths, model_config, system_prompt)
            elif text_paths:
                response_text = self._call_anthropic_with_texts(prompt, text_paths, model_config, system_prompt)
            else:
                response_text = self._call_anthropic(prompt, model_config, system_prompt)
        else:
            raise ValueError(f"Unknown provider: {model_config['provider']}")
        
        duration = time.time() - start_time
        self.logger.info(f"API call for stage '{stage}' took {duration:.2f} seconds.")
        return response_text, duration

    def make_api_call_cached(
        self, stage: str, prompt: str, text_paths: Optional[List[Path]] = None, 
        pdf_path: Optional[Path] = None, pdf_paths: Optional[List[Path]] = None, 
        system_prompt: Optional[str] = None, force_refresh: bool = False
    ) -> tuple[str, float]:
        """Make API call with caching support."""
        
        if not self.cache or force_refresh:
            return self.make_api_call(stage, prompt, text_paths, pdf_path, pdf_paths, system_prompt)
        
        model_config = self.config["models"][stage]
        
        # Collect file paths for cache key generation
        file_paths = []
        if text_paths:
            file_paths.extend(text_paths)
        if pdf_path:
            file_paths.append(pdf_path)
        if pdf_paths:
            file_paths.extend(pdf_paths)
        
        # Try cache first
        cached_response = self.cache.get(
            prompt=prompt,
            model_config=model_config,
            system_prompt=system_prompt,
            file_paths=file_paths if file_paths else None
        )
        
        if cached_response:
            self.logger.info(f"Cache hit for stage '{stage}'")
            return cached_response, 0.0  # No API call time for cached response
        
        # Cache miss - make API call
        response_text, duration = self.make_api_call(
            stage, prompt, text_paths, pdf_path, pdf_paths, system_prompt
        )
        
        # Cache the response
        self.cache.put(
            prompt=prompt,
            model_config=model_config,
            response=response_text,
            system_prompt=system_prompt,
            file_paths=file_paths if file_paths else None
        )
        
        return response_text, duration

    def make_batch_api_calls(self, requests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Make multiple API calls using batch processing."""
        
        if not self.batch_processor:
            # Fall back to sequential processing
            results = []
            for req in requests:
                try:
                    response, duration = self.make_api_call_cached(**req)
                    results.append({
                        'id': req.get('id', f"req_{len(results)}"),
                        'response': response,
                        'duration': duration,
                        'success': True
                    })
                except Exception as e:
                    results.append({
                        'id': req.get('id', f"req_{len(results)}"),
                        'response': '',
                        'duration': 0.0,
                        'success': False,
                        'error': str(e)
                    })
            return results
        
        # Use batch processor
        batch_results = self.batch_processor.submit_batch(requests)
        
        # Convert to expected format
        results = []
        for batch_result in batch_results:
            results.append({
                'id': batch_result.request_id,
                'response': batch_result.response,
                'duration': batch_result.duration,
                'success': batch_result.success,
                'error': batch_result.error,
                'cached': batch_result.cached
            })
        
        return results

    def process_large_pdf_optimized(
        self, stage: str, prompt: str, pdf_path: Path, system_prompt: Optional[str] = None
    ) -> tuple[str, float]:
        """Process large PDF with memory optimization."""
        
        if not self.memory_manager:
            return self.make_api_call_cached(stage, prompt, pdf_path=pdf_path, system_prompt=system_prompt)
        
        # Use memory manager for large PDF processing
        with self.memory_manager.process_pdf_memory_optimized(pdf_path):
            return self.make_api_call_cached(stage, prompt, pdf_path=pdf_path, system_prompt=system_prompt)

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics from all optimization components."""
        stats = {
            'api_calls_made': getattr(self, 'api_calls_made', 0),
            'performance_components': {
                'cache_available': self.cache is not None,
                'memory_manager_available': self.memory_manager is not None,
                'batch_processor_available': self.batch_processor is not None
            }
        }
        
        if self.cache:
            stats['cache_stats'] = self.cache.get_stats()
            
        if self.memory_manager:
            stats['memory_stats'] = self.memory_manager.get_stats()
            
        if self.batch_processor:
            stats['batch_stats'] = self.batch_processor.get_stats()
            
        return stats

    def optimize_performance(self):
        """Perform performance optimization operations."""
        if self.cache:
            # Save cache to disk
            self.cache.save_cache()
            
        if self.memory_manager:
            # Optimize memory usage
            self.memory_manager.optimize_memory()
            
        self.logger.info("Performance optimization completed")

    def clear_cache(self):
        """Clear API response cache."""
        if self.cache:
            self.cache.clear_cache()
            self.logger.info("API cache cleared")
        else:
            self.logger.warning("No cache available to clear")

    def invalidate_model_cache(self, model: str) -> int:
        """Invalidate cache entries for a specific model."""
        if self.cache:
            return self.cache.invalidate_model_cache(model)
        return 0

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup and optimization."""
        try:
            self.optimize_performance()
            
            if self.memory_manager:
                self.memory_manager.stop_monitoring()
                
            if self.batch_processor:
                self.batch_processor.stop_processing()
                
        except Exception as e:
            self.logger.error(f"Error during APIHandler cleanup: {e}")
