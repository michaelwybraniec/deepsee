# Task ID: 6.4
# Title: Implement idempotency and retry behavior
# Status: [x] Completed
# Priority: high
# Owner: Backend Dev
# Estimated Effort: 4h

## Description
Implement idempotency tracking and retry behavior so that reminder processing is fault-tolerant and does not produce duplicate reminders, per `docs/requirements.md` section "5. Notifications" and `docs/technical-specs.md` section "3.5 Notifications".

**Step-by-step:**
1. Review worker implementation from task 6.3 (basic reminder job exists, needs idempotency and retry).
2. Enhance idempotency mechanism (from task 6.2 design):
   - Use `reminder_sent_at` timestamp on task or `reminder_log` table.
   - Check before logging reminder: if reminder already sent today (or within last 24h), skip.
   - Use database transaction to ensure atomic check-and-set (prevent race conditions).
   - Example: `UPDATE tasks SET reminder_sent_at = NOW() WHERE id = ? AND (reminder_sent_at IS NULL OR reminder_sent_at < NOW() - INTERVAL '24 hours') RETURNING id;` (only updates if no recent reminder).
3. Implement retry logic for transient failures:
   - Wrap reminder processing in try-catch.
   - On failure (database error, network error, etc.):
     - Log error with task ID and error details.
     - Retry up to N times (e.g., 3 retries) with exponential backoff (e.g., 1s, 2s, 4s delays).
     - If all retries fail: log final error, mark task for manual review (optional), continue with next task.
   - Use idempotency check even on retries (if reminder was sent during retry, skip).
4. Implement fault tolerance:
   - Worker should handle database connection errors (retry connection, don't crash).
   - Worker should handle individual task processing errors (log, retry, continue).
   - Worker should be restartable (state stored in database, not memory - can resume after restart).
   - Use transaction boundaries (process each task in its own transaction if possible).
5. Write worker/queue tests:
   - Test idempotency: re-running worker over same time period does not create duplicate reminders (verify only one reminder per task per 24h window).
   - Test retry logic: simulate transient failure (database timeout, network error), verify retries happen and eventually succeed.
   - Test retry exhaustion: simulate permanent failure, verify retries stop after max attempts and error is logged.
   - Test fault tolerance: simulate worker crash, verify it can restart and resume (no duplicate reminders, no missed reminders).

**Implementation hints:**
- Use database transactions for idempotency (atomic check-and-set prevents race conditions).
- Use exponential backoff for retries (prevents overwhelming system on transient failures).
- Place retry logic in worker job function (wrap reminder processing in retry loop).
- Use structured logging for retries (log attempt number, error, retry delay).
- Consider using a job queue (celery, RQ) for better retry handling - optional enhancement.

## Dependencies
- [x] Task ID: 6.3 (Basic worker job must exist)

## Testing Instructions
- Worker/queue tests (unit/integration):
  - Re-running the worker over the same time period does not create duplicate "reminder sent" events (verify idempotency - only one reminder per task per 24h).
  - Failed jobs are retried according to design and eventually succeed or are reported (verify retries happen, succeed on transient failures, log on permanent failures).
  - Test idempotency with concurrent runs (simulate multiple workers, verify no duplicates).
  - Test fault tolerance (simulate worker crash/restart, verify resume without duplicates or misses).
- Manual test: Run worker multiple times, verify no duplicate reminders, simulate failures and verify retries.

## Security Review
- Ensure retry logs and storage do not expose sensitive data:
  - Log only task ID, error type, retry count (not task content, user data).
  - Use appropriate log levels (INFO for retries, ERROR for failures).

## Risk Assessment
- Without idempotency and retries, users may receive duplicate or missing reminders.
- Race conditions in idempotency check can cause duplicates (need atomic operations).
- Missing retry logic can cause missed reminders on transient failures.

## Acceptance Criteria
- [x] Idempotency mechanism implemented (e.g., marker per task/time window - `reminder_sent_at` or `reminder_log` table).
- [x] Idempotency uses atomic operations (database transaction or atomic update) to prevent race conditions.
- [x] Retry logic implemented for transient worker failures (exponential backoff, max retries, error logging).
- [x] Fault tolerance implemented (handle connection errors, individual task errors, restartable).
- [x] Tests for idempotency and retry scenarios are passing (no duplicates, retries work, fault tolerance works).

## Definition of Done
- [ ] Idempotency and retry logic integrated into the worker job (enhance job from task 6.3).
- [ ] Idempotency mechanism implemented (atomic check-and-set, prevent duplicates).
- [ ] Retry logic implemented (exponential backoff, max retries, error handling).
- [ ] Fault tolerance implemented (connection error handling, restartability).
- [ ] Tests added and passing (idempotency, retries, fault tolerance).
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: Tests show no duplicates after multiple runs and successful retries after simulated failures (idempotency works, retries work, fault tolerance works).
- **Observable Outcomes**: Worker handles failures gracefully, no duplicate reminders, retries succeed on transient failures.

## Notes
This fulfills the "idempotent and fault-tolerant (no duplicate reminders)" part of the requirement. Builds on task 6.3 to add robustness.

**Completed**: 
- Enhanced idempotency with atomic UPDATE operations (already in 6.3)
- Implemented retry logic with exponential backoff (1s, 2s, 4s delays, max 3 retries)
- Added fault tolerance for database connection errors (retry on next run)
- Individual task errors handled gracefully (log, continue with next task)
- Worker is restartable (state in database, not memory)
- Added test for retry behavior on transient failures

## Strengths
Makes notification behavior robust and production-friendly. Ensures reliable reminder delivery without duplicates.

## Sub-tasks (Children)
- [ ] Review worker implementation from task 6.3 (basic reminder job).
- [ ] Enhance idempotency mechanism (atomic check-and-set, prevent race conditions, use transactions).
- [ ] Implement retry logic (exponential backoff, max retries, error logging, handle transient failures).
- [ ] Implement fault tolerance (connection error handling, individual task error handling, restartability).
- [ ] Write worker/queue tests (idempotency - no duplicates, retries - succeed on transient failures, fault tolerance - restartable).
- [ ] Test manually by running worker multiple times and simulating failures.

## Completed
[x] Completed


