# Tasks: Security Access Control for CLI and API

## Phase 1: Setup
- [X] T001 Install `python-dotenv` and update `pyproject.toml`
- [X] T002 Create initial test file `tests/test_security.py` with failing placeholders

## Phase 2: Foundational
- [X] T003 [P] Implement centralized authentication service in `src/vehicle_asset_lib/services/auth.py`
- [X] T004 [P] Create `.env.example` with `ADMIN_SECRET` placeholder

## Phase 3: CLI Access Control (US1 & US2)
Goal: Ensure all administrative CLI commands are protected by `ADMIN_SECRET`.
Test Criteria: `vehicle-asset admin` commands fail without `ADMIN_SECRET` and pass with it.

- [X] T005 [US1] Write failing CLI security tests in `tests/test_security.py` using `typer.testing.CliRunner`
- [X] T006 [US1] Implement `@admin_app.callback()` in `src/vehicle_asset_lib/cli.py` to validate `ADMIN_SECRET`
- [X] T007 [US1] Load `.env` in `src/vehicle_asset_lib/cli.py` using `python-dotenv`
- [X] T008 [US1] Verify CLI security tests pass

## Phase 4: API Access Control (US3 & US4)
Goal: Ensure all `/admin` API endpoints are protected by `X-Admin-Secret` header.
Test Criteria: Requests to `/admin/*` return 403 without header and 200/201 with correct header.

- [X] T009 [US3] Write failing API security tests in `tests/test_security.py` using `fastapi.testclient.TestClient`
- [X] T010 [US3] Implement `verify_admin_access` dependency in `src/vehicle_asset_lib/api/auth.py`
- [X] T011 [US3] Apply `verify_admin_access` dependency to admin routes in `src/vehicle_asset_lib/api/main.py`
- [X] T012 [US3] Verify API security tests pass

## Phase 5: Polish & Cross-Cutting
- [X] T013 Update `README.md` with instructions on setting `ADMIN_SECRET` and using the header
- [X] T014 Ensure consistent error messages between CLI and API
- [X] T015 Perform final end-to-end verification of all admin commands and endpoints

## Dependencies
- Phase 2 depends on Phase 1
- Phase 3 depends on Phase 2
- Phase 4 depends on Phase 2
- Phase 5 depends on all previous phases

## Parallel Execution Examples
- T003 and T004 can be done in parallel.
- CLI implementation (Phase 3) and API implementation (Phase 4) can be done in parallel once T003 is complete.

## Implementation Strategy
- TDD approach: Write failing tests for both CLI and API before implementing the logic.
- MVP: Protect CLI first as it's the primary administrative tool.
- Centralized logic: Keep the secret validation logic in a shared service to ensure consistency between CLI and API.
