# API Contract: Asset Transactions (Updated)

## 1. Batch Return
**Endpoint**: `POST /return`
**Description**: Returns all assets currently held by the user.

### Request
```json
{
  "user_id": "uuid-string",
  "asset_ids": ["uuid-string-1", "uuid-string-2"]
}
```

### Response (Success)
- **Status**: 200 OK
```json
{
  "success": true,
  "otp": "123456",
  "message": "Return codes generated for 2 assets"
}
```

### Response (Error)
- **Status**: 400 Bad Request
```json
{
  "success": false,
  "message": "You are not the holder of one or more assets"
}
```

## 2. Pickup (Borrow)
**Endpoint**: `POST /pickup`
**Description**: Borrows selected assets, enforcing the "one of each type" limit.

### Request
```json
{
  "user_id": "uuid-string",
  "asset_ids": ["uuid-string-1", "uuid-string-2"]
}
```

### Response (Error - Limit Exceeded)
- **Status**: 400 Bad Request
```json
{
  "success": false,
  "message": "You cannot borrow more than one vehicle or gas card"
}
```
