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

### Option 1: Docker Compose (Recommended)

**Prerequisites:**
- Docker and Docker Compose installed

**Steps:**
1. Copy environment file:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` and set your values (especially `JWT_SECRET_KEY` with at least 32 characters)
3. Start all services:
   ```bash
   docker compose up
   ```
4. Access the application:
   - **Frontend**: http://localhost:5173
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs (Swagger UI)
   - **ReDoc**: http://localhost:8000/redoc

**Services:**
- `api` - Backend API (port 8000)
- `worker` - Background worker for reminders
- `database` - PostgreSQL database (port 5432)
- `redis` - Redis for rate limiting (port 6379)
- `frontend` - React frontend (port 5173)

**Stop services:**
```bash
docker compose down
```

**Stop and remove volumes (clean slate):**
```bash
docker compose down -v
```

### Option 2: Manual Setup

**Start Backend:**
```bash
npm run start:backend
```
Or manually:
```bash
cd backend
source .venv/bin/activate  # On macOS/Linux
uvicorn api.main:app --reload
```

**Start Frontend:**
```bash
npm run start:frontend
```
Or manually:
```bash
cd frontend
npm run dev
```

**Start Both (requires two terminals):**
```bash
# Terminal 1 - Backend
npm run start:backend

# Terminal 2 - Frontend  
npm run start:frontend
```

The backend will be available at **http://localhost:8000** and the frontend at **http://localhost:5173**.

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
