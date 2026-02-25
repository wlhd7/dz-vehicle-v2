# Gemini Agent Context - dz-vehicle-v2

This document provides essential context and instructions for Gemini CLI agents working on the `dz-vehicle-v2` project.

## Core Mandates
- **Language**: The frontend is exclusively in Simplified Chinese. Use `frontend/src/i18n/locales/zh-cn.json` for all UI strings.
- **TDD**: Adhere to strict Test-Driven Development. Run `pytest` before and after any backend changes.
- **Security**: Administrative functions require `ADMIN_SECRET`. Never hardcode secrets.
- **UI Logic**:
    - Pickup: Users can select one vehicle and one gas card.
    - Return: Bulk return for all items currently held by the user.
    - Password Display: Embedded UI with green border; persists across refreshes; auto-expires after 2 hours.
    - Selection feedback: Use light green backgrounds for selected rows in the inventory.
    - Vehicle Alerts: Use orange backgrounds (`warning-row`) and ⚠️ icons for vehicles with overdue maintenance (>6 months) or expiring compliance (<30 days).
    - Navigation: "车辆信息" (Vehicle Information) and "管理面板" (Admin Panel) links are on the login page, separated by `|`.

## Project Structure Refresher
- `src/vehicle_asset_lib/`: Library core and Typer CLI.
- `src/vehicle_asset_lib/api/`: FastAPI web layer.
- `src/vehicle_asset_lib/services/monitoring.py`: Monitoring logic for OTPs and vehicle alerts.
- `src/vehicle_asset_lib/services/notifications.py`: Email notification service (SMTP).
- `frontend/src/views/Dashboard.vue`: Main user interface.
- `frontend/src/views/VehicleInfo.vue`: Admin management for maintenance/compliance.
- `specs/`: Historical and current feature specifications.

## Common Workflows

### Running Tests
```bash
pytest
```

### Checking Vehicle Alerts (CLI)
```bash
vehicle-asset notify-admins --dry-run --json
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Adding a New UI String
1. Update `frontend/src/i18n/locales/zh-cn.json`.
2. Use `$t('key')` in Vue templates.

## Current State
The project has implemented a comprehensive vehicle maintenance and compliance tracking system, featuring:
- Persistent password UI and active loan monitoring.
- A secure "Vehicle Information" (车辆信息) panel for administrators.
- CLI support for adding and updating vehicle maintenance and compliance information.
- Automated weekly email notifications for maintenance and compliance warnings.
- Fully localized in Simplified Chinese and following strict TDD.
