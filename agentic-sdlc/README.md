# Agentic SDLC - Project Backlog

This directory contains the **Agentic Software Development Life Cycle (ASDLC)** project backlog and workflow documentation for the Task Tracker application with Agentic Workflow Protocol authored by Michael Wybraniec (www.one-front.com) and maintained together with an open source engineering community.

## Directory Structure

```
agentic-sdlc/
├── README.md              # This file - overview of the structure
├── AWP.md                 # Agentic Workflow Protocol - workflow instructions
├── project-backlog.md     # Main backlog index - lists all tasks
└── tasks/
    └── planned/           # Individual task files
        ├── task-1.md     # Parent/epic tasks (task-1 through task-11)
        ├── task-1-1.md   # Child tasks (task-X-Y format)
        ├── task-1-2.md
        └── ...
```

## Key Files

### `AWP.md` - Agentic Workflow Protocol
The workflow protocol that defines how to work with tasks. Contains:
- **Core workflow commands**: `awp check`, `awp update`, `awp commit`, `awp next`, `awp handoff`
- **Task lifecycle**: Starting, working on, and completing tasks
- **Handling issues**: How to document and resolve blockers, unclear requirements, etc.
- **Best practices**: Guidelines for humans and AI agents

**👉 Start here**: Read `AWP.md` to understand the workflow before working on tasks.

### `project-backlog.md` - Main Backlog Index
The high-level overview of all planned tasks. Contains:
- **Planned Tasks**: Hierarchical list of all 11 main tasks and their child tasks
- **How to Use This Backlog**: Quick start guide and workflow commands
- **Task links**: Direct links to all task files
- **Status tracking**: Planned, Unplanned, and Completed sections

**👉 Use this**: To see the big picture and find the next task to work on.

### `tasks/planned/` - Task Files
Individual task files containing detailed implementation guidance. Each task file includes:
- **Task metadata**: ID, title, status, priority, owner, estimated effort
- **Description**: Step-by-step instructions for implementation
- **Dependencies**: Prerequisite tasks that must be completed first
- **Acceptance criteria**: Detailed, measurable criteria for completion
- **Testing instructions**: How to test the implementation
- **Security review**: Security considerations
- **Risk assessment**: Potential risks and mitigation
- **Definition of done**: Checklist for completion
- **Implementation hints**: File locations, patterns, libraries to use
- **Sub-tasks**: Actionable breakdown of work

## Task Organization

### Hierarchical Structure

Tasks are organized in a two-level hierarchy:

1. **Parent/Epic Tasks** (`task-1.md` through `task-11.md`):
   - High-level feature areas (e.g., "Task 2: Secure login and authorization")
   - Contain links to child tasks
   - Provide overview of the feature area

2. **Child Tasks** (`task-X-Y.md`):
   - Detailed, actionable implementation tasks
   - Self-contained with full instructions
   - Can be worked on independently (once dependencies are met)

### Task Naming Convention

- **Parent tasks**: `task-1.md`, `task-2.md`, ..., `task-11.md`
- **Child tasks**: `task-1-1.md`, `task-1-2.md`, `task-2-1.md`, etc.
  - First number = parent task ID
  - Second number = child task ID within that parent

### Task Status

Tasks can have the following status values:
- `[ ] Pending` - Not yet started
- `[x] In Progress` - Currently being worked on
- `[x] Completed` - Finished and verified
- `[ ] Blocked` - Cannot proceed due to dependencies or blockers
- `[ ] Deferred` - Intentionally postponed

## How to Use This Backlog

### For New Contributors

1. **Read the workflow**: Start with `AWP.md` to understand the protocol
2. **Review the backlog**: Check `project-backlog.md` to see all tasks
3. **Find your task**: Look for tasks with all dependencies completed
4. **Read the task file**: Open the specific task file (e.g., `tasks/planned/task-2-1.md`)
5. **Follow the workflow**: Use AWP commands (`awp check`, `awp update`, etc.)

### Finding the Next Task

1. Open `project-backlog.md`
2. Look for tasks marked as `[ ] Pending`
3. Check dependencies (listed in each task file)
4. Choose a task where all dependencies are completed
5. Read the full task file before starting

### Working on a Task

