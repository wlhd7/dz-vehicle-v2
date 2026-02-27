# Data Model: Admin OTP Management Panel

## OTPPool
Represents the pool of pre-generated passwords.

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary key |
| password | String(8) | The 8-digit OTP string. Unique among unused. |
| is_used | Boolean | Whether the password has been assigned to a transaction. |
| used_at | DateTime | When the password was used (if applicable). |
| created_at | DateTime | When the password was added to the pool. |

## User
Represents the designated administrator.

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary key (used for identification). |
| name | String | User's full name. |
| id_last4 | String | Last 4 digits of ID card (used for verification). |

## State Transitions
- **Added**: `is_used = False`
- **Assigned/Used**: `is_used = True` (set during pickup/return)
