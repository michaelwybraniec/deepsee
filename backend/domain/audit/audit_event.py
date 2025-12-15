"""Audit event domain entity."""

from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum


class AuditActionType(str, Enum):
    """Audit action types."""
    
    TASK_CREATED = "task_created"
    TASK_UPDATED = "task_updated"
    TASK_DELETED = "task_deleted"
    ATTACHMENT_UPLOADED = "attachment_uploaded"
    ATTACHMENT_DELETED = "attachment_deleted"
    REMINDER_SENT = "reminder_sent"


class AuditEvent:
    """Audit event domain entity.
    
    Represents an immutable audit log entry for tracking key system actions.
    """
    
    def __init__(
        self,
        action_type: str,
        user_id: Optional[int],
        resource_type: str,
        resource_id: str,
        metadata: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
        id: Optional[int] = None
    ):
        """
        Initialize audit event.
        
        Args:
            action_type: Type of action (e.g., "task_created", "attachment_uploaded")
            user_id: ID of user who performed action (None for system actions)
            resource_type: Type of resource affected (e.g., "task", "attachment", "reminder")
            resource_id: ID of the affected resource
            metadata: Additional context (JSON-serializable dict)
            timestamp: When the event occurred (defaults to now)
            id: Database ID (None for new events)
        """
        self.id = id
        self.action_type = action_type
        self.user_id = user_id
        self.resource_type = resource_type
        self.resource_id = resource_id
        self.metadata = metadata or {}
        self.timestamp = timestamp or datetime.utcnow()
    
    def __repr__(self):
        return (
            f"<AuditEvent(id={self.id}, action_type={self.action_type}, "
            f"user_id={self.user_id}, resource_type={self.resource_type}, "
            f"resource_id={self.resource_id}, timestamp={self.timestamp})>"
        )
