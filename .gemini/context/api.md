# API Contracts

## Public Endpoints

### User Verification
- **POST `/verify`**
  - **Request**: `VerifyRequest { name: str, id_digits: str }`
  - **Logic**: Validates user against whitelist (`id_last4`).
  - **Response**: `{"success": bool, "user_id": str, "message": str}`

### Asset Management
- **GET `/assets`**
  - **Query**: `type` ("all", "key", "gas_card")
  - **Response**: List of `Asset` objects.
- **GET `/assets/loans`**
  - **Response**: `List[ActiveLoan]` (Active checkouts).
- **GET `/assets/loan-records`**
  - **Query**: `limit` (default 200)
  - **Response**: `List[LoanHistoryRecord]` (Pagination/History).

### Pickup & Return
- **POST `/pickup`**
  - **Request**: `PickupRequest { user_id: str, asset_ids: List[str] }`
  - **Response**: `{"success": bool, "otp": str, "message": str}`
- **POST `/return`**
  - **Request**: `ReturnRequest { user_id: str, asset_ids: Optional[List[str]], asset_id: Optional[str] }`
  - **Response**: `{"success": bool, "message": str}`

## Admin Endpoints (Protected)
Prefix: `/admin`, Header: `X-Admin-Secret` or custom dependency.

### Asset CRUD
- **POST `/admin/assets`**: Add new asset.
- **PATCH `/admin/assets/{asset_id}`**: Update asset (including maintenance/compliance).
- **DELETE `/admin/assets/{asset_id}`**: Remove asset.

### User CRUD
- **GET `/admin/users`**: List all whitelist users.
- **POST `/admin/users`**: Add new user.
- **PATCH `/admin/users/{user_id}`**: Update user details.
- **DELETE `/admin/users/{user_id}`**: Remove user.
