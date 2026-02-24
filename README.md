# Vehicle Asset Pickup Library

An unattended vehicle asset (keys, gas cards) pickup system.

## Project Structure
- `src/vehicle_asset_lib/`: Core logic and CLI.
- `src/vehicle_asset_lib/api/`: FastAPI REST endpoints.
- `frontend/`: Vue 3 + TypeScript + Element Plus dashboard.
- `tests/`: TDD test suite.

## Setup

### Backend
1. Create virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -e ".[test]"
   ```
3. Configure Security:
   Create a `.env` file in the root directory:
   ```bash
   ADMIN_SECRET=your_secure_random_string
   ```
   *Note: If .env is configured, you don't need to prefix commands with ADMIN_SECRET.*

4. Initialize Database:
   ```bash
   vehicle-asset admin init
   ```
5. Run API:
   ```bash
   uvicorn vehicle_asset_lib.api.main:app --reload
   ```

### Frontend
1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Run development server:
   ```bash
   npm run dev
   ```

## CLI Usage

### User Operations
```bash
# Verify user
vehicle-asset verify "John Doe" "1234"

# List assets
vehicle-asset list

# Pickup assets (keys/cards)
vehicle-asset pickup <user_id> "asset_id_1,asset_id_2"

# Return asset
vehicle-asset return <user_id> <asset_id>
```

### Administrative Operations
Administrative commands and endpoints are protected by `ADMIN_SECRET`.

#### Option 1: Using .env (Recommended)
If you have configured `ADMIN_SECRET` in your `.env` file, just run:
```bash
vehicle-asset admin list-users
```

#### Option 2: Command Prefix
If you haven't used a `.env` file, you must provide the secret manually:
```bash
ADMIN_SECRET=your_secret vehicle-asset admin list-users
```

#### API Access
Include the `X-Admin-Secret` header in your HTTP requests:
```bash
curl -H "X-Admin-Secret: your_secret" http://localhost:8000/admin/users
```

---

### Admin Commands Reference
```bash
# --- Whitelist Management ---
vehicle-asset admin add-user "Alice Smith" "5678"
vehicle-asset admin list-users
vehicle-asset admin update-user <user_id> --name "Alice Jones"
vehicle-asset admin delete-user <user_id>

# --- Asset Management ---
vehicle-asset admin add-asset KEY "PLATE-123"
vehicle-asset admin add-asset GAS_CARD "CARD-456"
vehicle-asset admin update-asset <asset_id> --identifier "PLATE-789"
vehicle-asset admin delete-asset <asset_id>

# --- OTP Pool Management ---
vehicle-asset admin seed-otps --count 50
```

## Architecture
- **Article I**: Library-First core.
- **Article II**: Typer-based CLI with JSON output.
- **Article III**: Strict TDD with `pytest`.
- **Article IX**: Realistic SQLite persistence.
