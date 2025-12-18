# Viewing Logs in Grafana (Loki)

## Quick Access

1. Grafana → Drilldown → **Logs**
2. Select data source: **Loki**

## Common Queries

```logql
{service="api"}                              # All API logs
{service="api"} |= "error"                   # API errors
{service="api"} | json | correlation_id="abc" # By correlation ID
{service=~"api|worker"} |= "error"           # All errors
{project="task-tracker"}                      # Only this project
```

## Available Labels

- `service`: api, worker, database, frontend, etc.
- `project`: task-tracker (this project) or other
- `container`: Full container name

## Tips

- Use `| json` to parse JSON log fields
- Filter by project: `{project="task-tracker"}` to exclude other containers
- Use time range selector (top right) for historical logs

## Troubleshooting

**No logs showing?**
- Check Loki: `docker compose ps loki`
- Check Promtail: `docker compose logs promtail`
- Generate logs: `curl http://localhost:8000/api/health/api`

**Seeing `unknown_service`?**
- Old logs from before labeling fix
- Filter out: `{service!="unknown_service"}`
- Or exclude in Grafana UI service selector
