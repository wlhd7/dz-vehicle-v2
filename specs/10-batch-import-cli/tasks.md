# Tasks: Batch Import CLI Features

## Dependencies
- [US1] Batch Add Users depends on Foundational Parsing Logic
- [US2] Seed OTPs enhancement depends on Foundational Parsing Logic

## Parallel Execution Examples
- [US1] and [US2] tests can be developed in parallel in `tests/test_batch_import.py` once the structure is defined.
- [US1] and [US2] `AdminService` methods can be implemented in parallel in `src/vehicle_asset_lib/services/admin.py`.

## Implementation Strategy
- **Foundational**: Implement the common regex-based parsing and validation utility first.
- **US1 (P1)**: Implement `batch-add-users` with atomic validation and duplicate skipping.
- **US2 (P1)**: Enhance `seed-otps` with file support, 8-digit validation, and atomic processing.
- **Validation**: Strict TDD for each phase.

---

## Phase 1: Setup
Story Goal: Initialize environment for batch import features.

- [x] T001 Verify project structure and ensure `src/vehicle_asset_lib/services/admin.py` is accessible
- [x] T002 Create test file `tests/test_batch_import.py` for integration testing

---

## Phase 2: Foundational (Parsing & Validation)
Story Goal: Implement shared utilities for unified delimiter parsing and atomic validation.

- [x] T003 Implement `_parse_batch_file` utility in `src/vehicle_asset_lib/cli.py` using regex `re.split(r'[,\n]+', content)`
- [x] T004 Implement `_validate_whitelist_tokens` atomic check in `src/vehicle_asset_lib/cli.py` (even count, 4-char IDs)
- [x] T005 Implement `_validate_otp_tokens` atomic check in `src/vehicle_asset_lib/cli.py` (exactly 8 digits)

---

## Phase 3: User Story 1 - Batch Add Users [US1]
Story Goal: Allow administrators to bulk import whitelist users from a file.
Independent Test Criteria: `vehicle-asset admin batch-add-users` correctly imports valid pairs, skips duplicates, and fails atomically on malformed files.

- [x] T006 [P] [US1] Create TDD tests for `batch-add-users` in `tests/test_batch_import.py` (success, duplicate, atomic failure cases)
- [x] T007 [P] [US1] Implement `batch_add_users` in `src/vehicle_asset_lib/services/admin.py` with duplicate skipping logic
- [x] T008 [US1] Implement `batch-add-users` CLI command in `src/vehicle_asset_lib/cli.py` using foundational utilities
- [x] T009 [US1] Verify `batch-add-users` with sample `whitelist.txt` and check JSON output

---

## Phase 4: User Story 2 - Seed OTPs [US2]
Story Goal: Enhance OTP seeding to support batch files with 8-digit validation and atomic processing.
Independent Test Criteria: `vehicle-asset admin seed-otps --file` correctly imports 8-digit OTPs and fails atomically if any invalid format is found.

- [x] T010 [P] [US2] Create TDD tests for `seed-otps --file` in `tests/test_batch_import.py` (success, invalid format, duplicate cases)
- [x] T011 [P] [US2] Update seed_otps in src/vehicle_asset_lib/services/admin.py to implement skipping of existing unused OTPs and return added/skipped counts
- [x] T012 [US2] Enhance `seed-otps` CLI command in `src/vehicle_asset_lib/cli.py` to support `--file` argument and 8-digit validation
- [x] T013 [US2] Verify `seed-otps --file` with sample `otp.txt` and check total pool size in JSON output

---

## Phase 5: Polish & Validation
Story Goal: Ensure cross-cutting concerns like encoding and error messaging are consistent.

- [x] T014 Ensure UTF-8 encoding is explicitly handled for file reads in `src/vehicle_asset_lib/cli.py`
- [x] T015 Run full test suite `pytest` to ensure no regressions
- [x] T016 Final manual verification of all success criteria (including <5s performance targets for 1000+ records) defined in `spec.md`
