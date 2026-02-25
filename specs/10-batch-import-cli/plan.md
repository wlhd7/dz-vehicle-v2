# Implementation Plan: Batch Import CLI Features

**Feature Name**: batch-import-cli
**Branch**: 10-batch-import-cli
**Status**: DRAFT

## Technical Context

- **Tech Stack**: Python, Typer (CLI), SQLAlchemy (ORM).
- **Existing Components**: 
    - `src/vehicle_asset_lib/cli.py`: CLI entry points.
    - `src/vehicle_asset_lib/services/admin.py`: Administrative business logic.
    - `src/vehicle_asset_lib/models.py`: Database models for `User` and `OTPPool`.
- **Infrastructure**: SQLite database managed via SQLAlchemy.

## Constitution Check

- [x] **Article I (Library-First)**: Implement batch logic in `AdminService` within the library.
- [x] **Article II (CLI Mandate)**: Commands will support JSON output and accept file paths.
- [x] **Article III (Test-First)**: TDD is mandatory; tests for batch operations must be written before implementation.
- [x] **Article VII (Minimal Structure)**: No new architectural layers or projects required.
- [x] **Article VIII (Framework Trust)**: Leverage Typer's argument parsing and SQLAlchemy's session management.
- [x] **Article IX (Integration-First)**: Tests will run against the real SQLite database to ensure integrity.

## Phase 0: Outline & Research

### Research Tasks
- [x] **R0.1**: Verify current `seed_otps` implementation in `AdminService` and `cli.py`. (Done: Identified in research phase).
- [x] **R0.2**: Confirm `User` model constraints for `id_last4` (Done: 4-character string).
- [x] **R0.3**: Plan unified delimiter parsing logic (RegEx vs simple split/strip).

### Findings (research.md)
- **Decision**: Use a regex-based parser `re.split(r'[,\n]+', content)` to handle mixed commas and newlines effectively while filtering out empty strings.
- **Decision**: Implementation of "Atomic Processing" will involve a dry-run validation pass over the entire token list before starting database transactions.
- **Decision**: `seed-otps` will be updated to accept a file or a raw string/count, maintaining backward compatibility while adding flexibility.

## Phase 1: Design & Contracts

### Data Model (data-model.md)
- No changes to existing database schema.
- Validation logic for `User` (name, 4-digit ID) and `OTPPool` (8-digit password).

### Interface Contracts (contracts/)
- **CLI Contract**:
    - `vehicle-asset admin batch-add-users <file_path>`
    - `vehicle-asset admin seed-otps --file <file_path>` (Extending existing command)

### Agent Context
- Run update script to ensure environment is synced.

## Phase 2: Implementation & Validation Plan

### Step 1: Tests (TDD)
- Create `tests/test_batch_import.py`.
- Test cases:
    - Successful whitelist batch import (multi-line).
    - Successful whitelist batch import (single-line comma separated).
    - Atomic failure for whitelist (odd number of tokens).
    - Successful OTP batch import (mixed delimiters).
    - Atomic failure for OTP (invalid 8-digit format).
    - Duplicate skipping for both users and OTPs.

### Step 2: Library Implementation
- Update `AdminService` in `src/vehicle_asset_lib/services/admin.py`:
    - Add `batch_add_users(pairs: List[Tuple[str, str]])`.
    - Update `seed_otps(passwords: List[str])` to skip passwords that already exist in the pool as unused.

### Step 3: CLI Implementation
- Update `src/vehicle_asset_lib/cli.py`:
    - Add `batch_add_users` command.
    - Refactor `seed_otps` to support the new file format and validation.
    - Implement the common parsing logic.

### Step 4: Verification
- Run `pytest`.
- Manual verification with sample `whitelist.txt` and `otp.txt`.
