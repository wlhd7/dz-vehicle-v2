# Data Model: UI Refactor & Borrowing/Returning Logic

## Entities

### Asset (Existing)
- **id**: UUID (Primary Key)
- **type**: Enum (KEY, GAS_CARD)
- **identifier**: String (e.g., Plate Number)
- **status**: Enum (AVAILABLE, CHECKED_OUT)
- **current_holder_id**: UUID (Foreign Key to User, nullable)

## State Transitions

### Asset Status
1. **AVAILABLE** -> **CHECKED_OUT**
   - **Trigger**: `pickup` action
   - **Pre-conditions**: 
     - Asset must be AVAILABLE.
     - User must not already hold an asset of the same type.
     - Total held assets by user must be < 2.
2. **CHECKED_OUT** -> **AVAILABLE**
   - **Trigger**: `return` action (batch)
   - **Pre-conditions**:
     - Asset must be CHECKED_OUT.
     - `current_holder_id` must match the requesting user.

## Validation Rules

### Borrowing (Pickup)
- **Rule 1**: Maximum 1 `KEY` (Vehicle) per user.
- **Rule 2**: Maximum 1 `GAS_CARD` per user.
- **Rule 3**: User cannot borrow if account is inactive (existing).

### Returning
- **Rule 1**: All currently held assets by the user must be included in the return list if the 'Return' button is clicked.
- **Rule 2**: Only the current holder can return an asset.
