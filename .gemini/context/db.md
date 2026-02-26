# Database Schema (SQLite)

## Models

### User
- `id`: `UUID` (Primary Key, default: `uuid4`)
- `name`: `String(255)`
- `id_last4`: `String(4)`
- `status`: `Enum(UserStatus)` (ACTIVE, INACTIVE)
- `created_at`: `DateTime` (UTC)
- **Relationships**: `transactions` (One-to-Many with `TransactionLog`)

### Asset
- `id`: `UUID` (Primary Key, default: `uuid4`)
- `type`: `Enum(AssetType)` (KEY, GAS_CARD)
- `identifier`: `String(255)`
- `status`: `Enum(AssetStatus)` (AVAILABLE, CHECKED_OUT)
- `current_holder_id`: `ForeignKey("users.id")` (Nullable)
- `maintenance_date`: `DateTime` (Nullable) - Last service date.
- `maintenance_mileage`: `Integer` (Nullable) - Last service mileage.
- `inspection_date`: `DateTime` (Nullable) - Annual inspection due.
- `insurance_date`: `DateTime` (Nullable) - Insurance renewal due.
- `created_at`: `DateTime` (UTC)
- **Relationships**: `transactions` (One-to-Many with `TransactionLog`)

### OTPPool
- `id`: `UUID` (Primary Key, default: `uuid4`)
- `password`: `String(255)` - 8-digit secure code.
- `is_used`: `Boolean` (Default: `False`)
- `used_at`: `DateTime` (Nullable)
- `created_at`: `DateTime` (UTC)
- **Relationships**: `transactions` (One-to-Many with `TransactionLog`)

### TransactionLog
- `id`: `UUID` (Primary Key, default: `uuid4`)
- `user_id`: `ForeignKey("users.id")`
- `asset_id`: `ForeignKey("assets.id")`
- `action`: `Enum(TransactionAction)` (PICKUP, RETURN)
- `otp_id`: `ForeignKey("otp_pool.id")`
- `timestamp`: `DateTime` (UTC)
- **Relationships**: `user`, `asset`, `otp`
