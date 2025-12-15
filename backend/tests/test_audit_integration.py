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
    assert event.metadata is not None
    assert "title" in event.metadata


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
    assert "changes" in event.metadata


def test_task_deletion_creates_audit_event(db_session: Session, test_user, audit_logger):
    """Test that task deletion creates an audit event."""
    task_repository = SQLAlchemyTaskRepository(db_session)
    
    # Create task first
    request = TaskCreateRequest(title="Test Task")
    created_task = create_task(task_repository, request, test_user.id, audit_logger)
    
    # Delete task
    delete_task(task_repository, created_task.id, test_user.id, audit_logger)
    
    # Verify audit event was created
    events = db_session.query(AuditEventModel).filter(
        AuditEventModel.action_type == AuditActionType.TASK_DELETED
    ).all()
    
    assert len(events) == 1
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
    assert "filename" in event.metadata


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
    assert "filename" in event.metadata


def test_reminder_sent_creates_audit_event(db_session: Session, test_user):
    """Test that reminder sent creates an audit event."""
    from worker.jobs.reminder_job import process_reminders
    from datetime import datetime, timedelta
    
    # Create task due in 12 hours
    task = Task(
        title="Task due soon",
        due_date=datetime.utcnow() + timedelta(hours=12),
        owner_user_id=test_user.id,
        status="todo"
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    
    # Run reminder worker
    process_reminders()
    
    # Verify audit event was created
    events = db_session.query(AuditEventModel).filter(
        AuditEventModel.action_type == AuditActionType.REMINDER_SENT
    ).all()
    
    assert len(events) == 1
    event = events[0]
    assert event.user_id is None  # System action
    assert event.resource_type == "reminder"
    assert event.resource_id == str(task.id)
    assert "task_id" in event.metadata
