#!/bin/bash
# Script to create test user for E2E tests
# Run this before running E2E tests if test user doesn't exist

cd "$(dirname "$0")/../../.." || exit 1

echo "Creating test user for E2E tests..."

if [ -d "backend" ]; then
  cd backend
  if [ -d ".venv" ]; then
    .venv/bin/python3 scripts/create_user.py testuser test@example.com testpassword 2>/dev/null
    if [ $? -eq 0 ]; then
      echo "✅ Test user 'testuser' created successfully"
    else
      echo "⚠️  Test user may already exist or error occurred"
    fi
  else
    echo "❌ Backend .venv not found. Please set up backend first."
    exit 1
  fi
else
  echo "❌ Backend directory not found"
  exit 1
fi
