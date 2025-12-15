"""Integration tests for change password endpoint."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import bcrypt

from api.main import app
from infrastructure.database import SessionLocal, engine, Base
from domain.models.user import User
from application.auth.login import create_access_token

# Create test database
Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides = {}
from infrastructure.database import get_db
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture
def test_user(db_session: Session):
    """Create test user."""
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


@pytest.fixture
def db_session():
    """Create test database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_change_password_success(db_session: Session, test_user: User):
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


def test_change_password_wrong_current_password(db_session: Session, test_user: User):
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


def test_change_password_unauthenticated():
    """Test change password without authentication."""
    response = client.post(
        "/api/auth/change-password",
        json={
            "current_password": "oldpassword",
            "new_password": "newpassword123"
        }
    )
    
    assert response.status_code == 403  # Forbidden (no token provided)
