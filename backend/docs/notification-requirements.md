# Notification Requirements

This document summarizes all notification requirements extracted from the project documentation.

## Source References
- `docs/requirements.md` section "5. Notifications"
- `docs/technical-specs.md` section "3.5 Notifications"

## Requirements Summary

### 1. Background Worker/Service
**Requirement**: A background worker/service that checks for tasks due in the next 24 hours.

**Source**: 
- `docs/requirements.md` §5: "Background worker/service checks for tasks due in the next 24 hours and logs 'reminder sent' events."
- `docs/technical-specs.md` §3.5: "A background worker/service: Checks for tasks due in the next 24 hours."

**Details**:
- Worker runs periodically (schedule to be determined in design)
- Worker queries database for tasks with `due_date` within next 24 hours
- Worker is a separate service/process (can run in same container or separate)

### 2. Reminder Sent Events
**Requirement**: Log "reminder sent" events.

**Source**:
- `docs/requirements.md` §5: "logs 'reminder sent' events."
- `docs/technical-specs.md` §3.5: "Logs 'reminder sent' events."

**Details**:
- Log reminder events (not actual email/SMS notifications per requirements)
- Events should be logged to audit trail or reminder log table
- Each event should include: task_id, timestamp, worker_run_id (optional)

### 3. Idempotency
**Requirement**: No duplicate reminders.

**Source**:
- `docs/requirements.md` §5: "Idempotent and fault-tolerant (no duplicate reminders)."
- `docs/technical-specs.md` §3.5: "The notification system must be: Idempotent."

**Details**:
- Same task should not receive multiple reminders in the same 24-hour window
- Need mechanism to track which tasks have reminders sent
- Idempotency check should prevent duplicate reminder events
- Use atomic operations (database transactions) to prevent race conditions

### 4. Fault Tolerance
**Requirement**: Fault-tolerant (no duplicate reminders).

**Source**:
- `docs/requirements.md` §5: "Idempotent and fault-tolerant (no duplicate reminders)."
- `docs/technical-specs.md` §3.5: "Fault‑tolerant (no duplicate reminders)."

**Details**:
- Worker should handle failures gracefully (retry, don't crash, resume after restart)
- Worker should handle database connection errors (retry connection, don't crash)
- Worker should handle individual task processing errors (log error, continue with next task)
- Worker should be restartable (state stored in database, not memory)
- Failed jobs should be retried with reasonable strategy (exponential backoff, max retries)

## Implicit Requirements

### 5. Worker Scheduling
**Requirement**: Worker runs on a schedule.

**Source**: Implicit (worker must run periodically to check for due tasks).

**Details**:
- Worker must run periodically (interval or cron - design decision from task 6.2)
- Schedule frequency: to be determined (e.g., every hour, every 6 hours)
- Implementation: Use `APScheduler`, `celery beat`, or simple loop with `time.sleep()`

### 6. Reminder Tracking
**Requirement**: Track which tasks have reminders sent.

**Source**: Implicit (needed for idempotency).

**Details**:
- Need to mark which tasks have reminders sent
- Options: `reminder_sent_at` timestamp in task table, or separate `reminder_log` table
- Query should exclude tasks with reminders already sent within last 24 hours
- Tracking should be stored in database (not memory) for fault tolerance

### 7. Time Window Definition
**Requirement**: "Due in next 24 hours" query logic.

**Source**: Implicit from "tasks due in the next 24 hours".

**Details**:
- Query tasks where `due_date` is between `NOW()` and `NOW() + 24 hours`
- Consider timezone handling (use UTC for consistency)
- Query should be efficient (index on `due_date` column)

### 8. Audit Trail Integration
**Requirement**: Reminder events should be part of audit trail.

**Source**: 
- `docs/requirements.md` §6: "Record key actions: ... reminder sent."
- `docs/technical-specs.md` §3.6: "Record key actions: ... Reminder sent."

**Details**:
- Reminder sent events should be recorded in audit trail
- Include timestamps and task ID
- Can be part of general audit trail or separate reminder log

## Design Decisions Needed

1. **Scheduling Frequency**:
   - How often should worker run? (e.g., every hour, every 6 hours)
   - Decision: To be made in task 6.2 (recommend every hour for balance)

2. **Idempotency Mechanism**:
   - Use `reminder_sent_at` column on tasks table or separate `reminder_log` table?
   - Decision: To be made in task 6.2 (recommend `reminder_sent_at` for simplicity)

3. **Scheduling Library**:
   - Use `APScheduler`, `celery beat`, or simple loop?
   - Decision: To be made in task 6.2 (recommend `APScheduler` for simplicity)

4. **Retry Strategy**:
   - Max retries, backoff strategy, error handling
   - Decision: To be made in task 6.4 (recommend exponential backoff, 3 retries)

5. **Reminder Log Storage**:
   - Store in tasks table (`reminder_sent_at`) or separate table?
   - Decision: To be made in task 6.2 (recommend `reminder_sent_at` for simplicity)

## Implementation Tasks

- Task 6.2: Design worker schedule and query (scheduling frequency, query logic, idempotency mechanism)
- Task 6.3: Implement reminder worker job (job function, scheduler integration, reminder logging)
- Task 6.4: Implement idempotency and retry behavior (atomic operations, retry logic, fault tolerance)

## Security Considerations

1. **Logging**: Log only task ID, timestamp, worker run ID (not task content, user data)
2. **Authorization**: Worker should only process tasks it's authorized to process
3. **Error Logging**: Use structured logging with appropriate log levels (INFO for reminders, ERROR for failures)

## Summary

**Required behaviors**:
- ✅ Background worker/service that runs periodically
- ✅ Checks for tasks due in the next 24 hours
- ✅ Logs "reminder sent" events (not actual notifications)
- ✅ Idempotent (no duplicate reminders in same 24h window)
- ✅ Fault-tolerant (handles failures gracefully, retry, restartable)
- ✅ Reminder tracking (mark which tasks have reminders sent)
- ✅ Audit trail integration (reminder events recorded)

**Design decisions needed**:
- Scheduling frequency (recommend: every hour)
- Idempotency mechanism (recommend: `reminder_sent_at` column)
- Scheduling library (recommend: `APScheduler`)
- Retry strategy (recommend: exponential backoff, 3 retries)
- Reminder log storage (recommend: `reminder_sent_at` on tasks table)

All requirements from `docs/requirements.md` §5 and `docs/technical-specs.md` §3.5 are accounted for.
