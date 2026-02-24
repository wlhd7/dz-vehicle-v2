# Quickstart: UI Refactor & Borrowing/Returning Logic

## Overview
This feature refactors the 'Using' and 'Inventory' modules to simplify selection and return processes.

## Development Steps

### 1. Backend: Update Asset Service
- Modify `src/vehicle_asset_lib/services/assets.py`:
  - Update `pickup` to enforce limits (max 1 KEY, 1 GAS_CARD).
  - Update `return_asset` (or add `return_assets`) to handle multiple IDs.
- Update `src/vehicle_asset_lib/api/main.py` to accept the new request body for `/return`.

### 2. Frontend: Refactor Dashboard
- Modify `frontend/src/views/Dashboard.vue`:
  - Remove individual 'Return' buttons in the table.
  - Add a single 'Return' button in the bottom-right of the 'Using' section.
  - Refactor 'Inventory' table to remove checkboxes and implement row-click selection with background highlighting.
  - Implement selection replacement logic (clicking a new vehicle replaces the previous vehicle).

### 3. Testing
- **Backend**: Update `tests/test_pickup.py` and `tests/test_return.py` to cover batch returns and borrowing limits.
- **Frontend**: Manual testing of the selection UI and the single return button.

## Verification Checklist
- [ ] User can select one vehicle and one gas card.
- [ ] Selecting a second vehicle replaces the first.
- [ ] 'Return' button only appears when items are held.
- [ ] Clicking 'Return' clears all held items and generates one OTP.
- [ ] Backend blocks borrowing a second vehicle if one is already held.
