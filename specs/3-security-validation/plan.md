# Implementation Plan: Security Access Control for CLI and API

## Technical Context
- **Language/Framework**: Python (Typer for CLI, FastAPI for API).
- **Security Mechanism**: Shared secret (`ADMIN_SECRET`) via environment variables.
- **CLI Implementation**: Typer callback on the `admin` app group to intercept all administrative commands.
- **API Implementation**: FastAPI `Header` dependency applied to all `/admin` routes.
- **Dependencies**: `python-dotenv` for loading secrets from `.env` files.

### Unknowns
- [ ] Best way to handle the secret in `pytest` to ensure isolation between tests that need it and those that don't.
- [ ] Whether to provide a default secret for development or strictly enforce it.

## Constitution Check

| Principle | Status | Justification |
|-----------|--------|---------------|
| **Article I: Library-First** | ✅ | Validation logic will be placed in `vehicle_asset_lib.services.auth` or similar. |
| **Article II: CLI Interface** | ✅ | The CLI will be updated to respect the security context. |
| **Article III: Test-First** | ✅ | New tests in `tests/test_security.py` will be written to confirm rejection of unauthorized access. |
| **Article VII: Simplicity** | ✅ | Using standard environment variables and headers; no complex OAuth/JWT needed for this prototype. |
| **Article VIII: Framework Trust** | ✅ | Using Typer callbacks and FastAPI dependencies directly. |
| **Article IX: Integration-First** | ✅ | Tests will use real environment variables and actual API requests. |

## Phase 0: Outline & Research
- Decisions will be documented in `research.md`.
- **Research Tasks**:
  1. Research Typer global callbacks for subcommand groups to ensure all `admin` commands are covered.
  2. Research FastAPI dependency injection for route groups (APIRouter) to protect all admin endpoints at once.
  3. Research `python-dotenv` integration patterns for FastAPI and Typer.

## Phase 1: Design & Contracts
- **Data Model**: Update `data-model.md` to reflect configuration requirements (not necessarily DB schema).
- **Contracts**:
  - `specs/3-security-validation/contracts/cli-contract.md`: Define how `ADMIN_SECRET` must be passed.
  - `specs/3-security-validation/contracts/api-contract.md`: Define the `X-Admin-Secret` header requirement.
- **Quickstart**: Create `quickstart.md` with setup instructions for the secret.
- **Agent Context**: Update using `.specify/scripts/bash/update-agent-context.sh`.

## Phase 2: Implementation Strategy
- **Step 1**: Write failing tests for unauthorized CLI and API access.
- **Step 2**: Implement centralized auth logic in the library.
- **Step 3**: Integrate auth logic into Typer CLI.
- **Step 4**: Integrate auth logic into FastAPI.
- **Step 5**: Verify with tests (Red-Green cycle).
