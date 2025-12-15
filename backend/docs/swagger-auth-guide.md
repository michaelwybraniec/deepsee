# Swagger UI Authorization Guide

## How to Authorize in Swagger UI

### Step 1: Get Your JWT Token

1. Open Swagger UI: `http://localhost:8000/docs`
2. Find the **"auth"** section
3. Click on **POST /api/auth/login**
4. Click **"Try it out"** button
5. Enter your credentials in the request body:
   ```json
   {
     "username": "your_username",
     "password": "your_password"
   }
   ```
6. Click **"Execute"**
7. In the response, find the `"token"` field and **copy the entire token value**

Example response:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}
```

### Step 2: Authorize in Swagger

1. Click the **"Authorize"** button (🔒 lock icon in the top right)
2. In the **"HTTPBearer"** section, you'll see a **"Value"** field
3. **Paste ONLY the token** (without "Bearer " prefix)
4. Click **"Authorize"**
5. Click **"Close"**

**Important:**
- ✅ **DO**: Paste just the token: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
- ❌ **DON'T**: Include "Bearer " prefix (Swagger adds it automatically)

### Step 3: Test Protected Endpoints

After authorizing, you can test any protected endpoint:

1. Navigate to any endpoint (e.g., **GET /api/worker/status**)
2. Click **"Try it out"**
3. Click **"Execute"**
4. The request will automatically include the Bearer token in the Authorization header

## Example: Testing Worker Endpoints

### 1. Get Worker Status

1. Go to **"worker"** section
2. Click **GET /api/worker/status**
3. Click **"Try it out"**
4. Click **"Execute"**
5. See the response:
   ```json
   {
     "status": "running",
     "running": true,
     "next_run": "2024-01-15T11:00:00",
     "last_reminder_sent": "2024-01-15T10:00:00",
     "schedule": "Every hour"
   }
   ```

### 2. Get Worker Statistics

1. Click **GET /api/worker/statistics**
2. Click **"Try it out"**
3. Click **"Execute"**

### 3. Manually Trigger Worker

1. Click **POST /api/worker/trigger**
2. Click **"Try it out"**
3. Click **"Execute"**

## Troubleshooting

### "401 Unauthorized" Error

**Problem**: Getting 401 when testing endpoints

**Solutions**:
1. Make sure you clicked **"Authorize"** and pasted the token
2. Check that the token is valid (not expired)
3. Get a new token by logging in again
4. Make sure you pasted **only the token** (no "Bearer " prefix)

### Token Expired

**Problem**: Token no longer works

**Solution**: Get a new token by logging in again via **POST /api/auth/login**

### Can't See "Authorize" Button

**Problem**: Don't see the lock icon

**Solution**: 
- Make sure you're on `http://localhost:8000/docs`
- Refresh the page
- Check browser console for errors

## Quick Reference

| Action | What to Do |
|--------|-----------|
| Get Token | Use POST /api/auth/login with username/password |
| Authorize | Click "Authorize" → Paste token (no "Bearer ") → Click "Authorize" |
| Test Endpoint | Click endpoint → "Try it out" → "Execute" |
| Token Expired | Login again to get new token |

## Visual Guide

```
┌─────────────────────────────────────────┐
│  Swagger UI                             │
│  ┌───────────────────────────────────┐  │
│  │  [Authorize] 🔒  ← Click here     │  │
│  └───────────────────────────────────┘  │
│                                          │
│  When you click "Authorize":             │
│  ┌───────────────────────────────────┐  │
│  │  HTTPBearer (http, Bearer)        │  │
│  │  Value: [paste token here]        │  │
│  │  [Authorize] [Close]              │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

## Example Token Format

A JWT token looks like this (three parts separated by dots):
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

**Paste the entire token** (all three parts) into the Value field.
