# Monitoring & Logging Usage Guide

This guide explains how to access and use the monitoring, logging, and health check features implemented in the Task Tracker API.

## Overview

The API provides three main observability features:
1. **Structured Logging** with correlation IDs
2. **Metrics** in Prometheus format
3. **Health Check Endpoints**

## Structured Logging

### Where to Find Logs

Logs are output to **stdout** (standard output) of the backend process. When running the API with `uvicorn`, you'll see logs in your terminal/console.

**Example:**
```bash
cd backend
source .venv/bin/activate
uvicorn api.main:app --reload
```

You'll see structured JSON logs like:
```json
{"event": "reminder_job_started", "worker_run_id": "worker-run-2024-12-16-10-30-00", "correlation_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890", "timestamp": "2024-12-16T10:30:00.123456Z", "level": "info"}
```

### Log Format

All logs are in **JSON format** with the following structure:
- `event`: Event name (e.g., `"reminder_job_started"`, `"task_created"`)
- `correlation_id`: Unique ID for tracing requests across the system
- `timestamp`: ISO 8601 timestamp
- `level`: Log level (`info`, `warning`, `error`, `debug`)
- Additional context fields specific to each event

### Correlation IDs

Every API request gets a **correlation ID** that:
- Is generated automatically (UUID v4) if not provided
- Can be provided via `X-Correlation-ID` request header
- Is returned in `X-Correlation-ID` response header
- Is included in all log entries for that request
- Allows tracing a request across API handlers and worker jobs

**Example:**
```bash
# Request with custom correlation ID
curl -H "X-Correlation-ID: my-custom-id-123" http://localhost:8000/api/health

# Response includes the correlation ID
# X-Correlation-ID: my-custom-id-123
```

### Filtering Logs

Since logs are JSON, you can filter them using tools like `jq`:

```bash
# Filter by correlation ID
uvicorn api.main:app 2>&1 | jq 'select(.correlation_id == "a1b2c3d4-e5f6-7890-abcd-ef1234567890")'

# Filter by log level
uvicorn api.main:app 2>&1 | jq 'select(.level == "error")'

# Filter by event type
uvicorn api.main:app 2>&1 | jq 'select(.event == "reminder_sent")'
```

### Log Levels

- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages (default level)
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for failures
- **CRITICAL**: Critical errors requiring immediate attention

## Metrics

### Metrics Endpoint

Metrics are exposed at **`GET /api/metrics`** in Prometheus text format.

**Example:**
```bash
curl http://localhost:8000/api/metrics
```

**Response format:**
```
# HELP http_requests_total Total number of HTTP requests
# TYPE http_requests_total counter
http_requests_total{endpoint="/api/tasks/",method="GET",status_code="200"} 42.0

# HELP http_request_duration_seconds HTTP request duration in seconds
# TYPE http_request_duration_seconds histogram
http_request_duration_seconds_bucket{endpoint="/api/tasks/",method="GET",le="0.1"} 35.0
http_request_duration_seconds_bucket{endpoint="/api/tasks/",method="GET",le="0.5"} 40.0
...
```

### Available Metrics

#### 1. `http_requests_total`
- **Type**: Counter
- **Labels**: `method`, `endpoint`, `status_code`
- **Description**: Total number of HTTP requests
- **Example**: `http_requests_total{method="GET",endpoint="/api/tasks/",status_code="200"} 42.0`

#### 2. `http_errors_total`
- **Type**: Counter
- **Labels**: `method`, `endpoint`, `error_type` (`client_error` or `server_error`)
- **Description**: Total number of HTTP errors (status >= 400)
- **Example**: `http_errors_total{method="GET",endpoint="/api/tasks/",error_type="client_error"} 2.0`

#### 3. `http_request_duration_seconds`
- **Type**: Histogram
- **Labels**: `method`, `endpoint`
- **Buckets**: `[0.1, 0.5, 1.0, 2.0, 5.0]` seconds
- **Description**: HTTP request latency distribution
- **Example**: `http_request_duration_seconds_bucket{method="GET",endpoint="/api/tasks/",le="0.5"} 40.0`

#### 4. `reminders_processed_total`
- **Type**: Counter
- **Labels**: `status` (`success` or `failure`)
- **Description**: Total number of reminders processed by the worker
- **Example**: `reminders_processed_total{status="success"} 15.0`

### Querying Metrics

You can query metrics directly from the endpoint or use Prometheus-compatible tools:

