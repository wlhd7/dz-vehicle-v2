# Implementation Plan - Persistent Password UI Refactor

## Technical Context
- **Frontend Framework**: Vue 3 (Composition API) with TypeScript.
- **UI Component Library**: Element Plus.
- **State Management**: Local component state with `localStorage` for persistence across refreshes.
- **Timer Management**: `setInterval` in the frontend to monitor and clear expired passwords.
- **CSS**: Vanilla CSS for the green border and visibility logic.

## Constitution Check
- **Article I (Library-First)**: UI components will be modularized within `Dashboard.vue` or extracted if complexity grows.
- **Article II (CLI Interface)**: N/A for this UI-only change, but backend service tests will be updated.
- **Article III (Test-First)**: Vitest tests will be written for the frontend logic (persistence, expiration) before implementation.
- **Article VII (Simplicity)**: Uses existing frontend structure without adding new libraries.
- **Article VIII (Anti-Abstraction)**: Directly uses Vue's reactive state and `localStorage`.
- **Article IX (Integration-First)**: End-to-end tests (if available) or manual verification of the pickup/return flow.

## Phase 0: Outline & Research
- Decision: Use `localStorage` to store `{ code, type, expires_at }`.
- Decision: Implement a global or component-level timer to check expiration every 60 seconds.
- Decision: The display area will be a `div` with `border: 2px solid #67C23A` (Element Plus success green).

## Phase 1: Design & Contracts
- **Data Model**: `ActivePassword` entity in frontend state.
- **Contracts**: Update `PickupResponse` and `ReturnResponse` types in `frontend/src/types/api.ts` if needed (though they already seem to have `otp` and `expires_at`).

## Phase 2: Implementation Steps
1. **Frontend**: Create `PasswordDisplay.vue` component or add logic to `Dashboard.vue`.
2. **Frontend**: Update `handlePickup` and `handleReturn` in `Dashboard.vue` to save to `localStorage` instead of showing dialogs.
3. **Frontend**: Add lifecycle hook (`onMounted`) to resume state from `localStorage` and start the expiration timer.
4. **Frontend**: Implement `formatPasswordMessage` to handle "领取密码：xxxx" and "归还密码：xxxx".
5. **Testing**: Add Vitest cases for `localStorage` persistence and the 2-hour expiration logic.
