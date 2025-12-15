# Task ID: 6
# Title: Notifications worker for due tasks
# Status: [x] In Progress
# Priority: high
# Owner: Backend Dev
# Estimated Effort: 8h

## Description
Implement a background worker/service that checks for tasks due in the next 24 hours and logs “reminder sent” events in an idempotent and fault-tolerant way (no duplicate reminders).

## Dependencies
- [x] Task ID: 3

## Testing Instructions
- Worker/queue tests for:
  - Detecting tasks due in the next 24 hours.
  - Logging “reminder sent” events.
  - Avoiding duplicate reminders for the same task/time window.
  - Retry behavior on transient failures.

## Security Review
- Ensure worker operations respect authorization and do not expose sensitive information in logs.

## Risk Assessment
- Duplicate or missing reminders could reduce user trust; failures must be handled gracefully.

## Acceptance Criteria
- [ ] Worker scans for tasks due in the next 24 hours on a schedule.
- [ ] “Reminder sent” events are logged for qualifying tasks.
- [ ] Implementation is idempotent: no duplicate reminder events for the same task/time window.
- [ ] Failed jobs are retried with a reasonable strategy.
- [ ] Worker tests (including idempotency and retries) are passing.

## Definition of Done
- [ ] Worker implemented and wired into the system.
- [ ] Logging for reminders integrated with audit trail.
- [ ] Tests for worker behavior implemented and passing.
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: Worker tests show correct reminders and no duplicates.

## Notes
The requirement is to log reminders; actual user-facing notification channels can be treated as a design choice if time is limited.

## Strengths
Satisfies the “Notifications” requirement in a robust, testable way.

## Sub-tasks (Children)
- [ ] [Task 6.1: Confirm notification requirements](task-6-1.md)
- [ ] [Task 6.2: Design worker schedule and query](task-6-2.md)
- [ ] [Task 6.3: Implement reminder worker job](task-6-3.md)
- [ ] [Task 6.4: Implement idempotency and retry behavior](task-6-4.md)

## Completed
[ ] Pending / [ ] Completed


