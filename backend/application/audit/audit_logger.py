"""Audit logger interface (port in Clean Architecture)."""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class AuditLogger(ABC):
    """Interface for audit logging service.
    
    This is the port (interface) in Clean Architecture.
    Implementations should be in the infrastructure layer.
    """
    
    @abstractmethod
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
        
        Args:
            action_type: Type of action (e.g., "task_created", "attachment_uploaded")
            user_id: ID of user who performed action (None for system actions)
            resource_type: Type of resource (e.g., "task", "attachment", "reminder")
            resource_id: ID of the affected resource
            metadata: Additional context (JSON-serializable dict)
        
        Note: This method should handle errors gracefully and not throw exceptions
        that would break the main operation flow.
        """
        pass
