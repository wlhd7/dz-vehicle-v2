# Implementation Plan: UI Refactor & Borrowing/Returning Logic

## Technical Context
- **Frontend**: Vue 3 (Composition API) with Element Plus.
- **Backend**: Python with FastAPI and SQLAlchemy.
- **State Management**: Local component state in `Dashboard.vue` for selections.
- **Business Logic**: Enforced in `AssetService`.

## Constitution Check
- [x] **Article I (Library-First)**: Business logic for limits and batch returns will be implemented in `AssetService` (library).
- [x] **Article II (CLI Interface)**: Functionality will be accessible via CLI; tasks added to update `cli.py`.
- [x] **Article III (Test-First)**: Unit tests for batch returns and limits will be written before implementation.
- [x] **Article VIII (Framework Trust)**: Using Element Plus features directly for table rendering and styling.

## Design Phase Gates
1. **Batch Return Atomicity**: Ensure all assets are updated in a single transaction. (PASSED)
2. **Selection State Integrity**: Ensure the frontend state accurately reflects the "max 1 of each" rule. (PASSED)

## Phase 0: Research
- [x] Map "Vehicle" to `KEY` asset type.
- [x] Plan batch return API and service method.
- [x] Design frontend row-selection logic.

## Phase 1: Design & Contracts
- [x] Created `data-model.md` for state transitions.
- [x] Created `contracts/api-contract.md` for batch return.
- [x] Created `quickstart.md`.
- [ ] Update agent context.

## Phase 2: Implementation (Tasks to be generated)
- [ ] Implement backend batch return and borrowing limits.
- [ ] Implement frontend UI refactor in `Dashboard.vue`.
- [ ] Update and run tests.
