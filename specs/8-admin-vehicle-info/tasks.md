# Tasks: Admin Vehicle Information Management

## Implementation Strategy
We will follow an incremental delivery approach, focusing on foundational backend changes first, followed by the management interface, and concluding with the automated notification system.

1.  **Foundational**: Update the database model and existing API endpoints to support vehicle information fields.
2.  **Management UI (US1 & US2)**: Implement the secure admin panel for viewing and updating vehicle data.
3.  **Alerting & Notifications (US3)**: Implement the visual alert logic and the weekly email notification CLI command.

## Phase 1: Setup & Foundational
Focus on database schema updates and core library service extensions.

- [x] T001 Update `Asset` model in `src/vehicle_asset_lib/models.py` with maintenance and compliance fields
- [x] T002 Update `AssetService` in `src/vehicle_asset_lib/services/assets.py` to include new fields in list and detail responses
- [x] T003 Update `AdminService` in `src/vehicle_asset_lib/services/admin.py` to allow updating maintenance and compliance fields
- [x] T004 Add unit tests for `Asset` model changes in `tests/test_models.py`
- [x] T005 Add unit tests for `AdminService` updates in `tests/test_admin.py`
- [x] T006 Update Pydantic models in `src/vehicle_asset_lib/api/main.py` to include new fields for requests and responses
- [x] T007 Update `admin_add_asset` and `admin_update_asset` endpoints in `src/vehicle_asset_lib/api/main.py`

## Phase 2: User Story 1 & 2 - Access & Update Vehicle Information
Implement the secure UI for administrators to manage vehicle data.

**Story Goal**: Administrators can securely access a vehicle info panel and update maintenance/compliance records.
**Independent Test Criteria**: 
- Admin link "车辆信息" is visible on the login page.
- Accessing the panel requires `ADMIN_SECRET`.
- Changes saved in the UI are persisted in the database.

- [x] T008 [P] [US1] Add `VehicleInfo` route to `frontend/src/router/index.ts`
- [x] T009 [US1] Create `VehicleInfo.vue` view in `frontend/src/views/VehicleInfo.vue` with authorized access check
- [x] T010 [US1] Update `frontend/src/views/Login.vue` to include the "车辆信息 | 管理面板" link structure
- [x] T011 [P] [US1] Add internationalization strings for vehicle info in `frontend/src/i18n/locales/zh-cn.json`
- [x] T012 [US2] Implement vehicle list table in `frontend/src/views/VehicleInfo.vue`
- [x] T013 [US2] Implement "Edit Vehicle Info" dialog in `frontend/src/views/VehicleInfo.vue`
- [x] T014 [US2] Connect edit dialog to backend `PATCH /admin/assets/{asset_id}` endpoint in `frontend/src/views/VehicleInfo.vue`

## Phase 3: User Story 3 - Monitoring & Notifications
Implement visual alerts and the weekly email notification system.

**Story Goal**: Automated alerts (UI and Email) for overdue maintenance or upcoming expirations.
**Independent Test Criteria**:
- Vehicles meeting alert criteria show orange background and ⚠️ icon in `VehicleInfo.vue`.
- `vehicle-asset notify-admins --dry-run` correctly identifies warning vehicles.
- `vehicle-asset notify-admins` successfully sends an email to the configured address.

- [x] T015 [US3] Implement alert calculation logic (6 months maintenance, 30 days compliance) in `src/vehicle_asset_lib/services/monitoring.py`
- [x] T016 [US3] Add unit tests for alert logic in `tests/test_monitoring.py`
- [x] T017 [US3] Apply visual styles (orange row + ⚠️ icon) in `frontend/src/views/VehicleInfo.vue` based on alert logic
- [x] T018 [US3] Implement `EmailService` using `smtplib` in `src/vehicle_asset_lib/services/notifications.py`
- [x] T019 [US3] Implement `notify-admins` command in `src/vehicle_asset_lib/cli.py`
- [x] T020 [US3] Add integration tests for CLI notification command in `tests/test_cli_notifications.py`

## Phase 4: Polish & Finalization
- [x] T021 [P] Ensure all date displays in UI are localized and formatted correctly
- [x] T022 Update `README.md` with instructions for configuring SMTP and scheduling the cron job
- [x] T023 Final end-to-end manual verification of the entire flow

## Dependencies
- US1 (Access) depends on Phase 1 (Foundational)
- US2 (Update) depends on US1
- US3 (Alerts) depends on US2 and SMTP configuration

## Parallel Execution Examples
- T008 (Router) and T011 (i18n) can be done in parallel with Backend T001-T003.
- T012 (List UI) and T018 (Email Service) can be developed independently.
