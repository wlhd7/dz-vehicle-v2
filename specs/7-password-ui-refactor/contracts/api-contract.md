# API Contract Update - Persistent Password UI

## Backend Endpoints

### `POST /pickup`
Returns `expires_at` (now + 2 hours) instead of current time.

#### Response Body
```json
{
  "success": true,
  "otp": "1234",
  "assets": ["VEH-01", "GAS-01"],
  "expires_at": "2026-02-24T12:00:00Z"
}
```

### `POST /return`
Adds `expires_at` (now + 2 hours).

#### Response Body
```json
{
  "success": true,
  "otp": "5678",
  "message": "Return code generated for 2 assets",
  "expires_at": "2026-02-24T12:00:00Z"
}
```

## Frontend State

### `localStorage` key: `active_otp`
Used to persist across refreshes.

#### Value Format
```json
{
  "code": "1234",
  "type": "PICKUP",
  "createdAt": "2026-02-24T10:00:00Z",
  "expiresAt": "2026-02-24T12:00:00Z"
}
```
