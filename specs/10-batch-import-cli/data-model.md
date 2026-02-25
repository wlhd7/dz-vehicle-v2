# Data Model: Batch Import CLI

The batch import feature relies on the existing `User` and `OTPPool` data models. No changes to the database schema are required.

## Key Entities (Existing)

### User
- `name`: String(255)
- `id_last4`: String(4)
- Validation: `id_last4` must be exactly 4 digits.

### OTPPool
- `password`: String(255)
- `is_used`: Boolean (Default: False)
- Validation: `password` must be exactly 8 digits for new batch imports.

## Validation Rules (Batch)

### Whitelist
- Data must be provided in pairs: `(Name, ID_Last4)`.
- If an odd number of tokens is provided in a file, the entire batch must fail (Atomic Processing).
- `ID_Last4` must be exactly 4 characters.

### OTP
- Every entry in the file must be exactly 8 digits.
- If any entry fails validation, the entire batch must fail (Atomic Processing).
