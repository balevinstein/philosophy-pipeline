"""API response caching with intelligent invalidation."""

import hashlib
import json
import logging
import os
import pickle
import time
from pathlib import Path
from typing import Any, Dict, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


@dataclass
class CacheEntry:
    """Represents a cached API response."""
    response: str
    timestamp: float
    model_config: Dict[str, Any]
    content_hash: str
    ttl_seconds: int
    hit_count: int = 0
    last_accessed: float = None

    def __post_init__(self):
        if self.last_accessed is None:
            self.last_accessed = self.timestamp

    def is_expired(self) -> bool:
        """Check if cache entry has expired."""
        return time.time() - self.timestamp > self.ttl_seconds

    def is_valid_for_config(self, model_config: Dict[str, Any]) -> bool:
        """Check if cache entry is valid for given model configuration."""
        # Key parameters that affect response
        key_params = ['model', 'temperature', 'max_tokens']
        for param in key_params:
            if self.model_config.get(param) != model_config.get(param):
                return False
        return True


class APICache:
    """Intelligent API response caching system."""

    def __init__(
        self, 
        cache_dir: Optional[Path] = None,
        default_ttl: int = 3600,  # 1 hour default TTL
        max_cache_size_mb: int = 100,
        enable_compression: bool = True
    ):
        """Initialize API cache.
        
        Args:
            cache_dir: Directory to store cache files
            default_ttl: Default time-to-live in seconds
            max_cache_size_mb: Maximum cache size in MB
            enable_compression: Enable response compression
        """
        self.cache_dir = cache_dir or Path.home() / ".philosophy_pipeline" / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.default_ttl = default_ttl
        self.max_cache_size_mb = max_cache_size_mb
        self.enable_compression = enable_compression
        
        self._cache: Dict[str, CacheEntry] = {}
        self._load_cache()
        
        # Statistics
        self.stats = {
            'hits': 0,
            'misses': 0,
            'invalidations': 0,
            'cache_size_bytes': 0
        }

    def _generate_cache_key(self, prompt: str, model_config: Dict[str, Any], 
                           system_prompt: Optional[str] = None,
                           file_hashes: Optional[Dict[str, str]] = None) -> str:
        """Generate a unique cache key for the request."""
        # Create content hash from prompt and system prompt
        content = prompt
        if system_prompt:
            content += f"\n---SYSTEM---\n{system_prompt}"
            
        # Include file hashes if provided
        if file_hashes:
            content += f"\n---FILES---\n{json.dumps(file_hashes, sort_keys=True)}"
        
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        
        # Include key model parameters in hash
        model_params = {
            'model': model_config.get('model'),
            'temperature': model_config.get('temperature'),
            'max_tokens': model_config.get('max_tokens')
        }
        model_hash = hashlib.md5(json.dumps(model_params, sort_keys=True).encode()).hexdigest()
        
        return f"{model_hash}_{content_hash[:16]}"

    def _calculate_file_hashes(self, file_paths: Optional[list[Path]]) -> Optional[Dict[str, str]]:
        """Calculate hashes for input files to detect changes."""
        if not file_paths:
            return None
            
        file_hashes = {}
        for file_path in file_paths:
            if file_path and file_path.exists():
                try:
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()
                    file_hashes[str(file_path)] = file_hash
                except Exception as e:
                    logger.warning(f"Could not hash file {file_path}: {e}")
        
        return file_hashes if file_hashes else None

    def get(self, prompt: str, model_config: Dict[str, Any], 
            system_prompt: Optional[str] = None,
            file_paths: Optional[list[Path]] = None) -> Optional[str]:
        """Retrieve cached response if available and valid."""
        
        # Calculate file hashes to detect file changes
        file_hashes = self._calculate_file_hashes(file_paths)
        cache_key = self._generate_cache_key(prompt, model_config, system_prompt, file_hashes)
        
        entry = self._cache.get(cache_key)
        if entry is None:
            self.stats['misses'] += 1
            return None
            
        # Check expiration
        if entry.is_expired():
            self._invalidate(cache_key)
            self.stats['misses'] += 1
            return None
            
        # Check model config compatibility
        if not entry.is_valid_for_config(model_config):
            self._invalidate(cache_key)
            self.stats['misses'] += 1
            return None
            
        # Update access statistics
        entry.hit_count += 1
        entry.last_accessed = time.time()
        self.stats['hits'] += 1
        
        logger.info(f"Cache hit for key {cache_key[:8]}... (hit #{entry.hit_count})")
        return entry.response

    def put(self, prompt: str, model_config: Dict[str, Any], response: str,
            system_prompt: Optional[str] = None,
            file_paths: Optional[list[Path]] = None,
            ttl: Optional[int] = None) -> None:
        """Store response in cache."""
        
        # Calculate file hashes
        file_hashes = self._calculate_file_hashes(file_paths)
        cache_key = self._generate_cache_key(prompt, model_config, system_prompt, file_hashes)
        
        # Create content hash for deduplication
        content_hash = hashlib.md5(response.encode()).hexdigest()
        
        entry = CacheEntry(
            response=response,
            timestamp=time.time(),
            model_config=model_config.copy(),
            content_hash=content_hash,
            ttl_seconds=ttl or self.default_ttl
        )
        
        self._cache[cache_key] = entry
        logger.info(f"Cached response for key {cache_key[:8]}...")
        
        # Periodic cache maintenance
        if len(self._cache) % 100 == 0:
            self._cleanup_expired()
            self._enforce_size_limit()

    def _invalidate(self, cache_key: str) -> None:
        """Remove entry from cache."""
        if cache_key in self._cache:
            del self._cache[cache_key]
            self.stats['invalidations'] += 1

    def _cleanup_expired(self) -> None:
        """Remove expired entries."""
        current_time = time.time()
        expired_keys = [
            key for key, entry in self._cache.items()
            if current_time - entry.timestamp > entry.ttl_seconds
        ]
        
        for key in expired_keys:
            del self._cache[key]
            self.stats['invalidations'] += 1
            
        if expired_keys:
            logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")

    def _enforce_size_limit(self) -> None:
        """Enforce cache size limit using LRU eviction."""
        cache_size = self._estimate_cache_size()
        if cache_size > self.max_cache_size_mb * 1024 * 1024:  # Convert MB to bytes
            
            # Sort by last accessed time (LRU)
            sorted_entries = sorted(
                self._cache.items(),
                key=lambda x: x[1].last_accessed
            )
            
            # Remove oldest entries until under limit
            removed = 0
            for key, _ in sorted_entries:
                if self._estimate_cache_size() <= self.max_cache_size_mb * 1024 * 1024:
                    break
                del self._cache[key]
                removed += 1
                
            if removed > 0:
                logger.info(f"Evicted {removed} cache entries to enforce size limit")

    def _estimate_cache_size(self) -> int:
        """Estimate total cache size in bytes."""
        total_size = 0
        for entry in self._cache.values():
            # Rough estimation: response text + metadata
            total_size += len(entry.response.encode()) + 1000  # 1KB for metadata
        return total_size

    def _load_cache(self) -> None:
        """Load cache from disk."""
        cache_file = self.cache_dir / "api_cache.pkl"
        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    self._cache = pickle.load(f)
                logger.info(f"Loaded {len(self._cache)} cache entries from disk")
                
                # Clean up expired entries on load
                self._cleanup_expired()
                
            except Exception as e:
                logger.warning(f"Could not load cache from disk: {e}")
                self._cache = {}

    def save_cache(self) -> None:
        """Save cache to disk."""
        cache_file = self.cache_dir / "api_cache.pkl"
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(self._cache, f)
            logger.info(f"Saved {len(self._cache)} cache entries to disk")
        except Exception as e:
            logger.error(f"Could not save cache to disk: {e}")

    def clear_cache(self) -> None:
        """Clear all cache entries."""
        self._cache.clear()
        cache_file = self.cache_dir / "api_cache.pkl"
        if cache_file.exists():
            cache_file.unlink()
        logger.info("Cache cleared")

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_requests = self.stats['hits'] + self.stats['misses']
        hit_rate = self.stats['hits'] / total_requests if total_requests > 0 else 0
        
        return {
            **self.stats,
            'hit_rate': hit_rate,
            'cache_entries': len(self._cache),
            'estimated_size_mb': self._estimate_cache_size() / (1024 * 1024)
        }

    def invalidate_model_cache(self, model: str) -> int:
        """Invalidate all cache entries for a specific model."""
        invalidated = 0
        keys_to_remove = []
        
        for key, entry in self._cache.items():
            if entry.model_config.get('model') == model:
                keys_to_remove.append(key)
                
        for key in keys_to_remove:
            del self._cache[key]
            invalidated += 1
            
        logger.info(f"Invalidated {invalidated} cache entries for model {model}")
        return invalidated

    def __del__(self):
        """Save cache when object is destroyed."""
        try:
            self.save_cache()
        except:
            pass  # Ignore errors during cleanup