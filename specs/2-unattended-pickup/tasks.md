# Tasks: Unattended Vehicle Asset Pickup

## Phase 1: Setup
- [X] T001 Initialize Python project structure with `pyproject.toml` and `src/vehicle_asset_lib/`
- [X] T002 [P] Configure `pytest` and `pytest-asyncio` in `pyproject.toml`
- [X] T003 Initialize Vue 3 project with TypeScript and Element Plus in `frontend/`
- [X] T004 [P] Configure `vitest` for frontend testing in `frontend/vitest.config.ts`

## Phase 2: Foundational (Library & Data)
- [X] T005 [P] Write failing TDD tests for data models and state transitions in `tests/test_models.py`
- [X] T006 [P] Implement SQLAlchemy models for User, Asset, OTPPool, and TransactionLog in `src/vehicle_asset_lib/models.py`
- [X] T007 Implement database migration/initialization script for SQLite in `src/vehicle_asset_lib/db.py`
- [X] T008 [P] Create base `Repository` class for generic CRUD operations in `src/vehicle_asset_lib/repository.py`
- [X] T009 Implement Article II CLI entry point using Typer in `src/vehicle_asset_lib/cli.py`

## Phase 3: [US1] First-time User Pickup
**Goal**: User can verify identity, select assets, and receive an OTP.
- [X] T010 [US1] Write failing TDD tests for identity verification in `tests/test_verification.py`
- [X] T011 [US1] Implement `VerificationService.verify_user` matching admin whitelist in `src/vehicle_asset_lib/services/verification.py`
- [X] T012 [US1] Write failing TDD tests for asset pickup, OTP consumption, and exhaustion handling in `tests/test_pickup.py`
- [X] T013 [US1] Implement `AssetService.pickup` with OTP selection, status update, and "Block & Notify" exhaustion logic in `src/vehicle_asset_lib/services/assets.py`
- [X] T014 [US1] Implement "First-to-Click" concurrency logic in `AssetService.pickup` in `src/vehicle_asset_lib/services/assets.py`
- [X] T015 [US1] Add `verify`, `list`, and `pickup` commands to CLI in `src/vehicle_asset_lib/cli.py`

## Phase 4: [US2] Returning an Asset
**Goal**: User can return a held asset and receive a new OTP.
- [X] T016 [US2] Write failing TDD tests for asset return in `tests/test_return.py`
- [X] T017 [US2] Implement `AssetService.return_asset` generating a new OTP and updating status in `src/vehicle_asset_lib/services/assets.py`
- [X] T018 [US2] Add `return` command to CLI in `src/vehicle_asset_lib/cli.py`

## Phase 5: [US3] Admin Management
**Goal**: Admin can manage assets, users, and the OTP pool.
- [X] T019 [US3] Write failing TDD tests for admin services and monitoring in `tests/test_admin.py`
- [X] T020 [US3] Implement CRUD services for Asset and User whitelist in `src/vehicle_asset_lib/services/admin.py`
- [X] T021 [US3] Implement OTP pool seeding service in `src/vehicle_asset_lib/services/admin.py`
- [X] T022 [US3] Implement Low OTP threshold (<30) detection and dual notification (log + email placeholder) in `src/vehicle_asset_lib/services/monitoring.py`
- [X] T023 [US3] Add `admin` sub-commands to CLI in `src/vehicle_asset_lib/cli.py`

## Phase 6: Web API & Frontend Integration
**Goal**: Expose library via FastAPI and build the Vue 3 user interface.
- [X] T024 [P] Create FastAPI app and define REST endpoints in `src/vehicle_asset_lib/api/main.py`
- [X] T025 [P] Implement session management and persistent authentication logic in `src/vehicle_asset_lib/api/auth.py`
- [X] T026 Implement Vue 3 Login/Verification view with Element Plus in `frontend/src/views/Login.vue`
- [X] T027 [P] Implement Vue 3 Asset Dashboard (Pickup/Return) in `frontend/src/views/Dashboard.vue`
- [X] T028 Implement Vue 3 Admin Panel for Asset/OTP management in `frontend/src/views/Admin.vue`
- [X] T029 [P] Integrate API calls with `axios` and add TypeScript interfaces in `frontend/src/api/`

## Phase 7: Polish & Validation
- [X] T030 [P] Add global loading states and error notifications using Element Plus in `frontend/src/App.vue`
- [X] T031 Perform full integration test pass (CLI vs Web vs DB)
- [X] T032 Create final `README.md` with deployment instructions

## Dependencies
- Phase 2 must be complete before Phase 3.
- US1 (Phase 3) is the MVP and prerequisite for US2 (Phase 4).
- US3 (Phase 5) is required to seed the system with initial data for US1.

## Parallel Execution Examples
- [US1]: T011 (Verification) and T013 (Pickup Logic) can be developed in parallel after models are defined.
- [Web]: T026, T027, and T028 (Vue Views) can be developed in parallel once API contracts are finalized.
