"""Tests for reminder worker job."""

import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from domain.models.task import Task
from domain.models.user import User
from worker.jobs.reminder_job import process_reminders
import bcrypt


@pytest.fixture
def test_user_with_tasks(db_session: Session):
    """Create a test user with various tasks for reminder testing."""
    # Create user
    hashed_password = bcrypt.hashpw(b"testpassword", bcrypt.gensalt()).decode('utf-8')
    user = User(
        username="testuser_worker",
        email="testworker@example.com",
        hashed_password=hashed_password
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    # Create tasks with different due dates
    now = datetime.utcnow()
    
    # Task due in 12 hours (should get reminder)
    task1 = Task(
        title="Task due in 12h",
        description="Should get reminder",
        due_date=now + timedelta(hours=12),
        owner_user_id=user.id,
        status="todo",
        priority="high"
    )
    
    # Task due in 6 hours (should get reminder)
    task2 = Task(
        title="Task due in 6h",
        description="Should get reminder",
        due_date=now + timedelta(hours=6),
        owner_user_id=user.id,
        status="todo",
        priority="medium"
    )
    
    # Task due in 30 hours (should NOT get reminder - beyond 24h)
    task3 = Task(
        title="Task due in 30h",
        description="Should NOT get reminder",
        due_date=now + timedelta(hours=30),
        owner_user_id=user.id,
        status="todo",
        priority="low"
    )
    
    # Task due in 2 hours but already reminded (should NOT get reminder)
    task4 = Task(
        title="Task already reminded",
        description="Already reminded",
        due_date=now + timedelta(hours=2),
        owner_user_id=user.id,
        status="todo",
        priority="high",
        reminder_sent_at=now - timedelta(hours=1)  # Reminded 1 hour ago
    )
    
    # Task due in 2 hours, reminded 25 hours ago (should get reminder - old reminder expired)
    task5 = Task(
        title="Task with old reminder",
        description="Old reminder expired",
        due_date=now + timedelta(hours=2),
        owner_user_id=user.id,
        status="todo",
        priority="medium",
        reminder_sent_at=now - timedelta(hours=25)  # Reminded 25 hours ago
    )
    
    db_session.add_all([task1, task2, task3, task4, task5])
    db_session.commit()
    
    return user, [task1, task2, task3, task4, task5]


def test_reminder_job_selects_tasks_due_in_next_24h(db_session: Session, test_user_with_tasks):
    """Test that reminder job selects tasks due in next 24 hours."""
    user, tasks = test_user_with_tasks
    
    # Run reminder job
    process_reminders()
    
    # Refresh tasks from database
    db_session.refresh(tasks[0])
    db_session.refresh(tasks[1])
    db_session.refresh(tasks[2])
    db_session.refresh(tasks[3])
    db_session.refresh(tasks[4])
    
    # Task 1 (due in 12h): should have reminder_sent_at set
    assert tasks[0].reminder_sent_at is not None, "Task due in 12h should get reminder"
    
    # Task 2 (due in 6h): should have reminder_sent_at set
    assert tasks[1].reminder_sent_at is not None, "Task due in 6h should get reminder"
    
    # Task 3 (due in 30h): should NOT have reminder_sent_at set
    assert tasks[2].reminder_sent_at is None, "Task due in 30h should NOT get reminder"
    
    # Task 4 (already reminded): should keep old reminder_sent_at (not updated)
    original_reminder = tasks[3].reminder_sent_at
    db_session.refresh(tasks[3])
    assert tasks[3].reminder_sent_at == original_reminder, "Already reminded task should not get new reminder"
    
    # Task 5 (old reminder expired): should have reminder_sent_at updated
    assert tasks[4].reminder_sent_at is not None, "Task with expired reminder should get new reminder"
    assert tasks[4].reminder_sent_at > tasks[4].reminder_sent_at - timedelta(hours=25), "Reminder should be recent"


def test_reminder_job_idempotency(db_session: Session, test_user_with_tasks):
    """Test that reminder job is idempotent (no duplicate reminders)."""
    user, tasks = test_user_with_tasks
    
    # Run reminder job first time
    process_reminders()
    
    # Get reminder_sent_at timestamps
    db_session.refresh(tasks[0])
    first_reminder_time = tasks[0].reminder_sent_at
    
    # Run reminder job second time (should not create duplicate)
    process_reminders()
    
    # Check that reminder_sent_at was not updated
    db_session.refresh(tasks[0])
    second_reminder_time = tasks[0].reminder_sent_at
    
    # Should be the same (no duplicate reminder)
    assert first_reminder_time == second_reminder_time, "Reminder should not be sent twice"


def test_reminder_job_handles_errors_gracefully(db_session: Session, test_user_with_tasks):
    """Test that reminder job handles errors gracefully."""
    user, tasks = test_user_with_tasks
    
    # Corrupt one task's due_date to cause error (set to None)
    tasks[0].due_date = None
    db_session.commit()
    
    # Run reminder job (should not crash)
    try:
        process_reminders()
    except Exception:
        pytest.fail("Reminder job should handle errors gracefully and not crash")
    
    # Other tasks should still be processed
    db_session.refresh(tasks[1])
    assert tasks[1].reminder_sent_at is not None, "Other tasks should still be processed despite errors"


def test_reminder_job_excludes_past_due_tasks(db_session: Session):
    """Test that reminder job excludes tasks that are already past due."""
    # Create user
    hashed_password = bcrypt.hashpw(b"testpassword", bcrypt.gensalt()).decode('utf-8')
    user = User(
        username="testuser_past",
        email="testpast@example.com",
        hashed_password=hashed_password
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    now = datetime.utcnow()
    
    # Task that was due 1 hour ago (should NOT get reminder - already past due)
    past_task = Task(
        title="Past due task",
        description="Already past due",
        due_date=now - timedelta(hours=1),
        owner_user_id=user.id,
        status="todo",
        priority="high"
    )
    
    db_session.add(past_task)
    db_session.commit()
    
    # Run reminder job
    process_reminders()
    
    # Check that past due task did not get reminder
    db_session.refresh(past_task)
    assert past_task.reminder_sent_at is None, "Past due task should NOT get reminder"


def test_reminder_job_retry_on_transient_failure(db_session: Session, monkeypatch):
    """Test that reminder job retries on transient database errors."""
    # Create user
    hashed_password = bcrypt.hashpw(b"testpassword", bcrypt.gensalt()).decode('utf-8')
    user = User(
        username="testuser_retry",
        email="testretry@example.com",
        hashed_password=hashed_password
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    now = datetime.utcnow()
    
    # Task due in 12 hours
    task = Task(
        title="Task for retry test",
        description="Test retry logic",
        due_date=now + timedelta(hours=12),
        owner_user_id=user.id,
        status="todo",
        priority="high"
    )
    
    db_session.add(task)
    db_session.commit()
    
    # Simulate transient failure on first attempt, success on second
    call_count = [0]
    original_execute = db_session.execute
    
    def mock_execute(*args, **kwargs):
        call_count[0] += 1
        if call_count[0] == 1:
            # First attempt: raise transient error
            from sqlalchemy.exc import OperationalError
            raise OperationalError("Connection lost", None, None)
        # Second attempt: succeed
        return original_execute(*args, **kwargs)
    
    monkeypatch.setattr(db_session, "execute", mock_execute)
    
    # Run reminder job (should retry and succeed)
    from worker.jobs.reminder_job import _process_single_reminder
    last_24h = now - timedelta(hours=24)
    success = _process_single_reminder(db_session, task, now, last_24h)
    
    # Should succeed after retry
    assert success, "Reminder should succeed after retry"
    assert call_count[0] == 2, "Should retry once after transient failure"
    
    # Check that reminder was sent
    db_session.refresh(task)
    assert task.reminder_sent_at is not None, "Reminder should be sent after successful retry"
