# Tasks: Persistent Password UI Refactor

## Implementation Strategy
We will follow an incremental delivery approach. First, we update the backend to provide the necessary expiration metadata. Then, we refactor the frontend to display the password embedded in the UI instead of popups. Finally, we implement the persistence and auto-hide logic to satisfy the 2-hour requirement.

## Phase 1: Setup
- [X] T001 Update frontend API types to include `expires_at` in `ReturnResponse` in `frontend/src/types/api.ts`

## Phase 2: Foundational
- [X] T002 [P] Update `AssetService.pickup` to return a 2-hour expiration timestamp in `src/vehicle_asset_lib/services/assets.py`
- [X] T003 [P] Update `AssetService.return_assets` to include a 2-hour expiration timestamp in `src/vehicle_asset_lib/services/assets.py`
- [X] T004 Update backend tests to verify `expires_at` fields in `tests/test_pickup.py` and `tests/test_return.py`

## Phase 3: User Story 1 - Pickup Flow
**Goal**: User sees the pickup password embedded in the dashboard after operation instead of a popup.
**Independent Test Criteria**: Pickup an asset; verify no dialog appears and "领取密码：xxxx" is shown in a green-bordered box below the title.

- [X] T004.1 [US1] Create Vitest tests for pickup password state update and display visibility in `frontend/src/views/__tests__/Dashboard.spec.ts`
- [X] T005 [US1] Define the embedded password display structure in `frontend/src/views/Dashboard.vue`
- [X] T006 [US1] Update `handlePickup` to update local state and suppress the OTP dialog in `frontend/src/views/Dashboard.vue`
- [X] T007 [US1] Apply green border styling and layout constraints to the password display in `frontend/src/views/Dashboard.vue`

## Phase 4: User Story 2 - Return Flow
**Goal**: User sees the return password embedded in the dashboard after operation instead of an alert.
**Independent Test Criteria**: Return an asset; verify no alert appears and "归还密码：xxxx" is shown in the green-bordered box.

- [X] T007.1 [US2] Create Vitest tests for return password label formatting and state override in `frontend/src/views/__tests__/Dashboard.spec.ts`
- [X] T008 [US2] Update `handleReturn` to update local state and suppress the return alert in `frontend/src/views/Dashboard.vue`
- [X] T009 [US2] Implement conditional formatting for pickup vs return labels in the display area in `frontend/src/views/Dashboard.vue`

## Phase 5: User Story 3 - Persistence & Expiry
**Goal**: Password remains after refresh and disappears automatically after 2 hours.
**Independent Test Criteria**: Perform an action, refresh the page, verify password remains. Mock time or wait to verify it disappears.

- [X] T009.1 [US3] Create Vitest tests for localStorage persistence and expiration timer logic in `frontend/src/views/__tests__/Dashboard.spec.ts`
- [X] T010 [US3] Implement `localStorage` saving/loading logic for the active password state in `frontend/src/views/Dashboard.vue`
- [X] T011 [US3] Implement a background timer using `setInterval` to check for expiration every minute in `frontend/src/views/Dashboard.vue`
- [X] T012 [US3] Implement auto-hide logic that clears state and layout when a password expires or is invalid in `frontend/src/views/Dashboard.vue`

## Phase 6: Polish
- [X] T013 Ensure active password state is cleared upon user logout in `frontend/src/views/Dashboard.vue`
- [X] T014 Final visual alignment check between the Title and "In Use" modules in `frontend/src/views/Dashboard.vue`

## Dependencies
US1 (Pickup) and US2 (Return) are the primary workflows. US3 (Persistence) depends on the state management established in US1/US2.

## Parallel Execution Examples
- T002 and T003 can be implemented simultaneously.
- T005 (UI structure) can be developed in parallel with backend updates T002/T003.
