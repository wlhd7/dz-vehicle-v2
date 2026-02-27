# Research: Admin OTP Management Panel

## Decision: Frontend Integration Point
**Decision**: The "OTP管理" link will be added to `frontend/src/views/Dashboard.vue` in the header section, to the left of the "Logout" button.
**Rationale**: This aligns with the requirement to place it in the dashboard panel near the logout button.
**Alternatives considered**: Adding it to the `Admin.vue` page, but the spec specifically asked for the dashboard panel.

## Decision: Specific Admin Identity
**Decision**: Access will be controlled by comparing the current `user_name` in `localStorage` with a configurable `VITE_OTP_ADMIN_NAME` defined in `docker/env.production`.
**Rationale**: The user requested using the administrator's name for easier configuration. This is more human-readable than a UUID.
**Alternatives considered**: Using UUID (previously proposed, now replaced).

## Decision: OTP Panel UI
**Decision**: The OTP Panel will be a new route and view (`OTPManagement.vue`) that is not linked in any sidebar or global navigation.
**Rationale**: Aligns with the "independent sub-page" and "no navigation links" requirements.
**Alternatives considered**: Modal dialog (rejected by user in clarification).

## Decision: Backend Service Extension
**Decision**: Extend `AdminService` with `get_otp_count()` and ensure `seed_otps()` returns the required metadata (added count + total pool).
**Rationale**: Reuses existing logic while providing the new data needed for the UI.
**Alternatives considered**: Creating a new `OTPService` (rejected for simplicity).

## Decision: File Upload Implementation
**Decision**: Use `multipart/form-data` for batch upload. The backend will parse the file in memory.
**Rationale**: Simplest approach for small to medium-sized text files.
**Alternatives considered**: Base64 encoding the file (less efficient).
