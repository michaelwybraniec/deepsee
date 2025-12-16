"""Task repository implementation (SQLAlchemy)."""

from typing import Optional, List
from sqlalchemy.orm import Session, joinedload

from domain.models.task import Task
from application.tasks.repository import TaskRepository
import json


class SQLAlchemyTaskRepository(TaskRepository):
    """SQLAlchemy implementation of TaskRepository."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, task: Task) -> Task:
        """Create a new task."""
        # Convert tags list to JSON string if provided
        if task.tags and isinstance(task.tags, list):
            task.tags = json.dumps(task.tags)
        elif task.tags is None:
            task.tags = None
        
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Get task by ID."""
        task = self.db.query(Task).options(joinedload(Task.owner)).filter(Task.id == task_id).first()
        return task
    
    def get_all(self) -> List[Task]:
        """Get all tasks (no ownership filter for reads)."""
        tasks = self.db.query(Task).options(joinedload(Task.owner)).all()
        return tasks
    
    def update(self, task: Task) -> Task:
        """Update an existing task."""
        # Convert tags list to JSON string if provided
        if task.tags and isinstance(task.tags, list):
            task.tags = json.dumps(task.tags)
        
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def delete(self, task_id: int) -> bool:
        """Delete a task by ID."""
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if task:
            self.db.delete(task)
            self.db.commit()
            return True
        return False
