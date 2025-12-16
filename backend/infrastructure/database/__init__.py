"""Database infrastructure module."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from domain.models import Base  # This imports all models and Base

# Database URL from environment variable (defaults to SQLite for development)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./task_tracker.db")

# SQLite-specific connection args (only apply to SQLite)
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
