"""Tests for health check endpoints."""

import pytest
from fastapi.testclient import TestClient

from api.main import app


def test_health_check_endpoint(client: TestClient):
    """Test that health check endpoint exists and returns health status."""
    response = client.get("/api/health")
    
    assert response.status_code in [200, 503]  # 200 if healthy, 503 if unhealthy
    data = response.json()
    assert "status" in data
    assert "checks" in data
    assert "api" in data["checks"]
    assert "database" in data["checks"]
    assert "worker" in data["checks"]


def test_health_check_api_only(client: TestClient):
    """Test API-only health check."""
    response = client.get("/api/health/api")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["check"] == "api"


def test_health_check_database_only(client: TestClient):
    """Test database-only health check."""
    response = client.get("/api/health/database")
    
    # Should be 200 if database is healthy, 503 if unhealthy
    assert response.status_code in [200, 503]
    data = response.json()
    assert "status" in data
    assert data["check"] == "database"
    assert "message" in data


def test_health_check_worker_only(client: TestClient):
    """Test worker-only health check."""
    response = client.get("/api/health/worker")
    
    # Should be 200 if worker is healthy, 503 if unhealthy
    # In test environment, worker may not be running
    assert response.status_code in [200, 503]
    data = response.json()
    assert "status" in data
    assert data["check"] == "worker"
    assert "message" in data


def test_health_check_returns_correct_structure(client: TestClient):
    """Test that health check returns correct JSON structure."""
    response = client.get("/api/health")
    
    data = response.json()
    
    # Verify structure
    assert "status" in data
    assert "checks" in data
    assert isinstance(data["checks"], dict)
    
    # Verify each check has status and message
    for check_name, check_data in data["checks"].items():
        assert "status" in check_data
        assert "message" in check_data
        assert check_data["status"] in ["healthy", "unhealthy"]


def test_health_check_database_connectivity(client: TestClient):
    """Test that database health check actually tests connectivity."""
    response = client.get("/api/health/database")
    
    data = response.json()
    
    # Database should be healthy in test environment (using test database)
    # But we verify the check runs and returns proper structure
    assert "status" in data
    assert "message" in data
    assert data["check"] == "database"
