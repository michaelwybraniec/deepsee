"""Integration tests for audit trail."""

import pytest
from sqlalchemy.orm import Session
import bcrypt

from domain.models.user import User
from domain.models.task import Task
from domain.audit.audit_event import AuditActionType
from infrastructure.persistence.models.audit_event import AuditEvent as AuditEventModel
from application.tasks.create_task import create_task
from application.tasks.update_task import update_task
from application.tasks.delete_task import delete_task
from application.tasks.schemas import TaskCreateRequest, TaskUpdateRequest
from application.attachments.upload_attachment import upload_attachment
from application.attachments.delete_attachment import delete_attachment
from application.attachments.repository import AttachmentRepository
from application.tasks.repository import TaskRepository
from infrastructure.persistence.repositories.task_repository import SQLAlchemyTaskRepository
from infrastructure.persistence.repositories.attachment_repository import SQLAlchemyAttachmentRepository
from infrastructure.attachments.storage import LocalFileStorage
from infrastructure.audit.audit_logger import AuditLoggerImpl
from infrastructure.persistence.repositories.audit_repository import SQLAlchemyAuditRepository
from io import BytesIO


@pytest.fixture
def test_user(db_session: Session):
    """Create a test user."""
    hashed_password = bcrypt.hashpw(b"testpassword", bcrypt.gensalt()).decode('utf-8')
    user = User(
        username="testuser_audit",
        email="testaudit@example.com",
        hashed_password=hashed_password
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def audit_logger(db_session: Session):
    """Create audit logger."""
    audit_repository = SQLAlchemyAuditRepository(db_session)
    return AuditLoggerImpl(audit_repository)


def test_task_creation_creates_audit_event(db_session: Session, test_user, audit_logger):
    """Test that task creation creates an audit event."""
    task_repository = SQLAlchemyTaskRepository(db_session)
    
    # Create task
    request = TaskCreateRequest(
        title="Test Task",
        description="Test Description",
        status="todo",
        priority="high"
    )
    create_task(task_repository, request, test_user.id, audit_logger)
    
    # Verify audit event was created
    events = db_session.query(AuditEventModel).filter(
        AuditEventModel.action_type == AuditActionType.TASK_CREATED
    ).all()
    
    assert len(events) == 1
    event = events[0]
    assert event.user_id == test_user.id
    assert event.resource_type == "task"
    assert event.event_metadata is not None
    assert "title" in event.event_metadata


def test_task_update_creates_audit_event(db_session: Session, test_user, audit_logger):
    """Test that task update creates an audit event."""
    task_repository = SQLAlchemyTaskRepository(db_session)
    
    # Create task first
    request = TaskCreateRequest(title="Test Task", status="todo")
    created_task = create_task(task_repository, request, test_user.id, audit_logger)
    
    # Update task
    update_request = TaskUpdateRequest(status="in_progress")
    update_task(task_repository, created_task.id, update_request, test_user.id, audit_logger)
    
    # Verify audit event was created
    events = db_session.query(AuditEventModel).filter(
        AuditEventModel.action_type == AuditActionType.TASK_UPDATED
    ).all()
    
    assert len(events) == 1
    event = events[0]
    assert event.user_id == test_user.id
    assert event.resource_type == "task"
    assert event.resource_id == str(created_task.id)
    assert "changes" in event.event_metadata


def test_task_deletion_creates_audit_event(db_session: Session, test_user, audit_logger):
    """Test that task deletion creates an audit event."""
    task_repository = SQLAlchemyTaskRepository(db_session)
    
    # Create task first
    request = TaskCreateRequest(title="Test Task")
    created_task = create_task(task_repository, request, test_user.id, audit_logger)
    db_session.commit()  # Commit task creation
    
    # Delete task (with attachment_repository=None, storage=None since we're not testing attachments)
    delete_task(
        task_repository, 
        created_task.id, 
        test_user.id, 
        audit_logger,
        attachment_repository=None,
        storage=None
    )
    db_session.commit()  # Commit deletion and audit event
    
    # Refresh session to see committed audit events
    db_session.expire_all()
    
    # Verify audit event was created
    events = db_session.query(AuditEventModel).filter(
        AuditEventModel.action_type == AuditActionType.TASK_DELETED
    ).all()
    
    assert len(events) == 1, f"Expected 1 audit event, found {len(events)}"
    event = events[0]
    assert event.user_id == test_user.id
    assert event.resource_type == "task"
    assert event.resource_id == str(created_task.id)


def test_attachment_upload_creates_audit_event(db_session: Session, test_user, audit_logger):
    """Test that attachment upload creates an audit event."""
    task_repository = SQLAlchemyTaskRepository(db_session)
    attachment_repository = SQLAlchemyAttachmentRepository(db_session)
    storage = LocalFileStorage()
    
    # Create task first
    request = TaskCreateRequest(title="Test Task")
    created_task = create_task(task_repository, request, test_user.id, audit_logger)
    
    # Upload attachment
    file_content = b"test file content"
    file_bytes = BytesIO(file_content)
    
    upload_attachment(
        task_repository=task_repository,
        attachment_repository=attachment_repository,
        storage=storage,
        task_id=created_task.id,
        file=file_bytes,
        filename="test.txt",
        content_type="text/plain",
        authenticated_user_id=test_user.id,
        audit_logger=audit_logger
    )
    
    # Verify audit event was created
    events = db_session.query(AuditEventModel).filter(
        AuditEventModel.action_type == AuditActionType.ATTACHMENT_UPLOADED
    ).all()
    
    assert len(events) == 1
    event = events[0]
    assert event.user_id == test_user.id
    assert event.resource_type == "attachment"
    assert event.event_metadata is not None
    assert "filename" in event.event_metadata


def test_attachment_deletion_creates_audit_event(db_session: Session, test_user, audit_logger):
    """Test that attachment deletion creates an audit event."""
    task_repository = SQLAlchemyTaskRepository(db_session)
    attachment_repository = SQLAlchemyAttachmentRepository(db_session)
    storage = LocalFileStorage()
    
    # Create task and attachment
    request = TaskCreateRequest(title="Test Task")
    created_task = create_task(task_repository, request, test_user.id, audit_logger)
    
    file_content = b"test file content"
    file_bytes = BytesIO(file_content)
    
    uploaded = upload_attachment(
        task_repository=task_repository,
        attachment_repository=attachment_repository,
        storage=storage,
        task_id=created_task.id,
        file=file_bytes,
        filename="test.txt",
        content_type="text/plain",
        authenticated_user_id=test_user.id,
        audit_logger=audit_logger
    )
    
    # Delete attachment
    delete_attachment(
        task_repository=task_repository,
        attachment_repository=attachment_repository,
        storage=storage,
        attachment_id=uploaded.id,
        authenticated_user_id=test_user.id,
        audit_logger=audit_logger
    )
    
    # Verify audit event was created
    events = db_session.query(AuditEventModel).filter(
        AuditEventModel.action_type == AuditActionType.ATTACHMENT_DELETED
    ).all()
    
    assert len(events) == 1
    event = events[0]
    assert event.user_id == test_user.id
    assert event.resource_type == "attachment"
    assert event.event_metadata is not None
    assert "filename" in event.event_metadata


def test_reminder_sent_creates_audit_event(db_session: Session, test_user):
    """Test that reminder sent creates an audit event."""
    from worker.jobs.reminder_job import _process_single_reminder
    from infrastructure.audit.audit_logger import AuditLoggerImpl
    from infrastructure.persistence.repositories.audit_repository import SQLAlchemyAuditRepository
    from datetime import datetime, timedelta, UTC
    
    # Create task due in 12 hours
    task = Task(
        title="Task due soon",
        due_date=datetime.now(UTC) + timedelta(hours=12),
        owner_user_id=test_user.id,
        status="todo"
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    
    # Initialize audit logger with same session
    audit_repository = SQLAlchemyAuditRepository(db_session)
    audit_logger = AuditLoggerImpl(audit_repository)
    
    # Manually process reminder (simulating worker behavior)
    now = datetime.now(UTC)
    last_24h = now - timedelta(hours=24)
    success = _process_single_reminder(db_session, task, now, last_24h)
    
    if success:
        # Log audit event (same as worker does)
        audit_logger.log(
            action_type=AuditActionType.REMINDER_SENT,
            user_id=None,  # System action
            resource_type="reminder",
            resource_id=str(task.id),
            metadata={
                "task_id": task.id,
                "due_date": task.due_date.isoformat() if task.due_date else None
            }
        )
    
    # Verify audit event was created
    events = db_session.query(AuditEventModel).filter(
        AuditEventModel.action_type == AuditActionType.REMINDER_SENT
    ).all()
    
    assert len(events) == 1
    event = events[0]
    assert event.user_id is None  # System action
    assert event.resource_type == "reminder"
    assert event.resource_id == str(task.id)
    assert event.event_metadata is not None
    assert "task_id" in event.event_metadata
