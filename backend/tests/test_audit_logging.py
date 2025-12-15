"""Tests for audit logging service."""

import pytest
from datetime import datetime
from sqlalchemy.orm import Session

from domain.audit.audit_event import AuditEvent, AuditActionType
from application.audit.audit_logger import AuditLogger
from application.audit.repository import AuditRepository
from infrastructure.audit.audit_logger import AuditLoggerImpl
from infrastructure.persistence.repositories.audit_repository import SQLAlchemyAuditRepository
from infrastructure.persistence.models.audit_event import AuditEvent as AuditEventModel


@pytest.fixture
def audit_repository(db_session: Session) -> AuditRepository:
    """Create audit repository."""
    return SQLAlchemyAuditRepository(db_session)


@pytest.fixture
def audit_logger(audit_repository: AuditRepository) -> AuditLogger:
    """Create audit logger."""
    return AuditLoggerImpl(audit_repository)


def test_audit_logger_logs_event(db_session: Session, audit_logger: AuditLogger):
    """Test that audit logger logs events correctly."""
    # Log an event
    audit_logger.log(
        action_type=AuditActionType.TASK_CREATED,
        user_id=1,
        resource_type="task",
        resource_id="123",
        metadata={"title": "Test Task", "status": "todo"}
    )
    
    # Verify event was persisted
    events = db_session.query(AuditEventModel).all()
    assert len(events) == 1
    
    event = events[0]
    assert event.action_type == AuditActionType.TASK_CREATED
    assert event.user_id == 1
    assert event.resource_type == "task"
    assert event.resource_id == "123"
    assert event.metadata == {"title": "Test Task", "status": "todo"}
    assert event.timestamp is not None


def test_audit_logger_logs_system_action(db_session: Session, audit_logger: AuditLogger):
    """Test that audit logger logs system actions (user_id=None)."""
    # Log a system action (reminder sent)
    audit_logger.log(
        action_type=AuditActionType.REMINDER_SENT,
        user_id=None,
        resource_type="reminder",
        resource_id="123",
        metadata={"task_id": 123, "due_date": "2024-01-15T10:00:00Z"}
    )
    
    # Verify event was persisted with user_id=None
    events = db_session.query(AuditEventModel).all()
    assert len(events) == 1
    
    event = events[0]
    assert event.action_type == AuditActionType.REMINDER_SENT
    assert event.user_id is None
    assert event.resource_type == "reminder"
    assert event.resource_id == "123"


def test_audit_logger_handles_errors_gracefully(db_session: Session):
    """Test that audit logger handles errors gracefully."""
    # Create a logger with a repository that will fail
    class FailingRepository(AuditRepository):
        def save(self, event: AuditEvent) -> None:
            raise Exception("Database error")
        
        def find_by_action_type(self, action_type: str):
            return []
        
        def find_by_user_id(self, user_id: int):
            return []
        
        def find_by_resource(self, resource_type: str, resource_id: str):
            return []
    
    failing_repo = FailingRepository()
    audit_logger = AuditLoggerImpl(failing_repo)
    
    # Logging should not throw exception
    try:
        audit_logger.log(
            action_type=AuditActionType.TASK_CREATED,
            user_id=1,
            resource_type="task",
            resource_id="123"
        )
    except Exception:
        pytest.fail("Audit logger should handle errors gracefully and not throw")


def test_audit_repository_find_by_action_type(db_session: Session, audit_repository: AuditRepository):
    """Test finding audit events by action type."""
    # Create some events
    event1 = AuditEvent(
        action_type=AuditActionType.TASK_CREATED,
        user_id=1,
        resource_type="task",
        resource_id="1"
    )
    event2 = AuditEvent(
        action_type=AuditActionType.TASK_UPDATED,
        user_id=1,
        resource_type="task",
        resource_id="1"
    )
    event3 = AuditEvent(
        action_type=AuditActionType.TASK_CREATED,
        user_id=2,
        resource_type="task",
        resource_id="2"
    )
    
    audit_repository.save(event1)
    audit_repository.save(event2)
    audit_repository.save(event3)
    
    # Find by action type
    created_events = audit_repository.find_by_action_type(AuditActionType.TASK_CREATED)
    assert len(created_events) == 2
    assert all(e.action_type == AuditActionType.TASK_CREATED for e in created_events)


def test_audit_repository_find_by_user_id(db_session: Session, audit_repository: AuditRepository):
    """Test finding audit events by user ID."""
    # Create events for different users
    event1 = AuditEvent(
        action_type=AuditActionType.TASK_CREATED,
        user_id=1,
        resource_type="task",
        resource_id="1"
    )
    event2 = AuditEvent(
        action_type=AuditActionType.TASK_CREATED,
        user_id=2,
        resource_type="task",
        resource_id="2"
    )
    
    audit_repository.save(event1)
    audit_repository.save(event2)
    
    # Find by user ID
    user1_events = audit_repository.find_by_user_id(1)
    assert len(user1_events) == 1
    assert user1_events[0].user_id == 1


def test_audit_repository_find_by_resource(db_session: Session, audit_repository: AuditRepository):
    """Test finding audit events by resource."""
    # Create events for different resources
    event1 = AuditEvent(
        action_type=AuditActionType.TASK_CREATED,
        user_id=1,
        resource_type="task",
        resource_id="123"
    )
    event2 = AuditEvent(
        action_type=AuditActionType.TASK_UPDATED,
        user_id=1,
        resource_type="task",
        resource_id="123"
    )
    event3 = AuditEvent(
        action_type=AuditActionType.TASK_CREATED,
        user_id=1,
        resource_type="task",
        resource_id="456"
    )
    
    audit_repository.save(event1)
    audit_repository.save(event2)
    audit_repository.save(event3)
    
    # Find by resource
    task123_events = audit_repository.find_by_resource("task", "123")
    assert len(task123_events) == 2
    assert all(e.resource_id == "123" for e in task123_events)
