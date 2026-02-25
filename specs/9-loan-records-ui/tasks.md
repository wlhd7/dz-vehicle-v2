# Tasks: Loan Records Panel

This feature adds a "Loan Records" (领取记录) panel to the login screen to provide transparency into usage history. It involves a backend service for pairing pickup and return events from transaction logs, a new API endpoint, and a dedicated frontend view with filtering and navigation back to login.

## Implementation Strategy
- **MVP First**: Focus on the core backend logic for pairing records and the basic frontend list.
- **Incremental Delivery**: Start with service-level logic and CLI verification, then move to API, and finally the UI components and routing.
- **TDD-Ready**: Unit tests and integration tests are included in each phase to ensure correctness.

## Dependencies
- Phase 2 must be complete before Phase 3.
- Phase 3 must be complete before Phase 4.
- Phase 4 must be complete before Phase 5.
- Phase 5 must be complete before Phase 6.

## Phase 1: Setup
Goal: Initialize the feature environment.
- [ ] T001 Initialize branch environment by running `bash .specify/scripts/bash/check-prerequisites.sh`
- [ ] T002 Update local agent context with technology stack from plan.md

## Phase 2: Foundational Logic (Backend)
Goal: Implement the core logic for pairing pickup and return events.
- [ ] T003 [P] Create unit tests for `list_loan_records` in `tests/test_assets.py` (Verify FAIL)
- [ ] T004 Implement `list_loan_records` method with correlated subquery in `src/vehicle_asset_lib/services/assets.py`
- [ ] T005 Verify unit tests pass for `list_loan_records` in `tests/test_assets.py`
- [ ] T006 [P] Add `loan-records` command to `src/vehicle_asset_lib/cli.py` and verify via CLI

## Phase 3: [US1] Public API Endpoint
Goal: Expose the loan records via a public REST API.
- [ ] T007 [P] [US1] Define `LoanRecord` Pydantic model in `src/vehicle_asset_lib/api/main.py`
- [ ] T008 [P] [US1] Create integration tests for `GET /assets/loan-records` in `tests/test_api_loan.py` (Verify FAIL)
- [ ] T009 [US1] Implement `GET /assets/loan-records` endpoint in `src/vehicle_asset_lib/api/main.py`
- [ ] T009.1 [US1] Implement `GET /assets/identifiers` to provide all unique identifiers for UI filters in `src/vehicle_asset_lib/api/main.py`
- [ ] T010 [US1] Verify integration tests pass in `tests/test_api_loan.py`

## Phase 4: [US2] Frontend Infrastructure & State
Goal: Prepare the frontend types, translations, and API client.
- [ ] T011 [P] [US2] Add `LoanRecord` interface to `frontend/src/types/api.ts`
- [ ] T012 [P] [US2] Implement `getLoanRecords` in `frontend/src/api/client.ts`
- [ ] T013 [P] [US2] Add UI translations for "Loan Records" (领取记录), "No Records" (无记录), and table headers to `frontend/src/i18n/locales/zh-cn.json`

## Phase 5: [US3] Loan Records View & Navigation
Goal: Create the dedicated view and link it from the login page.
- [ ] T014 [P] [US3] Create `frontend/src/views/LoanRecords.vue` with basic list and "Back to Login" button
- [ ] T015 [US3] Register `/loan-records` route in `frontend/src/router/index.ts`
- [ ] T016 [US3] Add "领取记录" link to `frontend/src/views/Login.vue` using the specified layout: `领取记录 | 车辆信息 | 管理面板` and verify navigation
- [ ] T017 [US3] Verify "Back to Login" functionality in `frontend/src/views/LoanRecords.vue`

## Phase 6: [US4] Filtering & Pagination
Goal: Implement Excel-style column header filtering and pagination.
- [ ] T018 [P] [US4] Implement integrated "类型" (Type) filter in `el-table-column` in `frontend/src/views/LoanRecords.vue`
- [ ] T019 [P] [US4] Implement integrated "标识符" (Identifier) filter in `el-table-column` in `frontend/src/views/LoanRecords.vue`
- [ ] T019.1 [US4] Expand filter click area to the entire column header title in `frontend/src/views/LoanRecords.vue`
- [ ] T020 [US4] Implement pagination (8 items per page) using `el-pagination` in `frontend/src/views/LoanRecords.vue`
- [ ] T021 [US4] Implement "无记录" (No records) empty state handling in `frontend/src/views/LoanRecords.vue`
- [ ] T022 [US4] Apply YY-MM-DD HH:mm date formatting in `frontend/src/views/LoanRecords.vue`

## Phase 7: Polish & Validation
Goal: Final project-wide validation.
- [ ] T022 Run all backend tests: `pytest`
- [ ] T023 Perform manual end-to-end verification following `quickstart.md`
- [ ] T024 Perform final linting and formatting of all modified files

## Parallel Execution Opportunities
- T003 (Backend Tests) can run in parallel with T007 (API Schema) and T011 (Frontend Types).
- T011, T012, and T013 (Frontend Setup) are independent and can be executed simultaneously.
- T018, T019, and T021 (UI Logic) can be implemented in parallel within the same view.
