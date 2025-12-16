"""Correlation ID middleware for FastAPI."""

import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from infrastructure.logging.config import get_logger

logger = get_logger(__name__)

# Header name for correlation ID
CORRELATION_ID_HEADER = "X-Correlation-ID"


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """Middleware to extract or generate correlation IDs for each request."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and add correlation ID.
        
        - Extracts correlation ID from X-Correlation-ID header if present
        - Generates new UUID v4 if not present
        - Stores correlation ID in request.state
        - Adds correlation ID to response header
        - Includes correlation ID in all log entries via contextvars
        """
        # Extract or generate correlation ID
        correlation_id = request.headers.get(CORRELATION_ID_HEADER)
        if not correlation_id:
            correlation_id = str(uuid.uuid4())
        
        # Store in request state for access in handlers
        request.state.correlation_id = correlation_id
        
        # Add to structlog contextvars so it's included in all log entries
        import structlog
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(correlation_id=correlation_id)
        
        # Process request
        response = await call_next(request)
        
        # Add correlation ID to response header
        response.headers[CORRELATION_ID_HEADER] = correlation_id
        
        return response


def get_correlation_id(request: Request) -> str:
    """
    Get correlation ID from request state.
    
    Args:
        request: FastAPI request object
    
    Returns:
        Correlation ID string
    """
    return getattr(request.state, "correlation_id", None)
