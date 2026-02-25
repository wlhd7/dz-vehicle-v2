# Data Model - Persistent Password UI

## Frontend Entities

### `ActivePassword`
State used in the dashboard to represent the currently active OTP.

| Field | Type | Description |
|-------|------|-------------|
| `code` | string | The 4-6 digit OTP string. |
| `type` | 'PICKUP' \| 'RETURN' | The type of operation that generated this OTP. |
| `createdAt` | string (ISO) | The timestamp when the OTP was generated. |
| `expiresAt` | string (ISO) | The timestamp when the OTP expires (CreatedAt + 2 hours). |

### `OTPStore` (LocalStorage)
Key: `active_otp`

Value:
```json
{
  "code": "1234",
  "type": "PICKUP",
  "createdAt": "2026-02-24T10:00:00Z",
  "expiresAt": "2026-02-24T12:00:00Z"
}
```

## Backend Changes

### `PickupResponse`
- Fix the `expires_at` to actually be 2 hours from `now`.

### `ReturnResponse`
- Add `expires_at` field (2 hours from `now`).
