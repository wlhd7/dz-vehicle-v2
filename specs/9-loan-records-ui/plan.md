# Implementation Plan: Loan Records Panel

**Feature**: Loan Records Panel
**Branch**: `9-loan-records-ui`

## Technical Context
- **Backend**: FastAPI with SQLAlchemy.
- **Frontend**: Vue 3 with Element Plus and Vue Router.
- **Data Source**: `TransactionLog` table joined with `Asset` and `User`.
- **Formatting**: `YY-MM-DD HH:mm` for timestamps.

## Constitution Check
- [x] Article I: Library-First (Logic in `AssetService`)
- [x] Article II: CLI Interface (Expose via `loan-records` CLI command)
- [x] Article III: Test-First (New tests in `tests/test_assets.py` and `tests/test_api_loan.py`)
- [x] Article VII: Minimal Project Structure (Existing FastAPI/Vue structure)
- [x] Article VIII: Framework Trust (Direct Vue Router and Element Plus usage)
- [x] Article IX: Integration-First (DB-backed tests)

## Phase 1: Backend Implementation

### Step 1.1: Service Layer
- Add `list_loan_records(limit=200)` to `AssetService` in `src/vehicle_asset_lib/services/assets.py`.
- Implement the correlated subquery to fetch `return_time`.

### Step 1.2: CLI Command
- Update `src/vehicle_asset_lib/cli.py` to include a `loan-records` command.

### Step 1.3: API Layer
- Define `LoanRecord` Pydantic model in `src/vehicle_asset_lib/api/main.py`.
- Add `GET /assets/loan-records` endpoint.
- Add `GET /assets/identifiers` endpoint to fetch all unique license plates and card IDs for filtering.

### Step 1.4: Testing (Red Phase)
- Add unit tests for `list_loan_records` in `tests/test_assets.py`.
- Add integration tests for `GET /assets/loan-records` in `tests/test_api_loan.py`.

## Phase 2: Frontend Implementation

### Step 2.1: API Client
- Add `getLoanRecords()` to `frontend/src/api/client.ts`.
- Update `frontend/src/types/api.ts` with `LoanRecord` interface.

### Step 2.2: Translations
- Add UI strings to `frontend/src/i18n/locales/zh-cn.json`.

### Step 2.3: New View
- Create `frontend/src/views/LoanRecords.vue`.
- Implement ElTable with columns: Identifier, Type, User, Loan Time, Return Time.
- Implement column-based filtering for Identifier and Type.
- Expand filter click area to cover the entire column header cell using CSS.
- Implement pagination (8 items per page).
- Implement "返回登录" link.

### Step 2.4: Routing
- Register `/loan-records` in `frontend/src/router/index.ts`.

### Step 2.5: Navigation
- Update `frontend/src/views/Login.vue` to include the `领取记录` link.

## Phase 3: Validation
- Run backend tests: `pytest`.
- Run frontend lint/build if applicable.
- Manual verification following `quickstart.md`.
