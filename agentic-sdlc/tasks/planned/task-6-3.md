# Task ID: 6.3
# Title: Implement reminder worker job
# Status: [x] Completed
# Priority: high
# Owner: Backend Dev
# Estimated Effort: 4h

## Description
Implement the worker job that queries for tasks due in the next 24 hours and logs "reminder sent" events, according to the design from task 6.2, per `docs/requirements.md` section "5. Notifications" and `docs/technical-specs.md` section "3.5 Notifications".

**Step-by-step:**
1. Review worker design from task 6.2 (schedule frequency, query logic, idempotency mechanism).
2. Create worker job function (e.g., `backend/worker/jobs/reminder_job.py`):
   - Function: `process_reminders()` or `check_due_tasks()`.
   - Query tasks due in next 24 hours:
     - `SELECT * FROM tasks WHERE due_date >= NOW() AND due_date <= NOW() + INTERVAL '24 hours'`.
     - Exclude tasks that already have reminders sent (idempotency check from task 6.2):
       - `AND (reminder_sent_at IS NULL OR reminder_sent_at < NOW() - INTERVAL '24 hours')`.
       - Or check reminder_log table for today's date.
   - For each qualifying task:
     - Log "reminder sent" event (write to audit trail or reminder_log table).
     - Mark task as having reminder sent (set `reminder_sent_at = NOW()` or insert into reminder_log).
   - Handle errors gracefully (log error, continue with next task, don't crash entire run).
3. Integrate with scheduling mechanism (from task 6.2):
   - Use `APScheduler` (Python) or `celery beat` to schedule job.
   - Configure schedule (e.g., run every hour at :00 minutes).
   - Start scheduler when worker service starts.
4. Create audit trail/reminder log:
   - Create `reminder_log` table or add `reminder_sent_at` column to tasks table.
   - Log entry: task_id, sent_at (timestamp), worker_run_id (optional for tracking).
5. Write worker tests:
   - Test query selects tasks due in next 24h (verify correct tasks selected).
   - Test query excludes tasks with reminders already sent (verify idempotency check works).
   - Test "reminder sent" events are logged (verify log entries created).
   - Test error handling (verify worker continues after individual task errors).
   - Test worker runs on schedule (verify scheduler triggers job at correct times).

**Implementation hints:**
- Place worker code in `backend/worker/` directory (separate from API).
- Use database connection pool for worker (same as API or separate).
- Use structured logging (include correlation IDs, timestamps, task IDs).
- Place reminder log in database (not just console logs) for audit trail.
- Worker should be a separate service/process (can run in same container or separate).

## Dependencies
- [x] Task ID: 6.2 (Worker design must be complete)

## Testing Instructions
- Worker tests (unit/integration):
  - For a given time window, tasks due in the next 24h are selected (verify query returns correct tasks).
  - "Reminder sent" events are logged for those tasks (verify log entries created in database).
  - Test idempotency check (verify tasks with reminders already sent are excluded).
  - Test error handling (verify worker continues after individual task errors).
  - Test scheduling (verify worker runs on schedule - can use test scheduler with shorter intervals).
- Manual test: Run worker manually, verify it queries and logs reminders correctly.

## Security Review
- Ensure logs do not expose sensitive task details:
  - Log only task ID, timestamp, worker run ID (not task content, user data).
  - Use structured logging with appropriate log levels (INFO for reminders, ERROR for failures).

## Risk Assessment
- Incorrect job behavior may result in no reminders or reminders for wrong tasks.
- Missing error handling may cause worker crashes and missed reminders.
- Incorrect query logic may select wrong tasks or miss tasks.

## Acceptance Criteria
- [x] Worker job executes on schedule and queries due tasks correctly (query selects tasks due in next 24h).
- [x] "Reminder sent" events are written for each qualifying task (log entries created in database).
- [x] Idempotency check implemented (tasks with reminders already sent are excluded from query).
- [x] Error handling implemented (worker continues after individual task errors, logs errors).
- [x] Tests verifying selection and logging behavior are passing (query correct, logging works, idempotency works).

## Definition of Done
- [ ] Worker job implemented and integrated with scheduling mechanism (job function, scheduler configured).
- [ ] Query logic implemented (select tasks due in next 24h, exclude already-reminded tasks).
- [ ] Reminder logging implemented (write to audit trail or reminder_log table).
- [ ] Error handling implemented (try-catch per task, log errors, continue).
- [ ] Tests added and passing (query, logging, idempotency, error handling, scheduling).
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: Tests confirm the correct tasks get corresponding reminder events (query correct, logging works, idempotency works).
- **Observable Outcomes**: Worker runs on schedule, queries correct tasks, logs reminders, handles errors gracefully.

## Notes
Idempotency and retry behavior are addressed in task 6.4. This task implements the core reminder logic, while task 6.4 adds robustness.

**Completed**: 
- Added `reminder_sent_at` column to Task model
- Implemented `process_reminders()` job function with query logic
- Integrated APScheduler to run job every hour
- Implemented atomic check-and-set for idempotency
- Added error handling (continues on individual task errors)
- Integrated scheduler with FastAPI app lifecycle (startup/shutdown)
- Added comprehensive tests (query selection, idempotency, error handling)

## Strengths
Implements the core "reminder sent" behavior required by the assignment. Provides foundation for idempotency and retry logic in task 6.4.

## Sub-tasks (Children)
- [ ] Review worker design from task 6.2 (schedule, query logic, idempotency mechanism).
- [ ] Create worker job function (query tasks due in next 24h, exclude already-reminded, log reminders).
- [ ] Integrate with scheduling mechanism (APScheduler or celery beat, configure schedule).
- [ ] Create reminder log/audit trail (reminder_log table or reminder_sent_at column).
- [ ] Implement error handling (try-catch per task, log errors, continue with next task).
- [ ] Write worker tests (query correct, logging works, idempotency check, error handling, scheduling).
- [ ] Test manually by running worker and verifying behavior.

## Completed
[x] Completed


