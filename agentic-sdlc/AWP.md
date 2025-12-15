# Agentic Workflow Protocol (AWP)

This document defines the workflow protocol for working with tasks in the Agentic SDLC backlog.

## Overview

The Agentic Workflow Protocol (AWP) provides a structured approach for humans and AI agents to collaborate on implementing tasks from the project backlog. It ensures consistent progress tracking, proper documentation, and clear handoffs.

## Hard Instructions for AI Agents

**This Agentic Workflow Protocol (AWP) governs collaboration between human and AI contributors. The following principles must always be followed:**

1. All work is guided strictly by the AWP; no deviations or improvisation.

2. The AI must always listen to the human, never override instructions, and never take initiative beyond what is explicitly requested.

3. Every change or decision must be validated by the human before proceeding.

4. The AI must never hide changes or actions; transparency is required at all times.

5. If instructions from the human are unclear, the AI must ask clarifying questions and never assume or anticipate requirements.

6. The protocol is designed to ensure trust, clarity, and effective collaboration between human and AI.

7. The AI must never make assumptions or take initiative beyond what is explicitly requested.

8. Always use the commit standard for all changes (see Commit Standards section).

9. Never override the human's instructions, or any content in this AWP.

10. Use numbers to reference changes in this AWP. Format: 1.1, 1.2, 1.3, etc.

11. Never use the word "AI" in any commit message.

12. Read this AWP.md and if exists the main README.md to understand the workflow and project goal.

13. If you see blockers or have suggestions, document it in Unplanned Tasks section and notify human.

14. Always respect human oversight and approval gates.

15. Never make critical business decisions without human approval.

16. Always document your reasoning and decisions.

17. Follow the commit standard and reference step numbers.

18. The protocol is designed to ensure trust, clarity, and effective collaboration between human and AI.

## Core Principles

### No Improvisation - Human Decisions Required

**Critical Principle**: AI agents must NOT improvise, assume, or make decisions beyond what is explicitly documented. When information is missing, unclear, or requires a decision, AI must ask humans for guidance rather than guessing.

**When to Ask Humans**:
- Missing information in task description, requirements, or documentation
- Unclear acceptance criteria or ambiguous instructions
- Design decisions not specified in `docs/technology.md` or task files
- Scope questions (is this feature required or optional?)
- Trade-offs between multiple valid approaches
- Any decision that could affect other tasks or architecture

**When AI Can Proceed**:
- Information is explicitly documented in task files, `docs/requirements.md`, `docs/technical-specs.md`, or `docs/technology.md`
- Decision is clearly specified (e.g., "use JWT" not "use JWT or OAuth2")
- Minor implementation details that don't affect scope or architecture
- Code organization within documented patterns

**Documentation Sources** (in priority order):
1. Task file (task-X-Y.md) - step-by-step instructions and acceptance criteria
2. `docs/requirements.md` - original assignment requirements
3. `docs/technical-specs.md` - structured restatement of requirements
4. `docs/technology.md` - technology decisions and rationale
5. `docs/architecture.md` - system architecture and design choices

If information is not found in these sources, **ask humans** rather than making assumptions.

## Core Workflow Commands

### `awp check`
**Purpose**: Review AWP.md and project-backlog.md to determine the current actionable step.

**When to use**: 
- At the start of a work session
- When unsure what to work on next
- After completing a task

**Actions**:
1. Review `agentic-sdlc/AWP.md` (this file)
2. Review `agentic-sdlc/project-backlog.md` to see planned tasks
3. Identify the next actionable task (check dependencies, priority, status)
4. Report the current actionable step

### `awp update`
**Purpose**: Review README.md and AWP.md, update documentation, check for blockers.

**When to use**:
- Before starting a new task
- When documentation needs updating
- When checking for blockers or dependencies

**Actions**:
1. Review `README.md` and `agentic-sdlc/AWP.md`
2. Update any relevant documentation
3. Check for blockers (missing dependencies, unclear requirements)
4. Update task status if needed

