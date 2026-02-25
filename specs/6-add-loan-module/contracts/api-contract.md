# API Contract: Inventory Loan Module

## Endpoint: GET /assets/loans

### Description
Returns a list of all currently borrowed (active) assets, including the username of the borrower and the time it was checked out.

### Response
- **Status**: 200 OK
- **Body**: `List[LoanRecord]`

### LoanRecord Object
| Field | Type | Description |
|-------|------|-------------|
| identifier | String | Unique ID of the asset (e.g. Plate #, Card #) |
| type | String | Type of asset (e.g. KEY, GAS_CARD) |
| user | String | Username of the current holder |
| timestamp | String | ISO 8601 timestamp of when it was checked out |

### Error Responses
- **401**: Not logged in (if auth is enforced).
- **500**: Internal error.

### Empty State
Returns `[]` when no items are currently loaned. This should trigger the UI to hide the tab.