1. **Check dependencies**: Verify all prerequisite tasks are completed
2. **Read the task file**: Review description, acceptance criteria, and sub-tasks
3. **Review requirements**: Check `docs/requirements.md` and `docs/technical-specs.md` for context
4. **Update status**: Mark task as `[x] In Progress` in the task file
5. **Follow instructions**: Use the step-by-step instructions in the Description section
6. **Test incrementally**: Run tests as you work, don't wait until the end
7. **Document issues**: Add any blockers or questions to the Notes section
8. **Verify acceptance criteria**: Check off criteria as you complete them
9. **Complete the task**: Mark as `[x] Completed`, update backlog, commit with task reference

### Handling Issues

When you encounter issues (blockers, unclear requirements, etc.):

1. **Document in task file**: Add to the "Notes" section with format:
   ```markdown
   **Issue [Type]**: Description. Impact: [what's affected]. Resolution: [if known] or [needs decision/escalation]
   ```

2. **Update status**: If blocked, change to `[ ] Blocked`

3. **Decide action**:
   - **Escalate**: If security concern, scope question, or major blocker
   - **Make decision**: If minor implementation detail, document choice and proceed
   - **Update task**: If task description is clearly wrong

4. **Use `awp handoff`**: If switching to human for decision/escalation

See `AWP.md` → "Handling Issues" section for complete guidance.

## Workflow Commands

The Agentic Workflow Protocol defines these commands:

- **`awp check`**: Determine the current actionable step
- **`awp update`**: Review docs, update documentation, check for blockers
- **`awp commit`**: Commit changes with task references (e.g., `feat(auth): implement login [task-2-3]`)
- **`awp next`**: Move to next task after update and commit
- **`awp handoff`**: Transfer work between human and AI

See `AWP.md` for detailed command descriptions and usage.

## Task File Template

Each task file follows this structure:

```markdown
# Task ID: X.Y
# Title: Task title
# Status: [ ] Pending
# Priority: high/medium/low
# Owner: Role
# Estimated Effort: Xh

## Description
Step-by-step instructions for implementation...

## Dependencies
- [ ] Task ID: X.Y

## Testing Instructions
How to test the implementation...

## Security Review
Security considerations...

## Risk Assessment
Potential risks...

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Definition of Done
- [ ] Checklist item 1
- [ ] Checklist item 2

## Measurable Outcomes
Verification criteria...

## Notes
Any additional notes, issues, or decisions...

## Strengths
Why this task is valuable...

## Sub-tasks (Children)
- [ ] Sub-task 1
- [ ] Sub-task 2

## Completed
[ ] Pending / [ ] Completed
```

## Integration with Project

This backlog is tightly integrated with the project documentation:

- **Requirements**: Tasks derive from `docs/requirements.md`
- **Technical Specs**: Tasks reference `docs/technical-specs.md`
- **Architecture**: Tasks align with `docs/architecture.md`
- **Code**: Tasks reference specific file paths and patterns

## Best Practices

1. **Always read the full task file** before starting work
2. **Check dependencies** before beginning a task
3. **Follow step-by-step instructions** precisely
4. **Document issues immediately** when encountered
5. **Test incrementally** rather than waiting until completion
6. **Commit frequently** with clear, descriptive messages
7. **Reference tasks** in commit messages for traceability
8. **Update task status** as you progress
9. **Use AWP commands** for consistent workflow

## Getting Help

- **Workflow questions**: See `AWP.md`
- **Task questions**: Check the task file's Notes section, or review `docs/requirements.md`
- **Structure questions**: See this README or `project-backlog.md`
- **Implementation questions**: Review task file's Implementation hints and step-by-step instructions

## Task Coverage

This backlog covers all requirements from `docs/requirements.md`:

- ✅ Task 1: Project environment and documentation
- ✅ Task 2: Secure login and authorization
- ✅ Task 3: Task management API (CRUD)
- ✅ Task 4: Attachments API
- ✅ Task 5: Search, filtering, sorting, pagination
- ✅ Task 6: Notifications worker for due tasks
- ✅ Task 7: Audit trail implementation
- ✅ Task 8: Rate limiting
- ✅ Task 9: Monitoring, logging, health checks
- ✅ Task 10: React frontend
- ✅ Task 11: Testing and self-assessment

Each main task is broken down into detailed child tasks (49 total child tasks) with comprehensive implementation guidance.

---

**Next Steps**: Read [AWP.md](AWP.md) to understand the workflow, then check [project-backlog.md](project-backlog.md) to find your next task.