### `awp commit`
**Purpose**: Commit changes using commit standards with step references.

**When to use**:
- After completing a task or significant work
- Before moving to the next task
- When changes are ready to be committed

**Actions**:
1. Review all changes made
2. Create commit message following standards:
   - Format: `type(scope): description [task-X-Y]`
   - Include task reference (e.g., `[task-3-3]`)
   - Be descriptive but concise
3. Stage and commit changes
4. Optionally push to remote

**Commit Standards**:
- `feat(scope): description [task-X-Y]` - New feature
- `fix(scope): description [task-X-Y]` - Bug fix
- `docs(scope): description [task-X-Y]` - Documentation
- `refactor(scope): description [task-X-Y]` - Code refactoring
- `test(scope): description [task-X-Y]` - Tests
- `chore(scope): description [task-X-Y]` - Maintenance

### `awp next`
**Purpose**: Move to the next actionable step only after update and commit are complete.

**When to use**:
- After `awp update` and `awp commit` are complete
- When ready to start the next task

**Actions**:
1. Verify `awp update` is complete (docs updated, blockers checked)
2. Verify `awp commit` is complete (changes committed)
3. Identify next actionable task from backlog
4. Update task status in backlog (mark previous as completed, mark next as in progress)
5. Begin work on next task

### `awp handoff`
**Purpose**: Transfer task ownership between human and AI.

**When to use**:
- When switching between human and AI work
- When pausing work on a task
- When resuming work on a task

**Actions**:
1. Document current state of task
2. Note what's been completed
3. Note what remains to be done
4. Document any blockers or questions
5. Update task status appropriately

## Task Lifecycle

### Starting a Task

1. **Check dependencies**: Ensure all prerequisite tasks are completed
2. **Read task file**: Review the full task description, acceptance criteria, and sub-tasks
3. **Review requirements**: Check `docs/requirements.md` and `docs/technical-specs.md` for context
4. **Update status**: Mark task as `[x] In Progress` in the task file
5. **Begin implementation**: Follow step-by-step instructions in task description

### Working on a Task

1. **Follow step-by-step instructions**: Use the detailed steps in the task description
2. **Check acceptance criteria**: Regularly verify progress against acceptance criteria
3. **Update task notes**: Document any decisions, blockers, or deviations
4. **Test as you go**: Run tests and verify functionality incrementally

### Completing a Task

1. **Verify all acceptance criteria**: Ensure all criteria are met
2. **Run tests**: Execute all relevant tests and ensure they pass
3. **Update task status**: Mark task as `[x] Completed` in the task file
4. **Update backlog**: Move task from "Planned" to "Completed" in `project-backlog.md`
5. **Commit changes**: Use `awp commit` with task reference
6. **Document completion**: Note any follow-up work or related tasks

## Task Status Values

- `[ ] Pending` - Task not yet started
- `[x] In Progress` - Task currently being worked on
- `[x] Completed` - Task finished and verified
- `[ ] Blocked` - Task cannot proceed due to dependencies or blockers
- `[ ] Deferred` - Task intentionally postponed

## Handling Issues

When encountering issues while working on a task, follow this structured approach:

### Types of Issues

1. **Blockers/Dependencies**
   - Prerequisite task not completed
   - External dependency unavailable
   - Missing information or documentation

2. **Unclear Requirements**
   - Task description is ambiguous
   - Acceptance criteria are unclear
   - Requirements conflict with each other

3. **Implementation Problems**
   - Task description doesn't match technical reality
   - Step-by-step instructions are incorrect
   - Implementation hints are outdated or wrong

4. **Scope Questions**
   - Feature seems out of scope
   - Task requires work beyond requirements
   - Missing functionality needed for task

5. **Technical Problems**
   - Tests failing unexpectedly
   - Errors or bugs encountered
   - Performance or security concerns

