"""Audit repository implementation (SQLAlchemy)."""

from typing import List
from sqlalchemy.orm import Session

from domain.audit.audit_event import AuditEvent
from application.audit.repository import AuditRepository
from infrastructure.persistence.models.audit_event import AuditEvent as AuditEventModel


class SQLAlchemyAuditRepository(AuditRepository):
    """SQLAlchemy implementation of AuditRepository."""
    
    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db
    
    def save(self, event: AuditEvent) -> None:
        """Save an audit event to the database."""
        audit_model = AuditEventModel(
            action_type=event.action_type,
            user_id=event.user_id,
            resource_type=event.resource_type,
            resource_id=str(event.resource_id),
            metadata=event.metadata,
            timestamp=event.timestamp
        )
        
        self.db.add(audit_model)
        self.db.commit()
        self.db.refresh(audit_model)
        
        # Update domain entity with database ID
        event.id = audit_model.id
    
    def find_by_action_type(self, action_type: str) -> List[AuditEvent]:
        """Find audit events by action type."""
        models = self.db.query(AuditEventModel).filter(
            AuditEventModel.action_type == action_type
        ).order_by(AuditEventModel.timestamp.desc()).all()
        
        return [self._to_domain_event(model) for model in models]
    
    def find_by_user_id(self, user_id: int) -> List[AuditEvent]:
        """Find audit events by user ID."""
        models = self.db.query(AuditEventModel).filter(
            AuditEventModel.user_id == user_id
        ).order_by(AuditEventModel.timestamp.desc()).all()
        
        return [self._to_domain_event(model) for model in models]
    
    def find_by_resource(self, resource_type: str, resource_id: str) -> List[AuditEvent]:
        """Find audit events by resource type and ID."""
        models = self.db.query(AuditEventModel).filter(
            AuditEventModel.resource_type == resource_type,
            AuditEventModel.resource_id == str(resource_id)
        ).order_by(AuditEventModel.timestamp.desc()).all()
        
        return [self._to_domain_event(model) for model in models]
    
    def _to_domain_event(self, model: AuditEventModel) -> AuditEvent:
        """Convert ORM model to domain entity."""
        return AuditEvent(
            id=model.id,
            action_type=model.action_type,
            user_id=model.user_id,
            resource_type=model.resource_type,
            resource_id=model.resource_id,
            metadata=model.metadata or {},
            timestamp=model.timestamp
        )
