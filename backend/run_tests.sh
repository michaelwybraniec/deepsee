#!/bin/bash
# Test runner script for all test categories

set -e

echo "Running all test categories..."
echo ""

# Unit tests
echo "=== Unit Tests ==="
pytest tests/unit/ -v
echo ""

# Integration tests
echo "=== Integration Tests ==="
pytest tests/integration/ -v
echo ""

# Worker tests
echo "=== Worker Tests ==="
pytest tests/worker/ -v
echo ""

# Contract tests
echo "=== Contract Tests ==="
pytest tests/contract/ -v
echo ""

# Observability tests
echo "=== Observability Tests ==="
pytest tests/observability/ -v
echo ""

echo "✅ All test categories completed!"