6. **Design Decisions**
   - Task doesn't specify a required choice
   - Multiple valid approaches exist
   - Trade-offs need to be made

### Documenting Issues

When you encounter an issue:

1. **Document in task file**:
   - Add to the task file's "Notes" section
   - Format: `**Issue [Type]**: Description of issue. Impact: [what's affected]. Resolution: [if known] or [needs decision/escalation]`
   - Include specific examples or error messages if applicable

2. **Update task status**:
   - If blocked: Change status to `[ ] Blocked`
   - If needs clarification: Keep `[x] In Progress` but document the question
   - If can proceed with decision: Document decision in notes, continue work

3. **Example issue documentation**:
   ```markdown
   ## Notes
   **Issue [Unclear Requirements]**: Task description mentions "OIDC/OAuth2 or JWT" but doesn't specify which to choose. 
   Impact: Cannot proceed with implementation without decision. 
   Resolution: Need to decide based on project constraints (time, complexity). Recommendation: JWT for simplicity.
   ```

### Decision Framework

**CRITICAL**: When in doubt, **ask humans**. It's better to ask than to make wrong assumptions.

**Escalate to Human** (ask for clarification/decision):
- **Missing information** in task description, requirements, or documentation
- **Unclear requirements** or ambiguous acceptance criteria
- **Design decisions** not specified in `docs/technology.md` or task files
- **Scope questions** (is this feature required or optional?)
- **Trade-offs** between multiple valid approaches
- **Security concerns** that need human review
- **Architecture decisions** that significantly impact other tasks
- **Blockers** that prevent any progress
- **Technology choices** not documented in `docs/technology.md`
- **Any decision** where multiple valid options exist and choice isn't specified

**Make Decision and Document** (proceed with documented choice - only if explicitly documented):
- **Library/framework choices** explicitly specified in `docs/technology.md` (e.g., "use FastAPI" not "use FastAPI or Flask")
- **Code organization** following documented patterns in task files
- **Minor implementation details** explicitly mentioned in task instructions
- **Error handling patterns** specified in task description or architecture docs

**When NOT to make decisions**:
- If `docs/technology.md` says "To be decided during implementation" → **ask human**
- If task says "choose between X or Y" → **ask human** (unless recommendation is clear in docs)
- If requirements are ambiguous → **ask human**
- If information is missing → **ask human**

**Update Task Description** (if clearly wrong):
- Step-by-step instructions are incorrect
- Implementation hints reference wrong libraries
- File paths or structure are outdated
- Only if you're certain it's an error (not a design choice)

### Issue Resolution Process

1. **Identify issue**: Clearly describe what the problem is
2. **Assess impact**: Determine if it blocks progress or just needs a decision
3. **Document**: Add to task notes with issue type and details
4. **Decide action**:
   - If blocker: Mark as `[ ] Blocked`, escalate if needed
   - If needs decision: Document options, make choice if safe, or escalate
   - If can proceed: Document decision, continue work
5. **Update status**: Change task status if needed
6. **Communicate**: Use `awp handoff` if switching to human, or commit with note if proceeding

### Escalation Guidelines

**When to escalate**:
- Security concerns or potential vulnerabilities
- Scope questions that could affect requirements compliance
- Ambiguous requirements that could lead to wrong implementation
- Blockers that prevent any progress
- Design decisions that significantly impact other tasks

**How to escalate**:
- Document issue clearly in task notes
- Use `awp handoff` to transfer to human
- In commit message, note the issue: `wip(auth): partial implementation [task-2-2] - blocked on auth method decision`
- Ask specific questions rather than open-ended ones

### Tracking Blockers

- **In task file**: Document blocker in "Notes" section, mark status as `[ ] Blocked`
- **In project-backlog.md**: Optionally add note in task description if blocker affects other tasks
- **In commits**: Reference blocker in commit message if work is partial: `wip(scope): description [task-X-Y] - blocked on [issue]`

## Best Practices

