"""API routes module."""

from . import auth, tasks, attachments, worker

__all__ = ["auth", "tasks", "attachments", "worker"]
