# Implementation Plan: Admin Vehicle Information Management

## Technical Context
We are adding tracking and notification for vehicle maintenance and compliance dates.
- **Frontend**: Vue 3, Element Plus (existing dashboard/admin views). Needs to add new columns to the admin panel or a separate panel, and highlight rows.
- **Backend**: FastAPI, SQLAlchemy (SQLite via DB service). Needs new fields on the `Asset` model.
- **Dependencies**: 
  - [NEEDS CLARIFICATION] Email delivery mechanism (e.g. standard `smtplib` vs `fastapi-mail`).
  - [NEEDS CLARIFICATION] Scheduling approach for weekly emails (e.g. OS Cron invoking CLI vs in-process `APScheduler`).

## Constitution Check (Phase -1 Gates)

| Article | Rule | Status | Justification / Action |
| :--- | :--- | :--- | :--- |
| **I: Library-First** | Core logic in library | PASS | The notification and tracking logic will be added to `vehicle_asset_lib/services/admin.py`. |
| **II: CLI Mandate** | Expose via CLI | PASS | We will expose the notification trigger via the `typer` CLI. |
| **III: Test-First** | TDD mandatory | PASS | All new models and services will have Pytest tests written before implementation. |
| **VII: Minimal Structure** | Max 3 projects | PASS | We are extending the existing `vehicle_asset_lib` and `frontend`. |
| **VIII: Framework Trust** | Use frameworks directly | PASS | We will use SQLAlchemy for models and FastAPI for endpoints without custom wrappers. |
| **IX: Integration-First** | Real environments | PASS | We will test against the local SQLite database. |

## Execution Phases

### Phase 0: Outline & Research
1. Determine the email delivery mechanism.
2. Determine the scheduling approach.
(See `research.md`)

### Phase 1: Design & Contracts
1. Update Data Model (`data-model.md`).
2. Update Contracts (`contracts/`).
3. Update Quickstart (`quickstart.md`).

### Phase 2: Implementation (Deferred to Task generation)
- Update Models
- Implement CLI command
- Implement API Endpoints
- Implement Frontend UI