```bash
# Get all metrics
curl http://localhost:8000/api/metrics

# Filter specific metric
curl http://localhost:8000/api/metrics | grep "http_requests_total"

# Count total requests
curl http://localhost:8000/api/metrics | grep "http_requests_total" | awk '{sum+=$NF} END {print sum}'
```

### Using with Prometheus

To use these metrics with Prometheus, configure Prometheus to scrape the `/api/metrics` endpoint:

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'task-tracker-api'
    scrape_interval: 15s
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/api/metrics'
```

**Note**: Full Prometheus + Grafana setup is tracked as an unplanned task (U-1) in the project backlog.

## Health Checks

### Health Check Endpoints

#### 1. Comprehensive Health Check
**Endpoint**: `GET /api/health`

Returns overall health status and individual component checks.

**Response (200 OK if healthy):**
```json
{
  "status": "healthy",
  "checks": {
    "api": {
      "status": "healthy",
      "message": "API is responding"
    },
    "database": {
      "status": "healthy",
      "message": "Database is healthy"
    },
    "worker": {
      "status": "healthy",
      "message": "Worker scheduler is running"
    }
  }
}
```

**Response (503 Service Unavailable if unhealthy):**
```json
{
  "status": "unhealthy",
  "checks": {
    "api": {
      "status": "healthy",
      "message": "API is responding"
    },
    "database": {
      "status": "unhealthy",
      "message": "Database error: connection timeout"
    },
    "worker": {
      "status": "unhealthy",
      "message": "Worker scheduler is not running"
    }
  }
}
```

#### 2. Individual Health Checks

**API Health**: `GET /api/health/api`
```json
{
  "status": "healthy",
  "check": "api",
  "message": "API is responding"
}
```

**Database Health**: `GET /api/health/database`
```json
{
  "status": "healthy",
  "check": "database",
  "message": "Database is healthy"
}
```

**Worker Health**: `GET /api/health/worker`
```json
{
  "status": "healthy",
  "check": "worker",
  "message": "Worker scheduler is running"
}
```

### Using Health Checks

**Example:**
```bash
# Check overall health
curl http://localhost:8000/api/health

# Check database only
curl http://localhost:8000/api/health/database

# Use in monitoring scripts
if curl -f http://localhost:8000/api/health > /dev/null 2>&1; then
  echo "API is healthy"
else
  echo "API is unhealthy"
  exit 1
fi
```

### Health Check Status Codes

- **200 OK**: All checks passed (or API check passed if using individual endpoints)
- **503 Service Unavailable**: One or more checks failed

## Integration with Monitoring Tools

### Log Aggregation

For production, consider forwarding logs to:
- **Loki** (Grafana stack)
- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Cloud logging** (AWS CloudWatch, Google Cloud Logging, Azure Monitor)

### Metrics Collection

The `/api/metrics` endpoint is compatible with:
- **Prometheus** (scrape the endpoint)
- **Grafana** (via Prometheus data source)
- **Other Prometheus-compatible tools**

### Health Check Monitoring

Health checks can be monitored with:
- **Prometheus** (using `up` metric or blackbox exporter)
- **Kubernetes** (liveness/readiness probes)
- **Load balancers** (health check endpoints)
- **Monitoring services** (Pingdom, UptimeRobot, etc.)

## Best Practices

1. **Correlation IDs**: Always include `X-Correlation-ID` in requests when tracing issues
2. **Log Levels**: Use appropriate log levels (don't log sensitive data)
3. **Metrics**: Monitor key metrics (request rate, error rate, latency)
4. **Health Checks**: Set up automated health check monitoring
5. **Alerting**: Configure alerts based on metrics and health checks

## Troubleshooting

### Logs Not Appearing

- Check that the API process is running
- Verify logs are going to stdout (not a file)
- Check log level configuration (default is INFO)

### Metrics Not Updating

- Verify the `/api/metrics` endpoint is accessible
- Check that requests are being made to the API
- Ensure metrics middleware is enabled

### Health Checks Failing

- **Database**: Check database connection and credentials
- **Worker**: Verify worker scheduler is running (check logs)
- **API**: If API check fails, the endpoint itself is down

## Related Documentation

- [Monitoring & Logging Requirements](monitoring-logging-requirements.md) - Detailed requirements
- [Testing Guide](testing.md) - How to test observability features
- [Architecture](../docs/architecture.md) - System architecture overview
