# Quickstart: Inventory Loan Module

## Development Setup

### 1. Backend
- The new logic is in `src/vehicle_asset_lib/services/assets.py`.
- Run tests: `pytest tests/test_loan_module.py` (to be created).
- Start API: `uvicorn src.vehicle_asset_lib.api.main:app --reload`.

### 2. Frontend
- Navigate to `frontend/`.
- Install dependencies: `npm install`.
- Run dev server: `npm run dev`.

## Verification Steps
1. **Empty State**: Ensure no assets are checked out. Open the app; the 'Loan' tab should **not** be visible in the Inventory module.
2. **Loan Item**: Borrow a vehicle or gas card.
3. **Check Visibility**: Navigate back to Inventory; the 'Loan' tab should now be visible.
4. **Verify Details**: Click 'Loan'. Verify:
   - 3 columns: Identifier, Type, User.
   - Your username is in the 'User' column.
   - The item you just borrowed is at the top.
5. **Return Item**: Return the asset.
6. **Verify Hidden**: The 'Loan' tab should disappear from Inventory.
