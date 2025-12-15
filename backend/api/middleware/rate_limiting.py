"""Rate limiting middleware for FastAPI."""

import os
import logging
from typing import Optional
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from infrastructure.rate_limiting.rate_limiter import check_rate_limit
from domain.models.user import User

logger = logging.getLogger(__name__)

# Configuration
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))


def get_rate_limit_key(request: Request) -> Optional[str]:
    """
    Extract rate limit key from request.
    
    Priority:
    1. Authenticated user ID (if user is authenticated)
    2. Client IP address (if user is not authenticated)
    
    Args:
        request: FastAPI request object
    
    Returns:
        Rate limit key string, or None if key cannot be determined
    """
    # Try to get authenticated user ID from Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        try:
            from infrastructure.auth.config import auth_config
            from jose import jwt
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, auth_config.secret_key, algorithms=[auth_config.algorithm])
            user_id = payload.get("sub")
            if user_id:
                return f"user:{user_id}"
        except Exception:
            # Token invalid or expired, fall back to IP
            pass
    
    # Fallback to IP address
    # Get real client IP (handle proxies)
    client_ip = request.client.host if request.client else None
    
    # Check X-Forwarded-For header (if behind proxy)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # Take first IP from comma-separated list
        client_ip = forwarded_for.split(",")[0].strip()
    
    if client_ip:
        return f"ip:{client_ip}"
    
    # Cannot determine key
    logger.warning("Cannot determine rate limit key (no user ID or IP address)")
    return None


def should_skip_rate_limiting(request: Request) -> bool:
    """
    Check if rate limiting should be skipped for this request.
    
    Args:
        request: FastAPI request object
    
    Returns:
        True if rate limiting should be skipped, False otherwise
    """
    # Skip health check endpoint
    if request.url.path == "/health":
        return True
    
    # Skip rate limiting if disabled
    if os.getenv("RATE_LIMIT_ENABLED", "true").lower() != "true":
        return True
    
    return False


class RateLimitingMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware for FastAPI."""
    
    async def dispatch(self, request: Request, call_next):
        """Process request and apply rate limiting."""
        
        # Skip rate limiting for certain endpoints
        if should_skip_rate_limiting(request):
            return await call_next(request)
        
        # Get rate limit key
        key = get_rate_limit_key(request)
        if key is None:
            # Cannot determine key, allow request (graceful degradation)
            logger.warning("Cannot determine rate limit key, allowing request")
            return await call_next(request)
        
        # Check rate limit
        allowed, retry_after, remaining = check_rate_limit(
            key=key,
            limit=RATE_LIMIT_REQUESTS,
            window_seconds=RATE_LIMIT_WINDOW_SECONDS
        )
        
        if not allowed:
            # Rate limit exceeded
            error_response = {
                "error": {
                    "code": "RATE_LIMIT_EXCEEDED",
                    "message": f"Rate limit exceeded. Please try again in {retry_after} seconds.",
                    "retry_after": retry_after
                }
            }
            
            response = JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content=error_response
            )
            
            # Add rate limit headers
            response.headers["Retry-After"] = str(retry_after)
            response.headers["X-RateLimit-Limit"] = str(RATE_LIMIT_REQUESTS)
            response.headers["X-RateLimit-Remaining"] = "0"
            
            logger.info(f"Rate limit exceeded for key {key}, retry_after: {retry_after}")
            return response
        
        # Within limit, continue to handler
        response = await call_next(request)
        
        # Add rate limit headers to successful responses
        response.headers["X-RateLimit-Limit"] = str(RATE_LIMIT_REQUESTS)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        
        return response
