# Tasks: UI Refactor & Borrowing/Returning Logic

## Implementation Strategy
- **MVP Focus**: Focus on the backend logic for limits and batch returns first (Phase 2), followed by the Inventory Selection UI (US1) and finally the Batch Return UI (US2).
- **Incremental Delivery**: Each User Story phase results in a functional improvement that can be independently tested.

## Phase 1: Setup
- [X] T001 Verify project environment and dependency alignment in `.python-version` and `pyproject.toml`
- [X] T001.1 [P] Verify existence of 'Borrow' button and logic in `frontend/src/views/Dashboard.vue`; create if missing.

## Phase 2: Foundational (Backend Logic)
- [X] T002 [P] Create unit tests for batch return functionality and confirm failure in `tests/test_assets_service.py`
- [X] T003 [P] Create unit tests for borrowing limits (max 1 KEY, 1 GAS_CARD) and confirm failure in `tests/test_assets_service.py`
- [X] T004 Implement batch return logic in `AssetService.return_assets` within `src/vehicle_asset_lib/services/assets.py`
- [X] T005 Implement borrowing limit validation in `AssetService.pickup` within `src/vehicle_asset_lib/services/assets.py`
- [X] T006 Update the `/return` API endpoint in `src/vehicle_asset_lib/api/main.py` to handle batch asset IDs
- [X] T006.1 Update the CLI in `src/vehicle_asset_lib/cli.py` to support batch returns and borrowing limits.

## Phase 3: User Story 1 - Inventory Selection [US1]
**Goal**: User can select one vehicle and one gas card using row clicks with visual feedback.
**Test Criteria**: Clicking a vehicle row highlights it in light green; clicking another vehicle row transfers the highlight to the new row; clicking a selected row deselects it.

- [X] T007 [US1] Refactor inventory table in `frontend/src/views/Dashboard.vue` to strictly show two columns ('Vehicle', 'Gas Card') and remove checkboxes.
- [X] T008 [P] [US1] Implement `row-click` handler to manage single-selection state for `KEY` and `GAS_CARD` types in `frontend/src/views/Dashboard.vue`
- [X] T009 [US1] Add CSS for light green background and apply via `row-class-name` in the inventory table of `frontend/src/views/Dashboard.vue`

## Phase 4: User Story 2 - Batch Return [US2]
**Goal**: User can return all held assets simultaneously via a single button.
**Test Criteria**: Individual return buttons are gone; one 'Return' button is visible when items are held; clicking it returns all items and clears the 'Using' section.

- [X] T010 [US2] Remove the 'Action' column and individual return buttons from the 'Using' table in `frontend/src/views/Dashboard.vue`
- [X] T011 [US2] Add a single 'Return' button to the bottom-right corner of the 'Using' section in `frontend/src/views/Dashboard.vue`
- [X] T012 [US2] Update `handleReturn` to send all held asset IDs to the batch return endpoint in `frontend/src/views/Dashboard.vue`

## Phase 5: Polish & Verification
- [X] T013 Run backend test suite `pytest tests/` to verify logic integrity
- [X] T014 Perform manual end-to-end verification of the borrow and return flow in the browser

## Dependencies
- US1 (Phase 3) depends on Phase 2 (Backend logic for limits)
- US2 (Phase 4) depends on Phase 2 (Backend logic for batch returns)

## Parallel Execution Examples
- **Phase 2**: T002 and T003 can be executed in parallel (independent test cases).
- **Phase 3**: T008 can be started once the data structure for selection is defined.
