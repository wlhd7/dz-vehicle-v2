# CLI Contract: Batch Import CLI

## Command Group: admin

### batch-add-users
**Purpose**: Import multiple users from a file (CSV/Newline mixed).

**Usage**:
```bash
vehicle-asset admin batch-add-users <FILE_PATH>
```

**Success Response (JSON)**:
```json
{
  "added": 15,
  "skipped": 2,
  "total": 17
}
```

**Error Response (Stderr)**:
```text
Error: [Atomic Failure] Malformed file. Odd number of tokens (3) found for user pairs.
Error: [Atomic Failure] Invalid ID_Last4 format (5 chars) for user 'Alice'.
```

---

### seed-otps (Enhanced)
**Purpose**: Seed the OTP pool, supporting batch files.

**Usage**:
```bash
vehicle-asset admin seed-otps --file <FILE_PATH>
vehicle-asset admin seed-otps --count <NUMBER> (Legacy)
```

**Success Response (JSON)**:
```json
{
  "added": 100,
  "skipped": 5,
  "total_pool": 1095
}
```

**Error Response (Stderr)**:
```text
Error: [Atomic Failure] Invalid OTP format (9 digits) found: '123456789'.
```
