# Grafana Internal Metrics

Grafana exposes its own metrics for monitoring Grafana's performance.

## Access

- **Dashboard**: Grafana → Dashboards → **Grafana metrics**
- **Metrics Endpoint**: `http://grafana:3000/metrics` (scraped by Prometheus)
- **Prometheus Job**: `grafana`

## Key Metrics

- `grafana_http_request_total` - Request counts
- `grafana_http_request_duration_seconds_*` - Request latency
- `grafana_dashboard_count` - Number of dashboards
- `grafana_active_users` - Active user count

## Troubleshooting

**No data?**
- Check Prometheus targets: `http://localhost:9090/targets` → Look for `grafana` job
- Verify endpoint: `curl http://localhost:3000/metrics`
- Wait a few minutes for data to accumulate
