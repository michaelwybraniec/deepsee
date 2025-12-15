"""Attachment storage interface (Clean Architecture port).

This interface abstracts file storage operations, allowing different storage
backends (filesystem, S3, etc.) to be swapped without changing business logic.
"""

from abc import ABC, abstractmethod
from typing import BinaryIO, Optional


class AttachmentStorage(ABC):
    """Interface for attachment file storage operations."""
    
    @abstractmethod
    def save(self, file: BinaryIO, task_id: int, filename: str) -> str:
        """
        Save a file to storage.
        
        Args:
            file: File-like object (bytes) to save
            task_id: ID of the task this attachment belongs to
            filename: Sanitized filename
        
        Returns:
            storage_path: Path or key where file was stored (for retrieval/deletion)
        
        Raises:
            StorageError: If file cannot be saved
        """
        pass
    
    @abstractmethod
    def get_url(self, storage_path: str) -> Optional[str]:
        """
        Get URL or path to access a stored file.
        
        Args:
            storage_path: Path/key returned from save()
        
        Returns:
            URL or file path, or None if file doesn't exist
        """
        pass
    
    @abstractmethod
    def delete(self, storage_path: str) -> bool:
        """
        Delete a file from storage.
        
        Args:
            storage_path: Path/key returned from save()
        
        Returns:
            True if file was deleted, False if file doesn't exist
        
        Raises:
            StorageError: If file cannot be deleted
        """
        pass
    
    @abstractmethod
    def exists(self, storage_path: str) -> bool:
        """
        Check if a file exists in storage.
        
        Args:
            storage_path: Path/key to check
        
        Returns:
            True if file exists, False otherwise
        """
        pass
