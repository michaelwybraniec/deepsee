"""Metrics registry for Prometheus metrics."""

from prometheus_client import Counter, Histogram, REGISTRY, generate_latest, CONTENT_TYPE_LATEST

# Request metrics
HTTP_REQUESTS_TOTAL = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status_code']
)

HTTP_ERRORS_TOTAL = Counter(
    'http_errors_total',
    'Total number of HTTP errors',
    ['method', 'endpoint', 'error_type']
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0]
)

# Worker metrics
REMINDERS_PROCESSED_TOTAL = Counter(
    'reminders_processed_total',
    'Total number of reminders processed',
    ['status']  # 'success' or 'failure'
)


def get_metrics_text() -> str:
    """
    Get metrics in Prometheus text format.
    
    Returns:
        Metrics in Prometheus text format
    """
    return generate_latest(REGISTRY).decode('utf-8')


def get_metrics_content_type() -> str:
    """
    Get content type for metrics endpoint.
    
    Returns:
        Content type string for Prometheus metrics
    """
    return CONTENT_TYPE_LATEST
