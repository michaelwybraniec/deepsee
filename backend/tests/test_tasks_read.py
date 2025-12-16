"""Integration tests for read task endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from domain.models.user import User
from domain.models.task import Task


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


def test_get_task_by_id_success(client: TestClient, user2: User, task_user1: Task):
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


def test_get_task_by_id_not_found(client: TestClient, user1: User):
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


def test_list_tasks_all_visible(client: TestClient, db_session: Session, user1: User, user2: User, task_user1: Task):
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
    assert len(data["tasks"]) >= 2
    task_ids = [task["id"] for task in data["tasks"]]
    assert task_user1.id in task_ids
    assert task2.id in task_ids


def test_list_tasks_unauthenticated(client: TestClient):
    """Test list tasks without authentication."""
    response = client.get("/api/tasks/")
    
    assert response.status_code in [401, 403]  # Unauthorized or Forbidden (no token provided)
