# Vehicle Asset Pickup Library

An unattended vehicle asset (keys, gas cards) pickup system with a localized Chinese dashboard.

## Features
- **Unattended Workflow**: Simplified pickup and return for vehicles and gas cards.
- **Batch Import CLI**: Bulk add authorized users and seed the OTP pool from text files with atomic validation.
- **Persistent Password Display**: Embedded OTP display with 2-hour auto-expiration and refresh persistence.
- **Loan Tracking & History**: Real-time monitoring of active loans and a public history panel with Excel-style filtering and pagination.
- **Vehicle Maintenance & Compliance**: Track maintenance dates, mileage, annual inspection, and insurance expirations.
- **Automated Alerts**: Visual row highlighting (orange background + ⚠️ icon) in the UI and weekly automated email notifications to administrators.
- **Localized UI**: Modern frontend built with Vue 3, Element Plus, and fully localized in Chinese.
- **Dual Interface**: Robust Typer-based CLI and FastAPI-powered REST API.
- **Secure Administration**: Protected administrative operations using `ADMIN_SECRET` and OTPs.
- **Reliable Persistence**: Production-ready SQLite integration with atomic transactions.

## Project Structure
- `src/vehicle_asset_lib/`: Core logic and CLI.
- `src/vehicle_asset_lib/api/`: FastAPI REST endpoints.
- `frontend/`: Vue 3 + TypeScript + Element Plus dashboard (Chinese).
- `tests/`: Comprehensive TDD test suite.

## Setup

### Backend
1. **Create virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. **Install dependencies**:
   ```bash
   pip install -e ".[test]"
   ```
3. **Configure Security**:
   Create a `.env` file in the root directory:
   ```bash
   ADMIN_SECRET=your_secure_random_string
   ADMIN_NOTIFICATION_EMAIL=admin@example.com
   SMTP_SERVER=smtp.example.com
   SMTP_PORT=587
   SMTP_USER=your_username
   SMTP_PASSWORD=your_password
   SMTP_TLS=True
   ```
   *Note: If .env is configured, you don't need to prefix commands with ADMIN_SECRET.*

4. **Initialize Database**:
   ```bash
   vehicle-asset admin init
   ```
5. **Run API**:
   ```bash
   uvicorn vehicle_asset_lib.api.main:app --reload
   ```

### Frontend
1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```
2. **Run development server**:
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

# List active loans
vehicle-asset loans

# List loan history (last 200 records)
vehicle-asset loan-records --limit 50

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
vehicle-asset admin batch-add-users users.txt  # Supports mixed comma/newline delimiters
vehicle-asset admin list-users
vehicle-asset admin update-user <user_id> --name "Alice Jones"
vehicle-asset admin delete-user <user_id>

# --- Asset Management ---
vehicle-asset admin add-asset KEY "PLATE-123" --maintenance-date 2026-01-01 --maintenance-mileage 5000
vehicle-asset admin add-asset GAS_CARD "CARD-456"
vehicle-asset admin update-asset <asset_id> --identifier "PLATE-789" --inspection-date 2026-12-31
vehicle-asset admin delete-asset <asset_id>

# --- OTP Pool Management ---
vehicle-asset admin seed-otps --count 50
vehicle-asset admin seed-otps --file-path otps.txt  # Atomic import of 8-digit OTPs

# --- Automated Notifications ---
# Scans for vehicle warnings and sends an email. Suitable for a weekly cron job.
vehicle-asset notify-admins
vehicle-asset notify-admins --dry-run
vehicle-asset notify-admins --json
```

## Architecture
- **Article I**: Library-First core.
- **Article II**: Typer-based CLI with JSON output.
- **Article III**: Strict TDD with `pytest`.
- **Article IX**: Realistic SQLite persistence.
