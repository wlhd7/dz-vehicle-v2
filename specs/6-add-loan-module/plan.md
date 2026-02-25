# Implementation Plan - Inventory Loan Module

## Technical Context
- **Project Structure**: Python library (`vehicle_asset_lib`) with FastAPI (`api`) and Vue 3 frontend (`frontend`).
- **Data Store**: SQLite (via SQLAlchemy) as seen in `src/vehicle_asset_lib/db.py`.
- **Existing Services**: `AssetService` handles borrowing/returning; `MonitoringService` handles OTP checks.
- **UI Framework**: Vue 3 + Vite + TypeScript (found in `frontend/`).
- **Translation**: i18n support found in `frontend/src/i18n/`.

## Constitution Check
- **Article I (Library-First)**: New logic for listing active loans will be added to `AssetService` in the library.
- **Article II (CLI Interface)**: `cli.py` will be updated to support the new `loans` command.
- **Article III (Test-First)**: Unit tests for `AssetService.list_active_loans` will be written and verified as failing before implementation.
- **Article IX (Integration-First)**: Tests will use the real database schema (SQLite) rather than mocks where feasible.

## Phase 0: Outline & Research
- **Research 0.1**: Determine if `AssetService.list_assets` can be extended or if a new method is better for "active loans" (Identifier, Type, User).
- **Research 0.2**: Verify existing sorting capabilities in the repository layer.
- **Research 0.3**: Identify the best place in the frontend to inject the 'Loan' tab visibility logic (likely `Dashboard.vue` or a dedicated Inventory component).

## Phase 1: Design & Contracts
- **Data Model**: No schema changes required. `Asset` already has `current_holder_id` and `status`. `TransactionLog` has `timestamp`.
- **Interface Contracts**:
  - **Backend**: `GET /assets/loans` returning `List[LoanRecord]`.
  - **CLI**: `vehicle-asset loans` returning JSON/Table.
- **Agent Context Update**: Run `update-agent-context.sh` after design artifacts are ready.

## Phase 2: Implementation (Summary)
- **Step 1**: Add `list_active_loans` to `AssetService` with descending timestamp sort from `TransactionLog`.
- **Step 2**: Update `api/main.py` with `GET /assets/loans`.
- **Step 3**: Implement frontend `Loan` tab with conditional visibility (hide if empty) and auto-refresh on click.
- **Step 4**: Add 'Loan' (借出) to `zh-cn.json`.
