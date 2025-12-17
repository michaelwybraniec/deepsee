# Monitoring

**Metrics Dashboard**: See [Grafana](grafana.md)

**Health Check Endpoints**: See [API Documentation](api.md) (Swagger UI: `/docs`, ReDoc: `/redoc`)

## Logs

**Location**: stdout (terminal/console when running uvicorn)

**Format**: JSON with `correlation_id` for request tracing

**Correlation ID**:

- Auto-generated (UUID v4) or provided via `X-Correlation-ID` header
- Returned in `X-Correlation-ID` response header
- Included in all log entries for request tracing

## Metrics

**Endpoint**: `GET /api/metrics` (Prometheus format)
