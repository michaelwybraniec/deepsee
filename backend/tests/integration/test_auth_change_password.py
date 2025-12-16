"""Integration tests for change password endpoint."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import bcrypt

from domain.models.user import User


@pytest.fixture
def test_user_with_old_password(db_session: Session):
    """Create test user with old password."""
    hashed_password = bcrypt.hashpw(b"oldpassword", bcrypt.gensalt()).decode('utf-8')
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hashed_password
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def test_change_password_success(client: TestClient, test_user_with_old_password: User):
    """Test successful password change."""
    # Login to get token
    login_response = client.post(
        "/api/auth/login",
        json={
            "username": "testuser",
            "password": "oldpassword"
        }
    )
    token = login_response.json()["token"]
    
    # Change password
    response = client.post(
        "/api/auth/change-password",
        json={
            "current_password": "oldpassword",
            "new_password": "newpassword123"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Password changed successfully"
    
    # Verify new password works
    login_response = client.post(
        "/api/auth/login",
        json={
            "username": "testuser",
            "password": "newpassword123"
        }
    )
    assert login_response.status_code == 200


def test_change_password_wrong_current_password(client: TestClient, test_user_with_old_password: User):
    """Test change password with wrong current password."""
    # Login to get token
    login_response = client.post(
        "/api/auth/login",
        json={
            "username": "testuser",
            "password": "oldpassword"
        }
    )
    token = login_response.json()["token"]
    
    # Try to change password with wrong current password
    response = client.post(
        "/api/auth/change-password",
        json={
            "current_password": "wrongpassword",
            "new_password": "newpassword123"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 401
    data = response.json()
    assert "error" in data["detail"]
    assert data["detail"]["error"]["code"] == "INVALID_CURRENT_PASSWORD"


def test_change_password_unauthenticated(client: TestClient):
    """Test change password without authentication."""
    response = client.post(
        "/api/auth/change-password",
        json={
            "current_password": "oldpassword",
            "new_password": "newpassword123"
        }
    )
    
    assert response.status_code in [401, 403]  # Unauthorized or Forbidden (no token provided)
