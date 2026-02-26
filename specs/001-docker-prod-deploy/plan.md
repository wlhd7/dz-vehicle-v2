# Implementation Plan: Production Container Startup

**Branch**: `001-docker-prod-deploy` | **Date**: 2026-02-26 | **Spec**: `specs/001-docker-prod-deploy/spec.md`
**Input**: Feature specification from `specs/001-docker-prod-deploy/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Provide a production startup flow that packages the existing service for container-based deployment and exposes the public web UI at `124.70.179.238:8081` on the root path `/`, with documented steps and user-facing failure feedback.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.10+, TypeScript 5.9  
**Primary Dependencies**: FastAPI, Typer, SQLAlchemy, Pydantic, Vue 3, Vite, Element Plus, Nginx (frontend container)  
**Storage**: SQLite (via SQLAlchemy)  
**Testing**: pytest, pytest-asyncio, httpx, vitest  
**Target Platform**: Linux server (public IP `124.70.179.238`)  
**Project Type**: library + CLI + web-service + web-frontend  
**Performance Goals**: Service reachable within 5 minutes of startup completion  
**Constraints**: Public access on port `8081`, web UI served at root path `/`, user-facing failure message with likely cause  
**Scale/Scope**: Single production server deployment for the current application

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Article I: Library-First Principle**: Pass. No new business logic is introduced; existing library remains the core.
- **Article II: CLI Interface Mandate**: Pass. Existing CLI remains available; no new logic bypasses CLI requirements.
- **Article III: Test-First Imperative**: Pass. Any code changes will be preceded by tests and validated in red-first order.
- **Article IV-VI**: Not defined; no additional gates applied.
- **Article VII: Minimal Project Structure**: Pass. Two projects (backend package + frontend app).
- **Article VIII: Framework Trust**: Pass. Use existing framework features without new abstractions.
- **Article IX: Integration-First Testing**: Pass. Use real SQLite and live service checks in integration tests.

**Post-Phase 1 Re-check**: Pass. No design changes introduced new violations.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
src/
└── vehicle_asset_lib/
    ├── api/
    ├── cli/
    └── ...

tests/

frontend/
└── src/
```

**Structure Decision**: Keep the existing backend package under `src/` with tests under `tests/`, and the Vue frontend under `frontend/`.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
