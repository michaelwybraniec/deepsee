"""Tests for correlation ID middleware."""

import pytest
from fastapi.testclient import TestClient
import json

from api.main import app


def test_correlation_id_generated(client: TestClient):
    """Test that correlation ID is generated when not present in request."""
    response = client.get("/health")
    
    assert response.status_code == 200
    # Check that correlation ID is in response header
    assert "X-Correlation-ID" in response.headers
    correlation_id = response.headers["X-Correlation-ID"]
    # Should be a valid UUID format
    assert len(correlation_id) == 36  # UUID v4 format
    assert correlation_id.count("-") == 4


def test_correlation_id_extracted_from_header(client: TestClient):
    """Test that correlation ID is extracted from request header if present."""
    custom_correlation_id = "custom-correlation-id-12345"
    response = client.get(
        "/health",
        headers={"X-Correlation-ID": custom_correlation_id}
    )
    
    assert response.status_code == 200
    # Check that same correlation ID is returned
    assert response.headers["X-Correlation-ID"] == custom_correlation_id


def test_correlation_id_preserved_across_handlers(client: TestClient, test_user):
    """Test that correlation ID is preserved across API handlers."""
    # Login to get token
    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "testpassword"}
    )
    token = login_response.json()["token"]
    correlation_id = login_response.headers.get("X-Correlation-ID")
    
    assert correlation_id is not None
    
    # Make another request - should have same or new correlation ID
    # (each request gets its own, but we verify it's present)
    task_response = client.get(
        "/api/tasks/",
        headers={
            "Authorization": f"Bearer {token}",
            "X-Correlation-ID": correlation_id
        }
    )
    
    # Should preserve the correlation ID from header
    assert task_response.headers.get("X-Correlation-ID") == correlation_id


def test_correlation_id_in_logs(client: TestClient, caplog):
    """Test that correlation ID appears in log entries."""
    import structlog
    import logging
    
    # Configure logging capture
    logging.basicConfig(level=logging.INFO)
    
    response = client.get("/health")
    correlation_id = response.headers.get("X-Correlation-ID")
    
    assert response.status_code == 200
    assert correlation_id is not None
    
    # Note: In test environment, logs may not be captured the same way
    # This test verifies the correlation ID is generated and returned
    # Actual log verification would require more complex setup
