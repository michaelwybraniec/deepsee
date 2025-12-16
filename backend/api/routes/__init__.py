"""API routes module."""

from . import auth, tasks, attachments, worker, metrics, health

__all__ = ["auth", "tasks", "attachments", "worker", "metrics", "health"]
