# Data Model: Unattended Vehicle Asset Pickup

## Entities

### User (Whitelist)
Represents authorized personnel.
- `id`: UUID (Primary Key)
- `name`: String (Full Name)
- `id_last4`: String (4 digits, for verification)
- `status`: Enum (Active, Inactive)
- `created_at`: Timestamp

### Asset
Represents vehicle keys or gas cards.
- `id`: UUID (Primary Key)
- `type`: Enum (KEY, GAS_CARD)
- `identifier`: String (Plate Number or Card Number)
- `status`: Enum (AVAILABLE, CHECKED_OUT)
- `current_holder_id`: UUID (Foreign Key to User, Nullable)
- `created_at`: Timestamp

### OTPPool
The pool of temporary passwords provided by admins.
- `id`: UUID (Primary Key)
- `password`: String (The secret code)
- `is_used`: Boolean (Default: False)
- `used_at`: Timestamp (Nullable)
- `created_at`: Timestamp

### TransactionLog
Historical record of pickups and returns.
- `id`: UUID (Primary Key)
- `user_id`: UUID (Foreign Key to User)
- `asset_id`: UUID (Foreign Key to Asset)
- `action`: Enum (PICKUP, RETURN)
- `otp_id`: UUID (Foreign Key to OTPPool)
- `timestamp`: Timestamp

## Relationships
- A `User` can have multiple `TransactionLogs`.
- An `Asset` can have multiple `TransactionLogs`.
- A `TransactionLog` links one `User`, one `Asset`, and one `OTP`.

## State Transitions
- **Asset**: `AVAILABLE` --(PICKUP)--> `CHECKED_OUT` --(RETURN)--> `AVAILABLE`
- **OTP**: `is_used: False` --(DISPATCHED)--> `is_used: True`
