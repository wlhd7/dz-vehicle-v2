# CLI Contract: Vehicle Asset Library

Following Article II, the library exposes functionality via a CLI.

## Commands

### 1. Verify Identity
`vehicle-asset verify --name "John Doe" --id-digits "1234"`
- **Output (JSON)**:
  ```json
  {
    "success": true,
    "user_id": "uuid-v4",
    "message": "Authenticated"
  }
  ```

### 2. List Available Assets
`vehicle-asset list --type all`
- **Output (JSON)**:
  ```json
  [
    {"id": "uuid-1", "type": "KEY", "identifier": "ABC-123", "status": "AVAILABLE"},
    {"id": "uuid-2", "type": "GAS_CARD", "identifier": "987654", "status": "AVAILABLE"}
  ]
  ```

### 3. Pickup Asset
`vehicle-asset pickup --user-id <uuid> --asset-ids <uuid1>,<uuid2>`
- **Output (JSON)**:
  ```json
  {
    "success": true,
    "otp": "998877",
    "assets": ["ABC-123", "987654"],
    "expires_at": "timestamp"
  }
  ```

### 4. Return Asset
`vehicle-asset return --user-id <uuid> --asset-id <uuid>`
- **Output (JSON)**:
  ```json
  {
    "success": true,
    "otp": "112233",
    "message": "Return code generated"
  }
  ```

### 5. Admin: Add OTPs
`vehicle-asset admin add-otps --file passwords.txt`
- **Output (JSON)**:
  ```json
  {
    "added": 50,
    "total_pool": 120
  }
  ```
