"""Integration tests for create task endpoint."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from domain.models.user import User


def test_create_task_success(client: TestClient, test_user: User):
    """Test successful task creation with all fields."""
    # Login to get token
    login_response = client.post(
        "/api/auth/login",
        json={
            "username": "testuser",
            "password": "testpassword"
        }
    )
    token = login_response.json()["token"]
    
    # Create task
    response = client.post(
        "/api/tasks/",
        json={
            "title": "Test Task",
            "description": "Test description",
            "status": "todo",
            "priority": "high",
            "due_date": "2024-12-31T00:00:00",
            "tags": ["tag1", "tag2"]
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test description"
    assert data["status"] == "todo"
    assert data["priority"] == "high"
    assert data["tags"] == ["tag1", "tag2"]
    assert data["owner_user_id"] == test_user.id
    assert "id" in data
    assert "created_at" in data


def test_create_task_minimal(client: TestClient, test_user: User):
    """Test task creation with minimal fields (title only)."""
    # Login to get token
    login_response = client.post(
        "/api/auth/login",
        json={
            "username": "testuser",
            "password": "testpassword"
        }
    )
    token = login_response.json()["token"]
    
    # Create task with only title
    response = client.post(
        "/api/tasks/",
        json={
            "title": "Minimal Task"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Minimal Task"
    assert data["owner_user_id"] == test_user.id


def test_create_task_validation_error(client: TestClient, test_user: User):
    """Test task creation with validation error (empty title)."""
    # Login to get token
    login_response = client.post(
        "/api/auth/login",
        json={
            "username": "testuser",
            "password": "testpassword"
        }
    )
    token = login_response.json()["token"]
    
    # Try to create task with empty title
    response = client.post(
        "/api/tasks/",
        json={
            "title": ""
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 422  # Pydantic validation error


def test_create_task_unauthenticated(client: TestClient):
    """Test task creation without authentication."""
    response = client.post(
        "/api/tasks/",
        json={
            "title": "Test Task"
        }
    )
    
    assert response.status_code in [401, 403]  # Unauthorized or Forbidden (no token provided)
