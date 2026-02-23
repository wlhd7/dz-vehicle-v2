# Quickstart: Vehicle Asset Pickup

## Installation
1. Ensure Python 3.9+ is installed.
2. `pip install -e .` (from the library root, once created).

## Common Tasks

### For Users
1. **Login**: `vehicle-asset verify --name "Your Name" --id-digits "5678"`
2. **View Assets**: `vehicle-asset list`
3. **Pickup**: `vehicle-asset pickup --asset-id <ID>` (Saves OTP to screen)
4. **Return**: `vehicle-asset return --asset-id <ID>`

### For Admins
1. **Add Asset**: `vehicle-asset admin add-asset --plate "XYZ-789"`
2. **Seed OTPs**: `vehicle-asset admin seed-otps --count 100`

## Running Tests
Following Article III (TDD):
`pytest tests/`
