# Task ID: 11.3
# Title: Add Docker Compose configuration
# Status: [ ] Pending
# Priority: high
# Owner: Full Stack Dev
# Estimated Effort: 3h

## Description
Add Docker Compose configuration to run API, worker, database, and frontend locally as required by the assignment, per `docs/requirements.md` section "Deliverables".

**Step-by-step:**
1. Review deliverable requirements from task 11.1 (Docker Compose for API, worker, database, frontend).
2. Create `docker-compose.yml` file in project root:
   - Define services: `api`, `worker`, `database`, `frontend`.
   - Define networks: `backend-network` (for API, worker, database), `frontend-network` (for frontend, API).
   - Define volumes: database data, uploads (if using local filesystem for attachments).
3. Configure database service:
   - Use PostgreSQL or MySQL image (e.g., `postgres:15` or `mysql:8`).
   - Set environment variables: `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` (use `.env` file, not hardcoded).
   - Expose port: `5432` (PostgreSQL) or `3306` (MySQL).
   - Add volume for data persistence: `postgres_data:/var/lib/postgresql/data`.
4. Configure API service:
   - Build from `backend/Dockerfile` or use Python base image.
   - Set environment variables: database connection, Redis connection, JWT secret, etc. (use `.env` file).
   - Expose port: `8000` (or chosen port).
   - Depends on: `database`, `redis` (if using Redis for rate limiting).
   - Add volume for code: `./backend:/app` (development) or copy code (production).
5. Configure worker service:
   - Build from `backend/Dockerfile` (same as API) or use Python base image.
   - Set environment variables: same as API (database, Redis, etc.).
   - Command: run worker process (e.g., `python -m worker.main`).
   - Depends on: `database`, `redis`.
   - Add volume for code: `./backend:/app` (development) or copy code (production).
6. Configure frontend service:
   - Build from `frontend/Dockerfile` or use Node.js base image.
   - Set environment variables: API URL (e.g., `REACT_APP_API_URL=http://api:8000`).
   - Expose port: `3000` (or chosen port).
   - Depends on: `api` (for API calls).
   - Add volume for code: `./frontend:/app` (development) or copy code (production).
7. Configure Redis service (if using for rate limiting):
   - Use `redis:7` image.
   - Expose port: `6379`.
   - Add volume for data persistence: `redis_data:/data`.
8. Create `.env.example` file:
   - Document all required environment variables.
   - Include database credentials, JWT secret, Redis connection, etc.
9. Create `README.md` or `INSTALL.md`:
   - Document how to run: `docker compose up`.
   - Document how to access services (API: `http://localhost:8000`, Frontend: `http://localhost:3000`).
   - Document environment variables setup.
10. Test Docker Compose setup:
    - Run `docker compose up` and verify all services start.
    - Verify services can communicate (API can connect to database, frontend can call API).
    - Verify health checks work (call `/health` endpoint).
    - Test basic functionality (create task, login, etc.).

**Implementation hints:**
- Use `docker-compose.yml` (v3 format) for service definitions.
- Use `.env` file for environment variables (not hardcoded in Compose file).
- Use Docker networks for service communication (internal network, not exposed ports).
- Use volumes for data persistence (database data, uploads).
- Create separate `docker-compose.dev.yml` and `docker-compose.prod.yml` if needed (optional).

## Dependencies
- [ ] Task ID: 3.3 (API must exist)
- [ ] Task ID: 6.3 (Worker must exist)
- [ ] Task ID: 10.2 (Frontend must exist)

## Testing Instructions
- Run `docker compose up` and verify all services start and can communicate as expected:
  - Verify all services start without errors (check logs).
  - Verify API can connect to database (check API logs, test health endpoint).
  - Verify frontend can call API (open frontend in browser, test API calls).
  - Verify worker can connect to database (check worker logs, test reminder job).
  - Test basic functionality (login, create task, view task).
- Test with `docker compose down` and `docker compose up` again (verify data persistence if using volumes).

## Security Review
- Ensure no secrets are hardcoded in Compose files:
  - Use `.env` file for secrets (database passwords, JWT secrets, etc.).
  - Add `.env` to `.gitignore` (don't commit secrets).
  - Document required environment variables in `.env.example`.

## Risk Assessment
- Incomplete or broken Compose setup will frustrate reviewers and hinder local testing.
- Missing environment variables can cause services to fail.
- Network configuration issues can prevent service communication.

## Acceptance Criteria
- [ ] Docker Compose file(s) exist and define API, worker, DB, and frontend services (all services configured).
- [ ] Services can be started and accessed locally via Compose (all services start, can communicate, accessible via ports).
- [ ] Environment variables documented (`.env.example` exists, required variables listed).
- [ ] Install/run instructions documented (README or INSTALL.md explains how to run).

## Definition of Done
- [ ] Compose configuration committed (`docker-compose.yml` exists, services defined).
- [ ] Environment variables documented (`.env.example` exists).
- [ ] Install/run instructions documented (README or INSTALL.md).
- [ ] Basic manual test shows system is reachable via Docker Compose (all services start, can communicate, basic functionality works).
- [ ] All acceptance criteria met.

## Measurable Outcomes
- **Verification Criteria**: `docker compose up` brings up a working stack (all services start, can communicate, accessible).
- **Observable Outcomes**: Docker Compose file exists, services can be started, system works locally.

## Notes
Supports the "Docker compose for local run" deliverable. This task makes the application easy to run and evaluate.

## Strengths
Makes the application trivial to run and evaluate. Enables reviewers to test the system easily.

## Sub-tasks (Children)
- [ ] Review deliverable requirements from task 11.1 (Docker Compose for API, worker, database, frontend).
- [ ] Create `docker-compose.yml` file (define services: api, worker, database, frontend, redis if needed).
- [ ] Configure database service (PostgreSQL/MySQL image, environment variables, volumes, ports).
- [ ] Configure API service (build from Dockerfile, environment variables, depends on database/redis, ports).
- [ ] Configure worker service (build from Dockerfile, environment variables, depends on database/redis, command).
- [ ] Configure frontend service (build from Dockerfile, environment variables, depends on api, ports).
- [ ] Configure Redis service (if using for rate limiting, image, volumes, ports).
- [ ] Create `.env.example` file (document all required environment variables).
- [ ] Create install/run instructions (README or INSTALL.md, how to run, how to access services).
- [ ] Test Docker Compose setup (run `docker compose up`, verify all services start, can communicate, basic functionality works).

## Completed
[ ] Pending / [ ] Completed


