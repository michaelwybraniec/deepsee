# Logging Guide

Essential guide to accessing and understanding logs. For viewing logs in Grafana, see [Loki Logs Guide](loki-logs.md).

## Quick Access Commands

```bash
# Backend API logs
docker compose logs api -f

# Worker logs
docker compose logs worker -f

# All services
docker compose logs -f

# Filter for errors
docker compose logs api | grep -i error
```

## Log Format

Backend uses **structured JSON logging** (structlog):
- Machine-readable JSON format
- Correlation IDs for request tracking
- Consistent event naming

Example:
```json
{
  "event": "task_created",
  "level": "info",
  "message": "Task created successfully",
  "correlation_id": "abc-123",
  "timestamp": "2025-12-18T20:00:00Z",
  "task_id": 1
}
```

## Essential Health Indicators

### ✅ Healthy System
- **API**: "Application startup complete", health check returns 200
- **Worker**: "Worker service started successfully"
- **Database**: "database system is ready to accept connections"

### ⚠️ Common Issues
- **SSL errors**: Add `?sslmode=disable` to database URL
- **Connection refused**: Check if service container is running
- **Authentication failed**: Verify credentials in environment variables

## Viewing Logs in Grafana

For advanced log viewing, filtering, and search, see [Loki Logs Guide](loki-logs.md).

Access: Grafana → **Drilldown > Logs**
