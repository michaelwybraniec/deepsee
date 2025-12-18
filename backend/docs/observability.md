# Observability Guide

Quick reference for monitoring and logging.

## Quick Links

- **Metrics**: Grafana → Dashboards → Task Tracker - System Metrics
- **Logs**: Grafana → Drilldown → Logs ([Loki Guide](loki-logs.md))
- **Prometheus**: <http://localhost:9090>

## Components

- **Metrics**: Prometheus scrapes `/api/metrics`, visualized in Grafana
- **Logs**: Promtail → Loki → Grafana Logs

## Command Line

```bash
docker compose logs api -f              # View logs
curl http://localhost:8000/api/metrics  # View metrics
curl http://localhost:9090/api/v1/targets  # Check Prometheus targets
```
