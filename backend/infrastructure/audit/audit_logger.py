"""Audit logger implementation (adapter in Clean Architecture)."""

import logging
from typing import Optional, Dict, Any

from application.audit.audit_logger import AuditLogger
from application.audit.repository import AuditRepository
from domain.audit.audit_event import AuditEvent

logger = logging.getLogger(__name__)


class AuditLoggerImpl(AuditLogger):
    """Implementation of audit logger.
    
    This is the adapter in Clean Architecture.
    Handles persistence of audit events via repository.
    """
    
    def __init__(self, repository: AuditRepository):
        """Initialize audit logger with repository."""
        self.repository = repository
    
    def log(
        self,
        action_type: str,
        user_id: Optional[int],
        resource_type: str,
        resource_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Log an audit event.
        
        Handles errors gracefully - audit logging failures should not break main operations.
        """
        try:
            # Create domain entity
            event = AuditEvent(
                action_type=action_type,
                user_id=user_id,
                resource_type=resource_type,
                resource_id=str(resource_id),
                metadata=metadata or {}
            )
            
            # Persist via repository
            self.repository.save(event)
            
            logger.debug(
                f"Audit event logged: {action_type} for {resource_type}:{resource_id} "
                f"by user {user_id}"
            )
            
        except Exception as e:
            # Log error but don't throw - audit should not break main flow
            logger.error(
                f"Failed to log audit event: {action_type} for {resource_type}:{resource_id}. "
                f"Error: {str(e)}",
                exc_info=True
            )
            # Continue - don't raise exception
