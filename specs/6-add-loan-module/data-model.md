# Data Model: Inventory Loan Module

## Entities

### Asset (Existing)
| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary Key |
| type | Enum | KEY, GAS_CARD |
| identifier | String | Unique ID |
| status | Enum | AVAILABLE, CHECKED_OUT |
| current_holder_id | UUID | FK to User (null if AVAILABLE) |

### User (Existing)
| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary Key |
| name | String | Username |

### TransactionLog (Existing)
| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary Key |
| user_id | UUID | FK to User |
| asset_id | UUID | FK to Asset |
| action | Enum | PICKUP, RETURN |
| timestamp | DateTime | When the action occurred |

## Logic: Active Loan Query
To generate the 'Loan' module list:
1. Filter `Asset` where `status == CHECKED_OUT`.
2. Join `User` on `Asset.current_holder_id == User.id`.
3. Join `TransactionLog` on `Asset.id == TransactionLog.asset_id`.
4. Filter `TransactionLog` for `action == PICKUP`.
5. Group/Select the *latest* `PICKUP` timestamp per asset.
6. Sort by that timestamp descending.
7. Return: `identifier` (Asset), `type` (Asset), `user_name` (User).
