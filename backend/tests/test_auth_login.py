"""Integration tests for login endpoint."""

import pytest
from fastapi.testclient import TestClient

from domain.models.user import User


def test_login_success(client: TestClient, test_user: User):
    """Test successful login with valid credentials."""
    response = client.post(
        "/api/auth/login",
        json={
            "username": "testuser",
            "password": "testpassword"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert "user" in data
    assert data["user"]["id"] == test_user.id
    assert data["user"]["username"] == "testuser"
    assert data["user"]["email"] == "test@example.com"


def test_login_invalid_password(client: TestClient, test_user: User):
    """Test login with invalid password."""
    response = client.post(
        "/api/auth/login",
        json={
            "username": "testuser",
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == 401
    data = response.json()
    assert "error" in data["detail"]
    assert data["detail"]["error"]["code"] == "INVALID_CREDENTIALS"


def test_login_nonexistent_user(client: TestClient):
    """Test login with non-existent user (should return same generic error)."""
    response = client.post(
        "/api/auth/login",
        json={
            "username": "nonexistent",
            "password": "anypassword"
        }
    )
    
    assert response.status_code == 401
    data = response.json()
    assert "error" in data["detail"]
    assert data["detail"]["error"]["code"] == "INVALID_CREDENTIALS"
