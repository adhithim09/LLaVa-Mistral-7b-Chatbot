import hashlib
from functools import lru_cache
from datetime import datetime, timedelta

class ImageProcessingCache:
    """Cache for processed images to avoid re-encoding identical images"""

    def __init__(self, max_cache_size=100, cache_ttl_hours=24):
        self.cache = {}
        self.max_cache_size = max_cache_size
        self.cache_ttl = timedelta(hours=cache_ttl_hours)

    def get_image_hash(self, image_bytes):
        """Generate SHA256 hash of image bytes for cache key"""
        return hashlib.sha256(image_bytes).hexdigest()

    def get(self, image_bytes, max_dim=800):
        """Get cached image processing result"""
        image_hash = self.get_image_hash(image_bytes)

        # Check if cached entry exists and is still valid
        if image_hash in self.cache:
            cached_entry = self.cache[image_hash]

            # Check TTL
            if datetime.now() - cached_entry['timestamp'] < self.cache_ttl:
                cached_entry['hits'] += 1
                return cached_entry['result']
            else:
                # Expired entry
                del self.cache[image_hash]

        return None

    def set(self, image_bytes, result, max_dim=800):
        """Cache image processing result"""
        image_hash = self.get_image_hash(image_bytes)

        # Evict oldest entry if cache is full
        if len(self.cache) >= self.max_cache_size:
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k]['timestamp'])
            del self.cache[oldest_key]

        self.cache[image_hash] = {
            'result': result,
            'timestamp': datetime.now(),
            'hits': 0,
        }

    def clear(self):
        """Clear entire cache"""
        self.cache.clear()

    def get_stats(self):
        """Get cache statistics"""
        total_hits = sum(entry['hits'] for entry in self.cache.values())
        return {
            'size': len(self.cache),
            'max_size': self.max_cache_size,
            'total_hits': total_hits,
            'entries': list(self.cache.keys())[:10],
        }


# Global cache instance
image_cache = ImageProcessingCache(max_cache_size=100, cache_ttl_hours=24)
