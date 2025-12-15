"""Rate limiter service using fixed window counter algorithm."""

import logging
from typing import Tuple, Optional
from infrastructure.rate_limiting.redis_client import get_redis_client

logger = logging.getLogger(__name__)


def check_rate_limit(
    key: str,
    limit: int,
    window_seconds: int
) -> Tuple[bool, int, int]:
    """
    Check if request is within rate limit using fixed window counter.
    
    Args:
        key: Rate limit key (e.g., "user:123" or "ip:192.168.1.1")
        limit: Maximum number of requests allowed in the window
        window_seconds: Window duration in seconds
    
    Returns:
        Tuple of (allowed: bool, retry_after: int, remaining: int)
        - allowed: True if request is allowed, False if limit exceeded
        - retry_after: Seconds until limit resets (0 if allowed)
        - remaining: Remaining requests in current window (0 if limit exceeded)
    """
    redis_client = get_redis_client()
    
    # If Redis is unavailable, allow request (graceful degradation)
    if redis_client is None:
        logger.debug("Redis unavailable, allowing request (rate limiting disabled)")
        return True, 0, limit
    
    try:
        # Calculate window timestamp (current time divided by window duration)
        import time
        current_time = int(time.time())
        window_timestamp = current_time // window_seconds
        
        # Generate Redis key
        redis_key = f"rate_limit:{key}:{window_timestamp}"
        
        # Increment counter and get current count
        current_count = redis_client.incr(redis_key)
        
        # Set TTL if this is the first request in the window
        if current_count == 1:
            redis_client.expire(redis_key, window_seconds)
        
        # Check if limit exceeded
        if current_count > limit:
            # Calculate retry_after (seconds until next window)
            next_window_timestamp = window_timestamp + 1
            next_window_time = next_window_timestamp * window_seconds
            retry_after = next_window_time - current_time
            
            logger.debug(f"Rate limit exceeded for key {key}: {current_count}/{limit}")
            return False, retry_after, 0
        
        # Within limit
        remaining = max(0, limit - current_count)
        logger.debug(f"Rate limit check for key {key}: {current_count}/{limit}, remaining: {remaining}")
        return True, 0, remaining
        
    except Exception as e:
        # On error, allow request (graceful degradation)
        logger.error(f"Error checking rate limit for key {key}: {e}", exc_info=True)
        return True, 0, limit
