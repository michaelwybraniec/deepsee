"""Local filesystem attachment storage implementation.

This implementation stores files on the local filesystem in a structured directory:
backend/uploads/{task_id}/{filename}

Design Decision: Local filesystem chosen for simplicity in development.
For production, consider switching to object storage (S3, MinIO) by implementing
a different AttachmentStorage adapter.
"""

import os
import shutil
from pathlib import Path
from typing import BinaryIO, Optional

from application.attachments.storage_interface import AttachmentStorage


class LocalFileStorage(AttachmentStorage):
    """Local filesystem implementation of AttachmentStorage."""
    
    def __init__(self, base_path: str = "backend/uploads"):
        """
        Initialize local file storage.
        
        Args:
            base_path: Base directory for storing uploads (relative to project root)
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def save(self, file: BinaryIO, task_id: int, filename: str) -> str:
        """
        Save a file to local filesystem.
        
        Files are stored in: {base_path}/{task_id}/{filename}
        """
        # Create task-specific directory
        task_dir = self.base_path / str(task_id)
        task_dir.mkdir(parents=True, exist_ok=True)
        
        # Full path to file
        file_path = task_dir / filename
        
        # Save file
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file, f)
        
        # Return relative path for storage in database
        return str(file_path.relative_to(self.base_path.parent))
    
    def get_url(self, storage_path: str) -> Optional[str]:
        """
        Get file path for local filesystem storage.
        
        Returns absolute path to file.
        """
        # Reconstruct full path
        full_path = self.base_path.parent / storage_path
        
        if full_path.exists():
            return str(full_path.absolute())
        return None
    
    def delete(self, storage_path: str) -> bool:
        """
        Delete a file from local filesystem.
        """
        # Reconstruct full path
        full_path = self.base_path.parent / storage_path
        
        if full_path.exists():
            full_path.unlink()
            return True
        return False
    
    def exists(self, storage_path: str) -> bool:
        """
        Check if a file exists in local filesystem.
        """
        full_path = self.base_path.parent / storage_path
        return full_path.exists()
