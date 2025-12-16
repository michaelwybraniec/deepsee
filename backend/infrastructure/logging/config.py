"""Structured logging configuration."""

import logging
import sys
import structlog
from typing import Any, Dict


def configure_structured_logging() -> None:
    """
    Configure structured logging with JSON output.
    
    Sets up structlog to output JSON-formatted logs with proper processors.
    """
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,  # Merge context variables
            structlog.processors.add_log_level,  # Add log level
            structlog.processors.TimeStamper(fmt="iso"),  # ISO timestamp
            structlog.processors.StackInfoRenderer(),  # Stack traces
            structlog.processors.format_exc_info,  # Exception formatting
            structlog.processors.JSONRenderer()  # JSON output
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str = None) -> structlog.BoundLogger:
    """
    Get a structured logger instance.
    
    Args:
        name: Logger name (typically __name__ of the calling module)
    
    Returns:
        Configured structlog logger
    """
    return structlog.get_logger(name)
