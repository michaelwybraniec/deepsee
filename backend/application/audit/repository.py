"""Audit repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional
from domain.audit.audit_event import AuditEvent


class AuditRepository(ABC):
    """Interface for audit event repository.
    
    This is the port (interface) in Clean Architecture.
    Implementations should be in the infrastructure layer.
    """
    
    @abstractmethod
    def save(self, event: AuditEvent) -> None:
        """Save an audit event to the database."""
        pass
    
    @abstractmethod
    def find_by_action_type(self, action_type: str) -> List[AuditEvent]:
        """Find audit events by action type."""
        pass
    
    @abstractmethod
    def find_by_user_id(self, user_id: int) -> List[AuditEvent]:
        """Find audit events by user ID."""
        pass
    
    @abstractmethod
    def find_by_resource(self, resource_type: str, resource_id: str) -> List[AuditEvent]:
        """Find audit events by resource type and ID."""
        pass
