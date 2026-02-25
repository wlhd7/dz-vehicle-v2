# Specification: Batch Import CLI Features

**Feature Name**: batch-import-cli
**Created**: 2026-02-25
**Status**: DRAFT

## 1. Overview
Extend the CLI tool to support batch adding of whitelist users and OTP passwords from text files. This improves efficiency when setting up the system with large amounts of pre-existing data.

## 2. Clarifications
### Session 2026-02-25
- Q: Malformed File Handling → A: Atomic (Validate entire file before processing).
- Q: OTP Format → A: Must be exactly 8 digits.
- Q: Whitelist Batch Command Name → A: `batch-add-users` under the admin group.

## 3. User Scenarios

### Scenario 1: Batch Import Whitelist Users
An administrator has a list of authorized users in a `.txt` file (formatted as name and ID pairs). They want to import all of them into the system in a single command.

### Scenario 2: Batch Import OTPs
An administrator has a list of pre-generated one-time passwords in a `.txt` file. They want to seed the OTP pool with these passwords efficiently.

## 4. Functional Requirements

### 4.1 Whitelist Batch Import (batch-add-users)
- **Command**: Add a new command `batch-add-users` to the `admin` command group.
- **File Format**: Supports unified delimiters. Both commas and newlines are treated as separators.
  - The parser will collect all non-empty tokens and process them sequentially as `Name, ID_Last4` pairs.
  - This supports both multi-line formats and single-line comma-separated lists.
- **Duplication Logic**: If a user with the same name and ID_Last4 already exists, the import for that specific user should be skipped.
- **Output**: The command should report the number of successfully added users and the number of skipped users.

### 4.2 OTP Batch Import (seed-otps)
- **Command**: Enhance the existing `seed-otps` command to support comma-separated files in addition to newline-separated files.
- **File Format**: Supports unified delimiters. Both commas and newlines are treated as separators.
- **Data Validation**: Each OTP must be exactly 8 digits.
- **Duplication Logic**: If an OTP password already exists in the pool (unused), it should skip adding it to prevent pool bloat.
- **Output**: The command should report the number of new OTPs added and the total pool size.

### 4.3 General Requirements
- File paths should be validated before processing.
- **Atomic Processing**: Validate the entire file for structural errors (e.g., odd number of items for whitelist, invalid OTP format) before adding any records to the database. If any error is found, abort the operation.
- **Encoding**: Support for encoding (UTF-8 by default).

## 5. Success Criteria
- Users can import 100+ whitelist entries from a single file in under 5 seconds.
- Users can import 1000+ OTP entries from a single file in under 5 seconds.
- The system correctly handles files with mixed delimiters (newlines and commas).
- Duplicate entries are correctly identified and skipped without crashing the process.

## 6. Key Entities
- **User**: (name, id_last4)
- **OTPPool**: (password)

## 7. Assumptions
- Files use UTF-8 encoding.
- `id_last4` is always 4 characters as per existing database constraints.
- Comma and newline are the primary delimiters; the system will treat any sequence of these as a unified separator.
