"""Metrics endpoint for Prometheus."""

from fastapi import APIRouter
from fastapi.responses import Response

from infrastructure.metrics.registry import get_metrics_text, get_metrics_content_type

router = APIRouter(prefix="/api", tags=["metrics"])


@router.get("/metrics")
def get_metrics():
    """
    Get Prometheus metrics.
    
    Returns metrics in Prometheus text format.
    This endpoint is used by Prometheus to scrape metrics.
    """
    metrics_text = get_metrics_text()
    return Response(
        content=metrics_text,
        media_type=get_metrics_content_type()
    )
