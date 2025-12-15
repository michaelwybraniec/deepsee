# Quick Start Guide

## Starting the API Server

### 1. Install Dependencies

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
JWT_SECRET_KEY=your-secret-key-minimum-32-characters-long
API_VERSION=1.0.0
```

### 3. Start the Server

```bash
# Make sure you're in the backend directory
cd backend

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Start the server
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

The server will start on `http://localhost:8000`

**Note**: The worker starts automatically when the API starts (unless `ENVIRONMENT=test`).

### 4. Verify Server is Running

```bash
# Check root endpoint
curl http://localhost:8000/

# Check health endpoint
curl http://localhost:8000/health

# Check Swagger docs
open http://localhost:8000/docs
```

## Testing Worker API Endpoints

### 1. Get Authentication Token

```bash
# Login to get token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

This returns a token like:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 2. Test Worker Endpoints

```bash
# Replace <token> with your actual token

# Get worker status
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/worker/status

# Get worker statistics
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/worker/statistics

# Manually trigger worker
curl -X POST -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/worker/trigger
```

## Using Swagger UI

1. Start the server
2. Open browser to `http://localhost:8000/docs`
3. Click "Authorize" button (top right)
4. Enter your token (without "Bearer " prefix)
5. Navigate to "worker" section
6. Test endpoints directly from the browser

## Troubleshooting

### 404 Error on Worker Endpoints

**Problem**: Getting 404 when accessing `/api/worker/status`

**Solutions**:
1. **Restart the server**: The routes were added recently, restart the server:
   ```bash
   # Stop the server (Ctrl+C)
   # Then restart:
   uvicorn api.main:app --reload
   ```

2. **Check server is running**: 
   ```bash
   curl http://localhost:8000/health
   ```

3. **Check route registration**: Verify in Swagger UI (`http://localhost:8000/docs`) that worker endpoints are listed

4. **Check authentication**: Make sure you're including the Bearer token:
   ```bash
   curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/api/worker/status
   ```

### Worker Not Starting

**Problem**: Worker scheduler not starting

**Check**:
1. Look for log message: `"Worker scheduler started - reminder job will run every hour"`
2. Check if `ENVIRONMENT=test` is set (this disables worker)
3. Check for errors in console output

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'apscheduler'`

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

## Common Commands

```bash
# Start server
uvicorn api.main:app --reload

# Start server on different port
uvicorn api.main:app --reload --port 8080

# Start server without worker (for testing)
ENVIRONMENT=test uvicorn api.main:app --reload

# Run tests
pytest tests/ -v

# Check API documentation
open http://localhost:8000/docs
```
