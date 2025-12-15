"""Get task by ID use case."""

from typing import Optional
import json

from domain.models.task import Task
from application.tasks.schemas import TaskResponse
from application.tasks.repository import TaskRepository


def get_task_by_id(
    repository: TaskRepository,
    task_id: int
) -> Optional[TaskResponse]:
    """
    Get a single task by ID.
    
    All authenticated users can view all tasks (no ownership filter for reads).
    
    Args:
        repository: Task repository interface
        task_id: ID of the task to retrieve
    
    Returns:
        TaskResponse if task exists, None otherwise
    """
    task = repository.get_by_id(task_id)
    
    if not task:
        return None
    
    # Convert tags JSON string back to list for response
    tags_list = None
    if task.tags:
        try:
            tags_list = json.loads(task.tags)
        except (json.JSONDecodeError, TypeError):
            tags_list = []
    
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        tags=tags_list,
        owner_user_id=task.owner_user_id,
        created_at=task.created_at,
        updated_at=task.updated_at
    )
