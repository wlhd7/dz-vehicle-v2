# Security & Authentication

## Admin Access
- **Mechanism**: Protected by `ADMIN_SECRET` environment variable.
- **Verification**: FastAPI dependency `verify_admin_access` checks for a valid secret.
- **Header/Token**: Usually passed via custom headers or session-based admin context.

## User Identification
- **Method**: Whitelist validation using `Name` + `Last 4 digits of ID`.
- **Session**: Successful verification returns a `user_id` which must be used for subsequent `pickup`/`return` requests.

## OTP Security
- **Type**: 8-digit numeric codes.
- **Source**: Pre-seeded `OTPPool` to ensure predictable but secure locker access.
- **Persistence**: Displayed in frontend for 2 hours; tracked in `transaction_logs`.
