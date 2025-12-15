"""
Application configuration module.

Handles application-level configuration like version, author, and metadata.
"""

import os


class AppConfig:
    """Application configuration."""
    
    # API Metadata
    API_VERSION: str = os.getenv("API_VERSION", "1.0.0")
    API_TITLE: str = os.getenv("API_TITLE", "Task Tracker API")
    API_AUTHOR: str = os.getenv("API_AUTHOR", "Michael Wybraniec (ONE-FRONT)")
    API_DESCRIPTION: str = os.getenv(
        "API_DESCRIPTION",
        """Task Tracker API - Enterprise-grade task management system.

A comprehensive RESTful API for secure task management with advanced features including authentication, file attachments, search capabilities, notifications, and comprehensive audit trails.

## Architecture

Built following **Clean Architecture** principles with clear separation of concerns across domain, application, and infrastructure layers. Developed using the **Agentic Workflow Protocol (AWP)** for structured, systematic development. See `agentic-sdlc/AWP.md` for workflow details.

## Key Features

- **Secure Authentication**: JWT-based authentication with bcrypt password hashing
- **Task Management**: Full CRUD operations with ownership-based authorization
- **File Attachments**: Upload and manage files associated with tasks
- **Advanced Search**: Filter and search tasks by multiple criteria
- **Notifications**: Automated reminder system for due tasks
- **Audit Trail**: Comprehensive logging of all system actions
- **Rate Limiting**: Per-user and per-IP request rate limiting
- **Monitoring**: Structured logging with correlation IDs and health checks

## Technology Stack

- **Framework**: FastAPI (Python)
- **Database**: SQLAlchemy ORM with SQLite/PostgreSQL support
- **Authentication**: JWT tokens with python-jose
- **Validation**: Pydantic for request/response validation

## Author

Michael Wybraniec (ONE-FRONT)"""
    )


# Global app config instance
app_config = AppConfig()
