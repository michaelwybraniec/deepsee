"""Integration tests for update and delete task endpoints."""

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
        description="Original description",
        status="todo",
        priority="high",
        owner_user_id=user1.id
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task


def test_update_task_owner_success(client: TestClient, user1: User, task_user1: Task):
    """Test owner can update their task."""
    # Login as user1
    login_response = client.post(
        "/api/auth/login",
        json={
            "username": "user1",
            "password": "password1"
        }
    )
    token = login_response.json()["token"]
    
    # Update task
    response = client.put(
        f"/api/tasks/{task_user1.id}",
        json={
            "title": "Updated Title",
            "description": "Updated description",
            "status": "in_progress"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated description"
    assert data["status"] == "in_progress"
    assert data["id"] == task_user1.id


def test_update_task_non_owner_forbidden(client: TestClient, user2: User, task_user1: Task):
    """Test non-owner cannot update task."""
    # Login as user2
    login_response = client.post(
        "/api/auth/login",
        json={
            "username": "user2",
            "password": "password2"
        }
    )
    token = login_response.json()["token"]
    
    # Try to update user1's task
    response = client.put(
        f"/api/tasks/{task_user1.id}",
        json={
            "title": "Hacked Title"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 403
    data = response.json()
    assert "error" in data["detail"]
    assert data["detail"]["error"]["code"] == "FORBIDDEN"


def test_delete_task_owner_success(client: TestClient, user1: User, task_user1: Task):
    """Test owner can delete their task."""
    # Login as user1
    login_response = client.post(
        "/api/auth/login",
        json={
            "username": "user1",
            "password": "password1"
        }
    )
    token = login_response.json()["token"]
    
    # Delete task
    response = client.delete(
        f"/api/tasks/{task_user1.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 204
    
    # Verify task is deleted
    get_response = client.get(
        f"/api/tasks/{task_user1.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_response.status_code == 404


def test_delete_task_non_owner_forbidden(client: TestClient, db_session: Session, user1: User, user2: User):
    """Test non-owner cannot delete task."""
    # Create task for user1
    task = Task(
        title="User1's Task",
        description="Description",
        owner_user_id=user1.id
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    
    # Login as user2
    login_response = client.post(
        "/api/auth/login",
        json={
            "username": "user2",
            "password": "password2"
        }
    )
    token = login_response.json()["token"]
    
    # Try to delete user1's task
    response = client.delete(
        f"/api/tasks/{task.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 403
    data = response.json()
    assert "error" in data["detail"]
    assert data["detail"]["error"]["code"] == "FORBIDDEN"


def test_update_task_not_found(client: TestClient, user1: User):
    """Test update non-existent task."""
    # Login
    login_response = client.post(
        "/api/auth/login",
        json={
            "username": "user1",
            "password": "password1"
        }
    )
    token = login_response.json()["token"]
    
    # Update non-existent task
    response = client.put(
        "/api/tasks/99999",
        json={"title": "New Title"},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 404


def test_delete_task_not_found(client: TestClient, user1: User):
    """Test delete non-existent task."""
    # Login
    login_response = client.post(
        "/api/auth/login",
        json={
            "username": "user1",
            "password": "password1"
        }
    )
    token = login_response.json()["token"]
    
    # Delete non-existent task
    response = client.delete(
        "/api/tasks/99999",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 404