1. **Always check dependencies** before starting a task
2. **Update documentation** as you work (don't wait until the end)
3. **Commit frequently** with clear, descriptive messages
4. **Reference tasks** in commit messages for traceability
5. **Test incrementally** rather than waiting until completion
6. **Document decisions** and trade-offs in task notes
7. **Document issues immediately** when encountered (don't wait)
8. **Escalate early** if blocker prevents progress
9. **Make safe decisions** and document them rather than blocking on minor choices

## Integration with Project Backlog

- Tasks are organized hierarchically (parent tasks → child tasks)
- Each task file contains detailed instructions, acceptance criteria, and sub-tasks
- The `project-backlog.md` provides the high-level overview
- Task files in `tasks/planned/` contain the detailed implementation guidance

## AI Agent Guidelines

When working as an AI agent:

### Mandatory Practices

1. **Read documentation first**:
   - Always read the full task file before starting
   - Review `docs/requirements.md`, `docs/technical-specs.md`, and `docs/technology.md` for context
   - Check `docs/architecture.md` for design patterns

2. **Follow instructions precisely**:
   - Follow step-by-step instructions exactly as written
   - Do not skip steps or assume shortcuts
   - Do not add features not specified in requirements

3. **No assumptions or improvisation**:
   - **DO NOT** make decisions beyond what's documented
   - **DO NOT** assume missing information
   - **DO NOT** improvise solutions when requirements are unclear
   - **DO** ask humans for clarification when information is missing

4. **Verify before completing**:
   - Check all acceptance criteria before marking complete
   - Run tests and verify functionality
   - Ensure all requirements from task file are met

5. **Document everything**:
   - Document any deviations from instructions (with rationale)
   - Document decisions made (if within scope to make them)
   - Document blockers or missing information immediately

6. **Ask, don't guess**:
   - When information is missing: ask humans
   - When requirements are unclear: ask humans
   - When design decisions are needed: ask humans
   - When scope is ambiguous: ask humans

7. **Use proper workflow**:
   - Use `awp commit` with proper task references
   - Use `awp handoff` when transferring to humans
   - Update task status appropriately

## Human Developer Guidelines

When working as a human developer:

1. Use `awp check` to find next task.
2. Use `awp update` before starting work.
3. Use `awp commit` after completing work.
4. Use `awp next` to move to next task.
5. Use `awp handoff` when switching with AI.
6. Review AI work before accepting commits.
7. Reference the step in every commit.
8. Update AWP.md as the project progresses.
9. Check off each item as you complete it.
10. Respect human-AI collaboration boundaries.

## Unplanned Tasks

When unplanned work is identified (new features, bug fixes, improvements, or scope changes), it must be documented here:

1. **Document in Unplanned Tasks**: Add to this section with task ID format `U-X` or `U-X-Y`.
2. **Notify Human**: Always notify the human when adding unplanned tasks.
3. **Get Approval**: Unplanned tasks require human approval before implementation.
4. **Track in Backlog**: Unplanned tasks should also be added to `project-backlog.md` in the "Unplanned Tasks" section.
5. **Reference in Commits**: When working on unplanned tasks, reference them as `[U-X]` or `[U-X-Y]` in commit messages.

**Current Unplanned Tasks**:
- _None yet. Any scope beyond `docs/requirements.md` should be tracked here with `U-` IDs._

## Unplanned Tasks Standard

_Standard for measuring what was 'overvibed' - to be defined._

## Commit Standard

Format: `type(scope step): subject`

**Types**: feat, fix, docs, test, chore  
**Rules**: Reference step number, imperative mood, concise  
**Examples**: `feat(api 2.1): add endpoint`, `docs(readme 3.2): update usage`  

**Note**: Never use "AI" in commit messages (AWP 1.11).

## Human Notes

1. Reference the step in every commit.
2. Update this file as the project progresses.
3. Check off each item as you complete it.
4. Respect human-AI collaboration boundaries.

