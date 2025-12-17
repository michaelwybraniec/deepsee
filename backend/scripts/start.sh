#!/bin/sh
set -e

echo "🚀 Starting API initialization..."

# Run initialization script
python scripts/init_docker.py

# Start uvicorn
echo "✅ Starting uvicorn server..."
exec uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
