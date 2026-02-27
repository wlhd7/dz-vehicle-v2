# Tasks: Admin OTP Management Panel

**Input**: Design documents from `/specs/011-admin-otp-panel/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/api-contract.md

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and environment configuration

- [x] T001 Configure `VITE_OTP_ADMIN_NAME` in `docker/env.production`
- [x] T002 [P] Register route for `/otp-management` in `frontend/src/router/index.ts`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure required for all OTP management features

- [x] T003 [P] Implement `get_otp_count` method in `src/vehicle_asset_lib/services/admin.py`
- [x] T004 [P] Create initial `frontend/src/views/OTPManagement.vue` component with basic layout
- [x] T005 [P] Add `getOTPCount` API call definition to `frontend/src/api/client.ts`

**Checkpoint**: Foundation ready - User Story 1 can now be implemented

---

## Phase 3: User Story 1 - OTP Pool Oversight (Priority: P1) 🎯 MVP

**Goal**: Display current unused OTP count to the designated administrator

**Independent Test**: Log in as the admin defined in `VITE_OTP_ADMIN_NAME`, verify "OTP管理" link appears in Dashboard header, click it, and see the correct remaining count.

### Tests for User Story 1

- [x] T006 [US1] Create TDD tests for `GET /admin/otp/count` in `tests/test_admin_otp.py`
- [x] T007 [US1] Ensure tests in `tests/test_admin_otp.py` fail before implementation

### Implementation for User Story 1

- [x] T008 [US1] Implement `GET /admin/otp/count` endpoint in `src/vehicle_asset_lib/api/main.py` (requires `X-Admin-Secret`)
- [x] T009 [US1] Add "OTP管理" link to `frontend/src/views/Dashboard.vue` header next to logout button
- [x] T010 [US1] Implement remaining OTP count display in `frontend/src/views/OTPManagement.vue` using `getOTPCount`

**Checkpoint**: User Story 1 is functional and testable independently

---

## Phase 4: User Story 2 - Manual OTP Injection (Priority: P2)

**Goal**: Allow admin to manually add a single 8-digit OTP code

**Independent Test**: Enter an 8-digit code in the manual input field, click "添加", and verify the remaining count increments by 1.

### Tests for User Story 2

- [x] T011 [US2] Create TDD tests for `POST /admin/otp/single` in `tests/test_admin_otp.py`
- [x] T012 [US2] Ensure tests in `tests/test_admin_otp.py` fail before implementation

### Implementation for User Story 2

- [x] T013 [US2] Implement single OTP addition logic in `src/vehicle_asset_lib/services/admin.py`
- [x] T014 [US2] Implement `POST /admin/otp/single` endpoint in `src/vehicle_asset_lib/api/main.py`
- [x] T015 [P] [US2] Add `addSingleOTP` API call definition to `frontend/src/api/client.ts`
- [x] T016 [US2] Implement manual OTP input form and submission in `frontend/src/views/OTPManagement.vue`

**Checkpoint**: User Story 2 is functional and testable independently

---

## Phase 5: User Story 3 - Batch OTP Import (Priority: P1)

**Goal**: Allow admin to upload a file for atomic batch OTP import with feedback

**Independent Test**: Upload a valid text file with 10 OTPs, see "成功导入 10 个，总数 X"；upload a file with an invalid 7-digit code, see "文件中包含无效的 OTP 格式" and no codes added.

### Tests for User Story 3

- [x] T017 [US3] Create TDD tests for `POST /admin/otp/batch` in `tests/test_admin_otp.py` (success and atomic failure cases)
- [x] T018 [US3] Ensure tests in `tests/test_admin_otp.py` fail before implementation

### Implementation for User Story 3

- [x] T019 [US3] Enhance `seed_otps` or add batch helper in `src/vehicle_asset_lib/services/admin.py` to return added count and total pool
- [x] T020 [US3] Implement `POST /admin/otp/batch` (multipart/form-data) in `src/vehicle_asset_lib/api/main.py`
- [x] T021 [P] [US3] Add `uploadOTPBatch` API call definition to `frontend/src/api/client.ts`
- [x] T022 [US3] Implement file upload component and feedback message logic in `frontend/src/views/OTPManagement.vue`

**Checkpoint**: All user stories are independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Security, redirection, and UI/UX finalization

- [x] T023 [P] Implement unauthorized access redirection to dashboard for non-designated users in `frontend/src/router/index.ts`
- [x] T024 Final CSS polish and responsiveness for `frontend/src/views/OTPManagement.vue` using Element Plus
- [x] T025 Run all tests in `tests/test_admin_otp.py` and verify all success/error scenarios
- [x] T026 [P] Update `docs/production.md` with instructions for setting `VITE_OTP_ADMIN_NAME`
- [x] T027 Verify batch import performance (SC-002) for 500 OTPs completes in under 3 seconds

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately
- **Foundational (Phase 2)**: Depends on Phase 1
- **User Stories (Phase 3-5)**: All depend on Phase 2 completion
  - US1 (P1) and US3 (P1) are high priority
  - US2 (P2) is lower priority
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1**: Foundation for the OTP Panel view.
- **User Story 2 & 3**: Can be developed in parallel once the view is established in US1.

### Parallel Opportunities

- T002-T005 (Foundational setup)
- T015 (API client) and backend logic for US2
- T021 (API client) and backend logic for US3
- T023 and T026 (Polish/Docs)

---

## Parallel Example: User Story 3

```bash
# Backend logic and API client definition can happen at the same time:
Task: "Implement POST /admin/otp/batch (multipart/form-data) in src/vehicle_asset_lib/api/main.py"
Task: "Add uploadOTPBatch API call definition to frontend/src/api/client.ts"
```

---

## Implementation Strategy

### MVP First (User Story 1 & 3)

1. Complete Setup and Foundational phases.
2. Complete User Story 1 (remaining count display).
3. Complete User Story 3 (batch upload - most efficient way to seed).
4. Verify core management capability.

### Incremental Delivery

1. Foundation → Routes and service methods ready.
2. US1 → Admin can see current status.
3. US3 → Admin can seed the pool via files.
4. US2 → Admin can perform surgical manual additions.
5. Polish → Ensure security and UI consistency.
