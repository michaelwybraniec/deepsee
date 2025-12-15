"""Integration tests for read task endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import bcrypt
import json

from api.main import app
from infrastructure.database import SessionLocal, engine, Base
from domain.models.user import User
from domain.models.task import Task

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
def user1(db_session: Session):
    """Create test user 1."""
    hashed_password = bcrypt.hashpw(b"password1", bcrypt.gensalt()).decode('utf-8')
    user = User(
        username="user1",
        email="user1@example.com",
        hashed_password=hashed_password
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def user2(db_session: Session):
    """Create test user 2."""
    hashed_password = bcrypt.hashpw(b"password2", bcrypt.gensalt()).decode('utf-8')
    user = User(
        username="user2",
        email="user2@example.com",
        hashed_password=hashed_password
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def task_user1(db_session: Session, user1: User):
    """Create task owned by user1."""
    task = Task(
        title="User1's Task",
        description="Task description",
        status="todo",
        priority="high",
        owner_user_id=user1.id
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task


def test_get_task_by_id_success(db_session: Session, user2: User, task_user1: Task):
    """Test get single task by ID (user2 can view user1's task)."""
    # Login as user2
    login_response = client.post(
        "/api/auth/login",
        json={
            "username": "user2",
            "password": "password2"
        }
    )
    token = login_response.json()["token"]
    
    # Get task by ID
    response = client.get(
        f"/api/tasks/{task_user1.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_user1.id
    assert data["title"] == "User1's Task"
    assert data["owner_user_id"] == task_user1.owner_user_id


def test_get_task_by_id_not_found(db_session: Session, user1: User):
    """Test get non-existent task."""
    # Login
    login_response = client.post(
        "/api/auth/login",
        json={
            "username": "user1",
            "password": "password1"
        }
    )
    token = login_response.json()["token"]
    
    # Get non-existent task
    response = client.get(
        "/api/tasks/99999",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "error" in data["detail"]
    assert data["detail"]["error"]["code"] == "TASK_NOT_FOUND"


def test_list_tasks_all_visible(db_session: Session, user1: User, user2: User, task_user1: Task):
    """Test list tasks - all users can see all tasks."""
    # Create another task for user2
    task2 = Task(
        title="User2's Task",
        description="Another task",
        status="in_progress",
        priority="low",
        owner_user_id=user2.id
    )
    db_session.add(task2)
    db_session.commit()
    db_session.refresh(task2)
    
    # Login as user1
    login_response = client.post(
        "/api/auth/login",
        json={
            "username": "user1",
            "password": "password1"
        }
    )
    token = login_response.json()["token"]
    
    # List tasks - should see both tasks
    response = client.get(
        "/api/tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    task_ids = [task["id"] for task in data]
    assert task_user1.id in task_ids
    assert task2.id in task_ids


def test_list_tasks_unauthenticated():
    """Test list tasks without authentication."""
    response = client.get("/api/tasks/")
    
    assert response.status_code == 403  # Forbidden (no token provided)
