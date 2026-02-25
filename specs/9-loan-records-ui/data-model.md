# Data Model: Loan Records Panel

The "Loan Records" feature does not introduce new database tables but relies on querying existing `TransactionLog`, `Asset`, and `User` entities.

## Entities

### LoanRecord (Virtual/UI Entity)
This entity represents a single loan lifecycle from pickup to return.

| Field | Type | Description |
| :--- | :--- | :--- |
| `identifier` | String | License plate or gas card ID |
| `type` | AssetType | `KEY` (车辆) or `GAS_CARD` (加油卡) |
| `user_name` | String | Name of the borrower |
| `loan_time` | DateTime | Timestamp of the `PICKUP` action |
| `return_time` | DateTime? | Timestamp of the subsequent `RETURN` action (null if active) |

## Logic: Loan Record Mapping
1.  Identify all `TransactionLog` entries where `action == PICKUP`.
2.  For each pickup:
    - Join `Asset` to get `identifier` and `type`.
    - Join `User` to get `user_name`.
    - Subquery `TransactionLog` for the same `asset_id` where `action == RETURN` and `timestamp > pickup.timestamp`.
    - Select the minimum (earliest) such timestamp as `return_time`.
3.  Sort by `loan_time` descending.
4.  Limit to 200.
