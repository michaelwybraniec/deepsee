"""Local filesystem attachment storage implementation.

This implementation stores files on the local filesystem in a structured directory:
uploads/{task_id}/{filename}

Design Decision: Local filesystem chosen for simplicity in development.
For production, consider switching to object storage (S3, MinIO) by implementing
a different AttachmentStorage adapter.

Docker Space Optimization:
- Uses absolute path based on file location to work consistently in Docker and local
- In Docker: uploads stored in named volume (uploads_data:/app/uploads) not bind mount
- This prevents uploads from syncing to host filesystem, saving space and improving performance
"""

import os
import shutil
from pathlib import Path
from typing import BinaryIO, Optional

from application.attachments.storage_interface import AttachmentStorage


def _get_uploads_path() -> Path:
    """
    Get absolute path to uploads directory.
    
    Resolves path relative to this file's location:
    - In Docker: /app/uploads (working dir is /app)
    - Locally: {project_root}/backend/uploads (if run from project root)
    - Locally: {backend_dir}/uploads (if run from backend directory)
    """
    # Get directory where this file is located
    current_file = Path(__file__).resolve()
    # Go up: infrastructure/attachments/storage.py -> infrastructure/attachments -> infrastructure -> backend
    backend_dir = current_file.parent.parent.parent
    
    # Use 'uploads' directory relative to backend directory
    # This works in both Docker (/app/uploads) and local (backend/uploads)
    uploads_path = backend_dir / "uploads"
    return uploads_path.resolve()


class LocalFileStorage(AttachmentStorage):
    """Local filesystem implementation of AttachmentStorage."""
    
    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize local file storage.
        
        Args:
            base_path: Optional base directory for storing uploads.
                      If None, uses absolute path based on file location.
                      This ensures consistent behavior in Docker and local environments.
        """
        if base_path is None:
            self.base_path = _get_uploads_path()
        else:
            self.base_path = Path(base_path).resolve()
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def save(self, file: BinaryIO, task_id: int, filename: str) -> str:
        """
        Save a file to local filesystem.
        
        Files are stored in: {base_path}/{task_id}/{filename}
        
        Returns: Relative path from base_path (e.g., "208/filename.png")
        """
        # Create task-specific directory
        task_dir = self.base_path / str(task_id)
        task_dir.mkdir(parents=True, exist_ok=True)
        
        # Full path to file
        file_path = task_dir / filename
        
        # Save file
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file, f)
        
        # Return relative path for storage in database (relative to base_path)
        return str(file_path.relative_to(self.base_path))
    
    def get_url(self, storage_path: str) -> Optional[str]:
        """
        Get file path for local filesystem storage.
        
        Args:
            storage_path: Relative path from base_path (e.g., "208/filename.png")
        
        Returns: Absolute path to file.
        """
        # Reconstruct full path (storage_path is relative to base_path)
        full_path = self.base_path / storage_path
        
        if full_path.exists():
            return str(full_path.absolute())
        return None
    
    def delete(self, storage_path: str) -> bool:
        """
        Delete a file from local filesystem.
        
        Args:
            storage_path: Relative path from base_path (e.g., "208/filename.png")
        """
        # Reconstruct full path (storage_path is relative to base_path)
        full_path = self.base_path / storage_path
        
        if full_path.exists():
            full_path.unlink()
            return True
        return False
    
    def exists(self, storage_path: str) -> bool:
        """
        Check if a file exists in local filesystem.
        
        Args:
            storage_path: Relative path from base_path (e.g., "208/filename.png")
        """
        full_path = self.base_path / storage_path
        return full_path.exists()
