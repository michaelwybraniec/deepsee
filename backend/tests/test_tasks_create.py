"""Integration tests for create task endpoint."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import bcrypt
import json

from api.main import app
from infrastructure.database import SessionLocal, engine, Base
from domain.models.user import User
from domain.models.task import Task
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
def db_session():
    """Create test database session."""
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


def test_create_task_success(db_session: Session, test_user: User):
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


def test_create_task_minimal(db_session: Session, test_user: User):
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


def test_create_task_validation_error(db_session: Session, test_user: User):
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


def test_create_task_unauthenticated():
    """Test task creation without authentication."""
    response = client.post(
        "/api/tasks/",
        json={
            "title": "Test Task"
        }
    )
    
    assert response.status_code == 403  # Forbidden (no token provided)
