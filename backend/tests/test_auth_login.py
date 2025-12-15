"""Integration tests for login endpoint."""

import pytest
from fastapi.testclient import TestClient
from fastapi import Depends
from sqlalchemy.orm import Session
import bcrypt

from api.main import app
from infrastructure.database import get_db, init_db, SessionLocal, engine, Base
from domain.models.user import User

# Create test database
Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture
def db_session():
    """Create test database session."""
    init_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def test_user(db_session: Session):
    """Create test user."""
    hashed_password = bcrypt.hashpw(b"testpassword", bcrypt.gensalt()).decode('utf-8')
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hashed_password
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def test_login_success(db_session: Session, test_user: User):
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


def test_login_invalid_password(db_session: Session, test_user: User):
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


def test_login_nonexistent_user():
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
