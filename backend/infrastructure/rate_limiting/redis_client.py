"""Redis client for rate limiting."""

import os
import logging
from typing import Optional
import redis

logger = logging.getLogger(__name__)

# Global Redis client instance
_redis_client: Optional[redis.Redis] = None


def get_redis_client() -> Optional[redis.Redis]:
    """Get or create Redis client instance.
    
    Returns:
        Redis client instance, or None if Redis is unavailable or disabled.
    """
    global _redis_client
    
    # Check if rate limiting is enabled
    if os.getenv("RATE_LIMIT_ENABLED", "true").lower() != "true":
        logger.debug("Rate limiting is disabled via RATE_LIMIT_ENABLED")
        return None
    
    # Return existing client if available
    if _redis_client is not None:
        try:
            # Test connection
            _redis_client.ping()
            return _redis_client
        except (redis.ConnectionError, redis.TimeoutError):
            logger.warning("Redis connection lost, attempting to reconnect...")
            _redis_client = None
    
    # Create new client
    try:
        # Support REDIS_URL (e.g., redis://redis:6379/0) or individual env vars
        redis_url = os.getenv("REDIS_URL")
        if redis_url:
            # Parse redis:// URL format
            from urllib.parse import urlparse
            parsed = urlparse(redis_url)
            host = parsed.hostname or "localhost"
            port = parsed.port or 6379
            password = parsed.password or None
            db = int(parsed.path.lstrip('/')) if parsed.path else 0
        else:
            # Fallback to individual environment variables
            host = os.getenv("REDIS_HOST", "localhost")
            port = int(os.getenv("REDIS_PORT", "6379"))
            password = os.getenv("REDIS_PASSWORD") or None
            db = int(os.getenv("REDIS_DB", "0"))
        
        _redis_client = redis.Redis(
            host=host,
            port=port,
            password=password,
            db=db,
            decode_responses=True,  # Return strings instead of bytes
            socket_connect_timeout=2,  # Fast timeout for rate limiting
            socket_timeout=2
        )
        
        # Test connection
        _redis_client.ping()
        logger.info(f"Redis client connected to {host}:{port}")
        return _redis_client
        
    except (redis.ConnectionError, redis.TimeoutError, Exception) as e:
        logger.warning(f"Redis unavailable for rate limiting: {e}. Rate limiting disabled.")
        _redis_client = None
        return None


def close_redis_client():
    """Close Redis client connection."""
    global _redis_client
    if _redis_client is not None:
        try:
            _redis_client.close()
        except Exception:
            pass
        _redis_client = None
