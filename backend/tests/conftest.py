"""Pytest configuration and shared fixtures."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import bcrypt

from api.main import app
from infrastructure.database import get_db
# Import Base first, then all models to ensure they're registered
from domain.models import Base
from domain.models.user import User
from domain.models.task import Task
from domain.models.attachment import Attachment
from infrastructure.persistence.models.audit_event import AuditEvent

# Use shared in-memory SQLite for tests (file-based ensures same connection)
# Using a file path ensures all connections share the same database
import tempfile
import os
_test_db_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
_test_db_file.close()
TEST_DATABASE_URL = f"sqlite:///{_test_db_file.name}"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Cleanup function to remove test database file
def _cleanup_test_db():
    try:
        if os.path.exists(_test_db_file.name):
            os.unlink(_test_db_file.name)
    except Exception:
        pass


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    # Drop all tables first to ensure clean state
    Base.metadata.drop_all(bind=test_engine)
    # Create tables
    Base.metadata.create_all(bind=test_engine)
    
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.rollback()  # Rollback any uncommitted changes
        db.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session: Session):
    """Create test client with database override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass  # Don't close here, fixture handles it
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session: Session):
    """Create a test user."""
    hashed_password = bcrypt.hashpw(b"testpassword", bcrypt.gensalt()).decode('utf-8')
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hashed_password
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_user2(db_session: Session):
    """Create a second test user."""
    hashed_password = bcrypt.hashpw(b"password2", bcrypt.gensalt()).decode('utf-8')
    user = User(
        username="user2",
        email="user2@example.com",
        hashed_password=hashed_password
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def user1(db_session: Session):
    """Create test user 1 (alias for compatibility with some tests)."""
    hashed_password = bcrypt.hashpw(b"password1", bcrypt.gensalt()).decode('utf-8')
    user = User(
        username="user1",
        email="user1@example.com",
        hashed_password=hashed_password
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def user2(db_session: Session):
    """Create test user 2 (alias for compatibility with some tests)."""
    hashed_password = bcrypt.hashpw(b"password2", bcrypt.gensalt()).decode('utf-8')
    user = User(
        username="user2",
        email="user2@example.com",
        hashed_password=hashed_password
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user
