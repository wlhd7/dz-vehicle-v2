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

## Project Structure Refresher
- `src/vehicle_asset_lib/`: Library core and Typer CLI.
- `src/vehicle_asset_lib/api/`: FastAPI web layer.
- `frontend/src/views/Dashboard.vue`: Main user interface.
- `specs/`: Historical and current feature specifications.

## Common Workflows

### Running Tests
```bash
pytest
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
The project has implemented a persistent password UI (embedded display with 2-hour expiry) and an active loan monitoring module. The system is fully localized in Chinese and follows strict TDD.
