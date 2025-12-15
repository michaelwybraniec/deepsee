# Task Tracker – Technical Assessment

This repository contains the implementation of the Task Tracker application for the Full Stack Developer technical assessment.

- **[Requirements (source)](docs/requirements.md)** - Original assignment (source of truth)
- **[Technical spec (structured restatement)](docs/technical-specs.md)** - Structured restatement of requirements
- **[Architecture overview & diagrams](docs/architecture.md)** - System architecture and design
- **[Technology stack & decisions](docs/technology.md)** - Technology decisions and rationale
- **[Implementation suggestions (optional, good practice)](docs/suggestions.md)** - Optional best practices
- **Backend**: Python (API + worker), following Clean Architecture principles.
- **Frontend**: React-based UI for authentication and task management.

## Getting Started

### Documentation Structure

```text
docs/
├── requirements.md          # Original assignment (source of truth)
├── technical-specs.md      # Structured restatement of requirements
├── architecture.md          # System architecture & design
├── technology.md            # Technology decisions & rationale
└── suggestions.md           # Optional best practices

agentic-sdlc/
├── AWP.md                   # Agentic Workflow Protocol
├── project-backlog.md       # Main backlog index
├── README.md                # Backlog structure guide
└── tasks/planned/           # Individual task files
```

**Documentation Flow**:

```text
requirements.md (source)
    ↓
technical-specs.md (structured)
    ↓
architecture.md (design)
    ↓
technology.md (decisions)
    ↓
tasks/ (implementation)
```

### Project Backlog & Workflow

This project uses an **Agentic SDLC** approach with a structured backlog and workflow protocol:

- **Backlog**: See `agentic-sdlc/project-backlog.md` for all planned tasks
- **Workflow**: See `agentic-sdlc/AWP.md` for the Agentic Workflow Protocol (AWP)
- **Task details**: Individual task files in `agentic-sdlc/tasks/planned/` contain step-by-step implementation instructions

Tasks are organized hierarchically and follow the AWP workflow (`awp check`, `awp update`, `awp commit`, `awp next`, `awp handoff`) for consistent progress tracking and collaboration between humans and AI agents.
