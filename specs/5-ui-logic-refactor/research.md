# Research: UI Refactor & Borrowing/Returning Logic

## Technical Unknowns & Decisions

### 1. Asset Type Mapping
- **Finding**: Currently, `AssetType` enum has `KEY` and `GAS_CARD`. The spec refers to "Vehicle" (车辆).
- **Decision**: Map "Vehicle" to `KEY` in the UI and backend, as vehicle access is typically managed via keys in this system. If a semantic change to `VEHICLE` is required, it would involve a database migration. For this UI refactor, we will continue using `KEY` but label it as "Vehicle" in the Chinese UI.
- **Rationale**: Maintain consistency with existing data model while satisfying user-facing terminology.

### 2. Simultaneous Return Implementation
- **Finding**: Current `AssetService.return_asset` only accepts a single `asset_id`.
- **Decision**: Implement a new method `return_assets(user_id, asset_ids)` in `AssetService` (or a batch equivalent) to handle multiple assets in a single transaction. This ensures data integrity and uses only one OTP from the pool for the entire return operation.
- **Rationale**: Aligns with the requirement that all items must be returned together and simplifies the OTP usage.

### 3. Inventory Single Selection Logic
- **Finding**: The current frontend uses `el-table` with a selection column which allows multiple selections.
- **Decision**: Replace the selection column with a custom row-click handler that manages state. We will maintain two separate selected IDs (one for `KEY`, one for `GAS_CARD`). Clicking a new item of the same type will overwrite the previous selection.
- **Rationale**: Directly implements the "replace selection" requirement and provides better control over the business rule.

### 4. Backend Borrowing Limits
- **Finding**: The backend `pickup` method currently accepts a list of IDs but doesn't enforce the "one of each type" limit.
- **Decision**: Add validation logic in `AssetService.pickup` to check the types of assets being requested and the user's current holdings.
- **Rationale**: Ensures the business rule is enforced even if frontend validation is bypassed.

## Best Practices
- **UI Feedback**: Use Element Plus `row-class-name` or scoped slots to apply the light green background for selected items.
- **API Design**: Use a single POST request for returns to ensure atomicity.

## Consolidation
- **Decision**: We will update the `AssetService` to support batch returns and enforce borrowing limits.
- **Rationale**: Critical for data integrity and business rule enforcement.
- **Alternatives**: We could have called the single return API multiple times, but this would use multiple OTPs and risk partial failures.
