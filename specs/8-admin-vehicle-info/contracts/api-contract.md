# API Contract: Admin Vehicle Information

## Endpoint Updates

### `GET /assets`
*Existing endpoint modified to return new fields for `KEY` asset types.*

**Response Item Shape (Modified)**:
```json
{
  "id": "uuid",
  "type": "KEY",
  "identifier": "京A·88888",
  "status": "AVAILABLE",
  "maintenance_date": "2026-01-15T00:00:00Z", // NEW (nullable)
  "maintenance_mileage": 15000,              // NEW (nullable)
  "inspection_date": "2026-10-01T00:00:00Z", // NEW (nullable)
  "insurance_date": "2026-11-01T00:00:00Z"   // NEW (nullable)
}
```

### `PATCH /admin/assets/{asset_id}`
*Existing endpoint modified to accept updates to the new tracking fields.*

**Request Body (Modified `UpdateAssetRequest`)**:
```json
{
  "identifier": "Optional[str]",
  "type": "Optional[str]",
  "maintenance_date": "Optional[str (ISO8601)]",  // NEW
  "maintenance_mileage": "Optional[int]",         // NEW
  "inspection_date": "Optional[str (ISO8601)]",   // NEW
  "insurance_date": "Optional[str (ISO8601)]"     // NEW
}
```

**Response (Modified)**:
```json
{
  "id": "uuid",
  "identifier": "string",
  "type": "KEY",
  "maintenance_date": "2026-01-15T00:00:00Z", // NEW
  "maintenance_mileage": 15000,              // NEW
  "inspection_date": "2026-10-01T00:00:00Z", // NEW
  "insurance_date": "2026-11-01T00:00:00Z"   // NEW
}
```
