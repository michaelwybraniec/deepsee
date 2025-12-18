# Prometheus Internal Metrics

Prometheus exposes its own metrics for monitoring Prometheus's performance and storage health.

## Access

- **Dashboard**: Grafana → Dashboards → **Prometheus 2.0 Stats**
- **Metrics Endpoint**: `http://localhost:9090/metrics` (Prometheus scraping itself)
- **Prometheus Job**: `prometheus`

## Key Metrics

- `prometheus_tsdb_head_samples_appended_total` - Samples ingested
- `prometheus_tsdb_blocks_loaded` - TSDB blocks loaded
- `prometheus_tsdb_wal_corruptions_total` - WAL corruptions (should be 0)
- `prometheus_engine_query_duration_seconds` - Query performance

## Troubleshooting

**No data after restart?**
- Wait 5-10 minutes for rate calculations (need 5+ minutes of history)
- Some panels only show data with specific operations (compactions, queries)

**Some panels show "No data"?**
- **Rule Eval Duration**: Only if alerting rules are configured (none by default)
- **Memory Profile**: Only if memory profiling is enabled
- This is normal for a simple setup
