# Task ID: 6.2
# Title: Design worker schedule and query
# Status: [ ] Pending
# Priority: high
# Owner: Backend Dev
# Estimated Effort: 2h

## Description
Design how often the worker should run and how it queries for tasks due in the next 24 hours, per `docs/requirements.md` section "5. Notifications" and `docs/technical-specs.md` section "3.5 Notifications".

**Step-by-step:**
1. Review requirements: worker must "check for tasks due in the next 24 hours" and be "idempotent and fault-tolerant" per `docs/requirements.md`.
2. Design scheduling mechanism:
   - **Option 1: Interval-based** (e.g., run every hour, every 6 hours): Simple, but may miss exact due times.
   - **Option 2: Cron-based** (e.g., run at specific times daily): More predictable, but requires cron scheduler.
   - **Option 3: Continuous polling** (e.g., check every 5 minutes): Most responsive, but higher resource usage.
   - **Recommendation**: Run every hour (balance between responsiveness and resource usage).
3. Define "due in next 24 hours" query:
   - Query tasks where `due_date` is between `NOW()` and `NOW() + 24 hours`.
   - Consider timezone handling (use UTC for consistency).
   - Exclude tasks that already have reminders sent (idempotency check).
4. Design idempotency mechanism:
   - Track which tasks have reminders sent (e.g., `reminder_sent_at` timestamp in task table, or separate `reminder_log` table).
   - Query should exclude tasks with `reminder_sent_at` within the last 24 hours (or check reminder_log for today's date).
   - This prevents duplicate reminders if worker runs multiple times.
5. Design fault tolerance:
   - Worker should handle database connection errors gracefully (retry, log, continue).
   - Worker should handle individual task processing errors (log error, continue with next task, don't crash entire run).
   - Worker should be restartable (state stored in database, not memory).
6. Document query logic:
   - SQL/ORM query: `SELECT * FROM tasks WHERE due_date >= NOW() AND due_date <= NOW() + INTERVAL '24 hours' AND (reminder_sent_at IS NULL OR reminder_sent_at < NOW() - INTERVAL '24 hours')`.
   - Or use reminder_log table to check if reminder already sent today.
7. Document schedule:
   - Frequency: e.g., "Run every hour at :00 minutes" or "Run every 6 hours".
   - Implementation: Use `APScheduler`, `celery beat`, or simple `while True` loop with `time.sleep()`.

**Implementation hints:**
- See `docs/technology.md` section "5. Infrastructure & Services" → "Worker Scheduling" for scheduling library choices, versions, and rationale.
- Use `APScheduler` 3.10+ (recommended) for Python scheduling (simple, no external dependencies) per `docs/technology.md`.
- Or use `celery` 5.3+ with `celery beat` if you want distributed task queue per `docs/technology.md`.
- Query should be efficient (index on `due_date` column).
- Store reminder state in database (not memory) for fault tolerance.
- Use transaction to ensure reminder_sent_at is set atomically with reminder log entry.

## Dependencies
- [ ] Task ID: 6.1 (Requirements analysis must be complete)

## Testing Instructions
- N/A for design task. Verify design describes schedule and query semantics clearly.
- Review design document to ensure query logic handles edge cases (timezone, idempotency, fault tolerance).

## Security Review
- Ensure design does not expose internal scheduling details unnecessarily.
- Query should only access tasks the worker is authorized to process (no user data leakage).

## Risk Assessment
- Poorly chosen schedule or query logic may cause missed or excessive reminders.
- Missing idempotency check will cause duplicate reminders.
- Missing fault tolerance will cause worker crashes and missed reminders.

## Acceptance Criteria
- [ ] Schedule (e.g. interval or cron) is documented with specific frequency (e.g., "every hour", "every 6 hours at :00").
- [ ] Query definition for "due in next 24 hours" is documented with SQL/ORM example.
- [ ] Idempotency mechanism is documented (how to prevent duplicate reminders).
- [ ] Fault tolerance strategy is documented (error handling, restartability).
- [ ] Design is implementable (clear enough to code without guesswork).

## Definition of Done
- [ ] Worker design documented in code comments or design notes.
- [ ] Schedule frequency specified.
- [ ] Query logic documented with example.
- [ ] Idempotency and fault tolerance strategies documented.
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: Design can be implemented directly without guesswork (schedule, query, idempotency, fault tolerance all specified).
- **Observable Outcomes**: Design document/code shows complete worker design with all aspects covered.

## Notes
This decouples decision-making about timing from implementation. The actual worker implementation happens in task 6.3.

## Strengths
Provides clarity on how and when reminders are processed, ensuring idempotency and fault tolerance from the start.

## Sub-tasks (Children)
- [ ] Review notification requirements from `docs/requirements.md` (check tasks due in next 24h, idempotent, fault-tolerant).
- [ ] Evaluate scheduling options (interval, cron, continuous polling) and choose frequency.
- [ ] Define "due in next 24 hours" query logic (SQL/ORM example with timezone handling).
- [ ] Design idempotency mechanism (how to track and check if reminder already sent).
- [ ] Design fault tolerance strategy (error handling, restartability, state management).
- [ ] Document schedule, query, idempotency, and fault tolerance in code comments or design doc.

## Completed
[ ] Pending / [ ] Completed


