# Prometheus + Grafana Usage Guide

This guide explains how to use Prometheus and Grafana for monitoring the Task Tracker application.

## Overview

- **Prometheus**: Scrapes metrics from the API's `/api/metrics` endpoint
- **Grafana**: Visualizes metrics with dashboards

## Starting Services

### Option 1: Docker Compose (Recommended)

```bash
# Start all services including Prometheus and Grafana
docker compose up

# Or start only observability stack
docker compose up prometheus grafana api
```

### Option 2: Standalone

**Prometheus:**
```bash
# Run Prometheus
docker run -d \
  -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus:latest
```

**Grafana:**
```bash
# Run Grafana
docker run -d \
  -p 3000:3000 \
  -e GF_SECURITY_ADMIN_USER=admin \
  -e GF_SECURITY_ADMIN_PASSWORD=admin \
  -v $(pwd)/grafana/provisioning:/etc/grafana/provisioning \
  -v $(pwd)/grafana/dashboards:/etc/grafana/provisioning/dashboards \
  grafana/grafana:latest
```

## Access Points

- **Prometheus UI**: http://localhost:9090
- **Grafana UI**: http://localhost:3000
  - Default credentials: `admin` / `admin` (change in production!)

## Grafana Dashboard

The Task Tracker dashboard is automatically provisioned and includes:

1. **Request Volume**: Requests per second by endpoint
2. **Error Rate**: Percentage of errors over total requests
3. **Request Latency**: p50 and p95 percentiles
4. **Reminders Processed**: Success/failure rates for reminder jobs

### Accessing the Dashboard

1. Log in to Grafana (http://localhost:3000)
2. Navigate to **Dashboards** → **Task Tracker - System Metrics**
3. The dashboard will show real-time metrics from the API

## Prometheus Queries

You can query metrics directly in Prometheus UI:

**Request Count:**
```
http_requests_total
```

**Request Rate:**
```
rate(http_requests_total[1m])
```

**Error Rate:**
```
rate(http_errors_total[1m]) / rate(http_requests_total[1m])
```

**Latency (p95):**
```
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[1m]))
```

**Reminders Processed:**
```
reminders_processed_total
```

## Configuration

### Prometheus Configuration

Edit `prometheus.yml` to adjust:
- Scrape interval (default: 15s)
- Metrics path (default: `/api/metrics`)
- Target host (default: `api:8000`)

### Grafana Configuration

- **Data Source**: Automatically configured to use Prometheus
- **Dashboards**: Located in `grafana/dashboards/`
- **Provisioning**: Configured in `grafana/provisioning/`

## Troubleshooting

### Prometheus not scraping metrics

1. Check API is running: `curl http://localhost:8000/api/metrics`
2. Check Prometheus targets: http://localhost:9090/targets
3. Verify network connectivity (if using Docker Compose)

### Grafana not showing data

1. Verify Prometheus data source is connected
2. Check Prometheus has data: http://localhost:9090/graph
3. Verify time range in Grafana dashboard

### Metrics not appearing

1. Ensure API is generating metrics (make some requests)
2. Check `/api/metrics` endpoint returns Prometheus format
3. Verify scrape configuration in `prometheus.yml`

## Production Considerations

- Change default Grafana admin password
- Use environment variables for sensitive configuration
- Consider authentication for Prometheus/Grafana
- Set up retention policies for Prometheus data
- Configure alerting rules in Prometheus
