"""Metrics middleware for FastAPI."""

import time
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from infrastructure.metrics.registry import (
    HTTP_REQUESTS_TOTAL,
    HTTP_ERRORS_TOTAL,
    HTTP_REQUEST_DURATION_SECONDS
)
from infrastructure.logging.config import get_logger
from api.middleware.correlation_id import get_correlation_id

logger = get_logger(__name__)


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to collect HTTP request metrics."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and collect metrics.
        
        - Records request start time
        - Increments request counter
        - Records latency histogram
        - Increments error counter if status >= 400
        """
        # Record start time
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Extract method and endpoint
        method = request.method
        endpoint = request.url.path
        
        # Normalize endpoint (remove IDs for better aggregation)
        # e.g., /api/tasks/123 -> /api/tasks/{id}
        normalized_endpoint = self._normalize_endpoint(endpoint)
        
        # Record metrics
        status_code = response.status_code
        
        # Increment request counter
        HTTP_REQUESTS_TOTAL.labels(
            method=method,
            endpoint=normalized_endpoint,
            status_code=str(status_code)
        ).inc()
        
        # Record latency
        HTTP_REQUEST_DURATION_SECONDS.labels(
            method=method,
            endpoint=normalized_endpoint
        ).observe(duration)
        
        # Increment error counter if status >= 400
        if status_code >= 400:
            error_type = self._get_error_type(status_code)
            HTTP_ERRORS_TOTAL.labels(
                method=method,
                endpoint=normalized_endpoint,
                error_type=error_type
            ).inc()
        
        return response
    
    def _normalize_endpoint(self, endpoint: str) -> str:
        """
        Normalize endpoint path by replacing IDs with {id}.
        
        Examples:
            /api/tasks/123 -> /api/tasks/{id}
            /api/tasks/123/attachments/456 -> /api/tasks/{id}/attachments/{id}
            /api/tasks/ -> /api/tasks/
        """
        import re
        # Replace numeric IDs with {id}
        normalized = re.sub(r'/\d+(?=/|$)', '/{id}', endpoint)
        # Replace UUIDs with {id}
        normalized = re.sub(r'/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}(?=/|$)', '/{id}', normalized, flags=re.IGNORECASE)
        return normalized
    
    def _get_error_type(self, status_code: int) -> str:
        """
        Get error type from status code.
        
        Args:
            status_code: HTTP status code
        
        Returns:
            Error type string
        """
        if 400 <= status_code < 500:
            return "client_error"
        elif status_code >= 500:
            return "server_error"
        else:
            return "unknown"
