# Grafana

## Access

- **Grafana**: http://localhost:3000 (default: l:`admin` / p:`admin`)
- **Prometheus**: http://localhost:9090

## Start Services

```bash
docker compose up -d prometheus grafana
```

## Dashboard

**Task Tracker Dashboard** (automatically provisioned) shows:
- Request volume (requests/sec)
- Error rate (%)
- Request latency (p50/p95)
- Reminders processed

Access: Log in to Grafana → **Dashboards** → **Browse** → **Task Tracker Dashboard**

## Official Documentation

- [Grafana Documentation](https://grafana.com/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/)
