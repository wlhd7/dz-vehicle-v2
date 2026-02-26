---

description: "Task list for Production Container Startup"
---

# Tasks: Production Container Startup

**Input**: Design documents from `specs/001-docker-prod-deploy/`
**Prerequisites**: `specs/001-docker-prod-deploy/plan.md`, `specs/001-docker-prod-deploy/spec.md`, `specs/001-docker-prod-deploy/research.md`, `specs/001-docker-prod-deploy/data-model.md`, `specs/001-docker-prod-deploy/contracts/`, `specs/001-docker-prod-deploy/quickstart.md`

**Tests**: Required by constitution (Article III, Article IX).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and shared configuration

- [x] T001 Create `.dockerignore` at repo root for production build context
- [x] T002 [P] Add runtime configuration template in `docker/env.production.example`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core container build assets required before any user story

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Create backend container build in `docker/backend/Dockerfile`
- [x] T004 [P] Create frontend container build in `docker/frontend/Dockerfile`
- [x] T005 Create baseline production stack in `docker/docker-compose.prod.yml`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Start production deployment (Priority: P1) 🎯 MVP

**Goal**: Provide a standardized production startup and restart flow.

**Independent Test**: Run the startup and restart scripts and confirm the service stack reaches a running state.

### Tests for User Story 1 (required) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T006 [P] [US1] Contract test for public root UI in `tests/contract/test_public_root_ui.py`
- [x] T007 [P] [US1] Integration test for startup/restart flow in `tests/integration/test_prod_startup.py`

### Implementation for User Story 1

- [x] T008 [P] [US1] Add production start script in `scripts/prod-start.sh`
- [x] T009 [P] [US1] Add production restart script in `scripts/prod-restart.sh`
- [x] T010 [US1] Add startup failure detection and user-facing message in `scripts/prod-start.sh`
- [x] T011 [US1] Document startup and restart steps in `docs/production.md`

**Checkpoint**: User Story 1 is functional and restartable via documented scripts

---

## Phase 4: User Story 2 - Access service via fixed endpoint (Priority: P2)

**Goal**: Ensure the web UI is reachable at `http://124.70.179.238:8081/`.

**Independent Test**: Load `http://124.70.179.238:8081/` and receive an HTML page response.

### Tests for User Story 2 (required) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T012 [P] [US2] Contract test for root UI response in `tests/contract/test_root_ui.py`
- [x] T013 [P] [US2] Integration test for public endpoint reachability in `tests/integration/test_public_endpoint.py`

### Implementation for User Story 2

- [x] T014 [US2] Publish the frontend service on port `8081` in `docker/docker-compose.prod.yml`
- [x] T015 [P] [US2] Add web server configuration in `docker/frontend/nginx.conf` to serve `/`
- [x] T016 [P] [US2] Add endpoint validation script in `scripts/validate-prod-endpoint.sh`

**Checkpoint**: User Story 2 is reachable via the public endpoint on `/`

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Documentation and consistency updates

- [x] T017 [P] Update production deployment notes in `README.md`
- [x] T018 [P] Align `specs/001-docker-prod-deploy/quickstart.md` with scripts and paths

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Final Phase)**: Depends on desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - no dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational - no dependencies on other stories

### Within Each User Story

- Core implementation before validation scripts and documentation updates
- Story complete before moving to the next priority if delivering MVP first

### Parallel Opportunities

- T002 and T004 can run in parallel with other setup/foundation work
- T006 and T007 can run in parallel (separate test files)
- T008 and T009 can run in parallel (separate scripts)
- T012 and T013 can run in parallel (separate test files)
- T015 and T016 can run in parallel (separate files)
- T017 and T018 can run in parallel (separate documentation files)

---

## Parallel Example: User Story 1

```bash
# Launch in parallel (separate files):
Task: "Contract test for public root UI in tests/contract/test_public_root_ui.py"
Task: "Integration test for startup/restart flow in tests/integration/test_prod_startup.py"
```

---

## Parallel Example: User Story 2

```bash
# Launch in parallel (separate files):
Task: "Contract test for root UI response in tests/contract/test_root_ui.py"
Task: "Integration test for public endpoint reachability in tests/integration/test_public_endpoint.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL)
3. Complete Phase 3: User Story 1
4. Validate startup and restart flow

### Incremental Delivery

1. Complete Setup + Foundational
2. Add User Story 1 → Validate
3. Add User Story 2 → Validate public endpoint

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Avoid vague tasks; keep file paths explicit
