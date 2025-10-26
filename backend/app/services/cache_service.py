from typing import Any, Optional, Dict
from datetime import datetime, timedelta
import hashlib
import json
import threading

class CacheService:
    """Simple in-memory cache service (for production use Redis)."""
    
    def __init__(self):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.lock = threading.Lock()
    
    def _generate_key(self, prefix: str, data: Dict[str, Any]) -> str:
        """Generate cache key from data."""
        data_str = json.dumps(data, sort_keys=True)
        hash_obj = hashlib.md5(data_str.encode())
        return f"{prefix}:{hash_obj.hexdigest()}"
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        with self.lock:
            if key in self.cache:
                entry = self.cache[key]
                if entry['expires_at'] > datetime.utcnow():
                    return entry['value']
                else:
                    # Remove expired entry
                    del self.cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl_seconds: int = 3600):
        """Set value in cache with TTL."""
        with self.lock:
            self.cache[key] = {
                'value': value,
                'expires_at': datetime.utcnow() + timedelta(seconds=ttl_seconds)
            }
    
    def delete(self, key: str):
        """Delete value from cache."""
        with self.lock:
            if key in self.cache:
                del self.cache[key]
    
    def clear(self):
        """Clear all cache."""
        with self.lock:
            self.cache.clear()
    
    def clean_expired(self):
        """Remove expired entries."""
        with self.lock:
            now = datetime.utcnow()
            expired_keys = [
                key for key, entry in self.cache.items()
                if entry['expires_at'] <= now
            ]
            for key in expired_keys:
                del self.cache[key]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self.lock:
            return {
                'total_entries': len(self.cache),
                'memory_usage_bytes': len(str(self.cache)),
            }

# Global cache instance
cache = CacheService()

# Cache decorators for specific use cases
def cache_form_generation(org_data: Dict[str, Any]) -> Optional[Any]:
    """Check cache for form generation."""
    key = cache._generate_key('form_gen', org_data)
    return cache.get(key)

def save_form_generation(org_data: Dict[str, Any], result: Any):
    """Save form generation result to cache."""
    key = cache._generate_key('form_gen', org_data)
    # Forms are relatively static, cache for 1 hour
    cache.set(key, result, ttl_seconds=3600)

def cache_step1_analysis(input_data: Dict[str, Any]) -> Optional[Any]:
    """Check cache for step1 analysis."""
    key = cache._generate_key('step1_analysis', input_data)
    return cache.get(key)

def save_step1_analysis(input_data: Dict[str, Any], result: Any):
    """Save step1 analysis result to cache."""
    key = cache._generate_key('step1_analysis', input_data)
    # Analysis results cache for 30 minutes
    cache.set(key, result, ttl_seconds=1800)
