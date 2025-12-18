# Monitoring

**Complete Observability Guide**: See [Observability Guide](observability.md)

**Metrics Dashboard**: See [Grafana](grafana.md)

**Health Check Endpoints**: See [API Documentation](api.md) (Swagger UI: `/docs`, ReDoc: `/redoc`)

## Logs

**Location**: stdout (terminal/console when running uvicorn)

**Format**: JSON with `correlation_id` for request tracing

**Correlation ID**:

- Auto-generated (UUID v4) or provided via `X-Correlation-ID` header
- Returned in `X-Correlation-ID` response header
- Included in all log entries for request tracing

### Viewing Logs in Grafana

**Loki Integration**: Logs are automatically collected by Promtail and sent to Loki.

**Access Logs in Grafana:**
1. Go to Grafana: <http://localhost:3000>
2. Navigate to: **Drilldown > Logs**
3. Select **Loki** as the data source
4. Use LogQL queries to filter logs:
   - `{service="api"}` - All API logs
   - `{service="worker"}` - All worker logs
   - `{service="api"} |= "error"` - API error logs
   - `{service="api"} | json | correlation_id="abc123"` - Logs by correlation ID

**Command Line Access:**
```bash
# View logs via Docker (still works)
docker compose logs api -f
docker compose logs worker -f
```

**Log Aggregation**: Loki automatically collects logs from all Docker containers with `task-tracker-` prefix.

## Metrics

### Application Metrics

**Endpoint**: `GET /api/metrics` (Prometheus format)

### Accessing Metrics

**From your browser (host machine):**
```
http://localhost:8000/api/metrics
```

**From Docker containers (e.g., Prometheus):**
```
http://api:8000/api/metrics
```

**Important:** 
- `localhost:8000` works from your host machine (browser, terminal)
- `api:8000` only works from inside Docker containers on the same network
- Prometheus (running in Docker) uses `api:8000` to scrape metrics
- Your browser must use `localhost:8000`

### Grafana Queries

**⚠️ Important:** Never graph `*_created` metrics - these are metadata timestamps, not actual values.

See [Grafana Queries Guide](grafana-queries.md) for correct Prometheus queries for:
- Request duration (average, p50, p95, p99)
- Request rate
- Error rate
- Reminders processed

### Grafana Internal Metrics

Grafana also exposes its own metrics for monitoring Grafana's performance and usage.

**Dashboard**: Dashboards → **Grafana metrics**

**Metrics Endpoint**: `http://grafana:3000/metrics` (scraped by Prometheus)

See [Grafana Internal Metrics](grafana-internal-metrics.md) for details.

### Prometheus Internal Metrics

Prometheus exposes its own internal metrics for monitoring Prometheus's performance, storage, and health.

**Dashboard**: Dashboards → **Prometheus 2.0 Stats**

**Metrics Endpoint**: `http://localhost:9090/metrics` (Prometheus scraping itself)

See [Prometheus Internal Metrics](prometheus-internal-metrics.md) for details.
