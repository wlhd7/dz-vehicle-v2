# Implementation Plan: Unattended Vehicle Asset Pickup

## Technical Context
- **Target**: Standalone Python Library + CLI (Articles I & II).
- **Storage**: SQLite (Article IX).
- **Validation**: Strict TDD with `pytest` (Article III).
- **Framework**: Typer for CLI, SQLAlchemy for ORM (Article VIII).

## Constitution Check
- [x] **Article I (Library-First)**: Core logic will be in `src/vehicle_asset_lib/`.
- [x] **Article II (CLI-Interface)**: `vehicle-asset` command will support JSON.
- [x] **Article III (Test-First)**: Implementation starts with `tests/`.
- [x] **Article VII (Minimal Structure)**: Single repository, 3-tier structure (CLI, Service, DB).
- [x] **Article VIII (Framework Trust)**: Using standard SQLAlchemy and Typer patterns.
- [x] **Article IX (Integration-First)**: Using real SQLite for testing.

## Implementation Phases

### Phase 0: Setup & Research
- [x] Identify tech stack (Python, SQLite, Typer).
- [x] Document research in `research.md`.

### Phase 1: Design & Contracts
- [x] Define data model in `data-model.md`.
- [x] Define CLI contract in `contracts/cli-contract.md`.
- [x] Create `quickstart.md`.
- [x] Update agent context.

### Phase 2: Core Library & TDD (Skeleton)
1. **Initialize Project Structure**:
   - `src/vehicle_asset_lib/`
   - `tests/`
2. **Define Schema**: Implement SQLAlchemy models.
3. **Write Failing Tests**: Define user verification and pickup logic tests.

### Phase 3: Implementation (Green Phase)
1. **Service Layer**: Implement logic for verification, asset selection, and OTP consumption.
2. **CLI Layer**: Implement Typer commands matching the contract.
3. **Alerting**: Implement the <30 OTP threshold notification logic.

### Phase 4: Frontend & API (Web Interface)
1. **FastAPI Bridge**: Expose the core library functions via REST endpoints.
2. **Vue 3 Application**:
   - Authentication view (Name + ID digits).
   - Asset Selection/Return view.
   - Admin Dashboard for asset and OTP management.
3. **TypeScript Integration**: Ensure type safety between backend models and frontend state.
4. **Element Plus UI**: Leverage Element Plus components for a rapid, responsive, and professional user interface.

### Phase 5: Validation
1. Run full test suite (pytest + Vitest).
2. End-to-end verification via browser and CLI.
