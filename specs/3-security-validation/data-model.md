# Data Model: Security Configuration

## Environment Variables
- `ADMIN_SECRET`: A string required for all administrative operations.
  - **Validation**: Must not be empty.
  - **Default**: No default (secure by default, will fail if missing).

## Constants
- `ADMIN_HEADER_NAME`: `X-Admin-Secret` (The header key used in API requests).
