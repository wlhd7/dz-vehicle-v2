# Tasks: Inventory Loan Module

## Implementation Strategy
The feature will be implemented incrementally. First, the backend service and API endpoint will be created to fetch active loans. Then, the frontend will be updated to display the "Loan" tab conditionally and render the data. Finally, CLI support and minor UI polish like translations and auto-refresh will be added.

## Phase 1: Setup
- [X] T001 Initialize the feature branch and verify environment in project root

## Phase 2: Foundational
- [X] T002 Define `LoanRecord` schema in `src/vehicle_asset_lib/models.py` or as a service return type
- [X] T003 [P] Create unit test for `list_active_loans` in `tests/test_assets.py` (Verify FAIL)
- [X] T004 Update `zh-cn.json` with new translation keys in `frontend/src/i18n/locales/zh-cn.json`

## Phase 3: [US1] View Loaned Items
Goal: Users can see a list of all currently loaned items with Identifier, Type, and User.

- [X] T005 [P] [US1] Implement `list_active_loans` logic in `src/vehicle_asset_lib/services/assets.py`
- [X] T006 [US1] Verify `list_active_loans` unit test passes in `tests/test_assets.py`
- [X] T007 [P] [US1] Create API endpoint `GET /assets/loans` in `src/vehicle_asset_lib/api/main.py`
- [X] T008 [US1] Create integration test for `GET /assets/loans` in `tests/test_api.py`
- [X] T009 [P] [US1] Define API client method for fetching loans in `frontend/src/api/client.ts`
- [X] T010 [P] [US1] Create `LoanList.vue` component in `frontend/src/components/LoanList.vue`
- [X] T011 [US1] Integrate `LoanList.vue` into the Inventory module in `frontend/src/views/Dashboard.vue`

**Independent Test Criteria**:
- API `GET /assets/loans` returns the correct list of active loans with required fields.
- `LoanList.vue` correctly renders the table with three columns: Identifier, Type, and User.

## Phase 4: [US2] Conditional Tab Visibility
Goal: The 'Loan' tab is only visible when there is at least one active loan.

- [X] T012 [P] [US2] Add logic to fetch loan count in `frontend/src/views/Dashboard.vue`
- [X] T013 [US2] Implement `v-if` directive on the 'Loan' tab in `frontend/src/views/Dashboard.vue`
- [X] T014 [US2] Verify tab disappears when all items are returned and appears when an item is borrowed

**Independent Test Criteria**:
- The 'Loan' tab is hidden when the API returns an empty list.
- The 'Loan' tab is visible when at least one loan record exists.

## Phase 5: [US3] Auto-Refresh & Data Accuracy
Goal: Data is refreshed whenever the tab is clicked to ensure accuracy.

- [X] T015 [US3] Add `@click` event handler to the 'Loan' tab to trigger data refresh in `frontend/src/views/Dashboard.vue`
- [X] T016 [US3] Verify that switching to the 'Loan' tab updates the list with any concurrent changes

**Independent Test Criteria**:
- Clicking the 'Loan' tab triggers a new API request to `GET /assets/loans`.

## Phase 6: [US4] CLI Support
Goal: Admin can view active loans via the CLI.

- [X] T017 [US4] Add `loans` command to the CLI in `src/vehicle_asset_lib/cli.py`

**Independent Test Criteria**:
- Running `vehicle-asset loans` (or equivalent) in the terminal displays the current active loans in a table or JSON format.

## Phase 7: Polish & Verification
- [X] T018 Final end-to-end verification of the "Loan" module across Web and CLI

## Dependencies
- US1 (Base implementation) must be completed before US2, US3, and US4.
- US2 and US3 can be worked on in parallel once US1 is functional.

## Parallel Execution Examples
- T005 (Service) and T010 (UI Component) can be developed simultaneously.
- T007 (API) and T017 (CLI) can be developed independently after the service layer is complete.
