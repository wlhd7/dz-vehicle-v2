# Implementation Plan: Admin OTP Management Panel

**Branch**: `011-admin-otp-panel` | **Date**: 2026-02-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/011-admin-otp-panel/spec.md`

## Summary
Implement a secure, administrator-only OTP management panel to monitor and replenish the OTP pool. This involves backend extensions for counting and seeding OTPs, and a new frontend sub-page accessible via a specific link in the dashboard header for a designated administrator name defined in `docker/env.production`.

## Technical Context

**Language/Version**: Python 3.12, TypeScript/Vue 3  
**Primary Dependencies**: FastAPI, SQLAlchemy, Element Plus  
**Storage**: PostgreSQL (SQLAlchemy)  
**Testing**: pytest (backend), vitest (frontend)  
**Target Platform**: Linux/Docker  
**Project Type**: Web application  
**Performance Goals**: Batch import of 500 OTPs < 3s  
**Constraints**: No rate limiting, restricted to specific Admin Name, no navigation links  
**Scale/Scope**: Administrative management of OTP pool.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Article I (Library-First)**: Reuse `AdminService` logic in the core library.
- **Article II (CLI Interface)**: Existing CLI `seed-otps` covers the core logic; no new CLI commands needed.
- **Article III (Test-First)**: Mandatory TDD for new API endpoints and frontend components.
- **Article VII (Simplicity)**: Implement within existing `AdminService` and `Dashboard.vue`/`Admin.vue` ecosystem.
- **Article VIII (Anti-Abstraction)**: Use FastAPI and Element Plus features directly.
- **Article IX (Integration-First)**: Test with real database for OTP seeding atomicity.

## Project Structure

### Documentation (this feature)

```text
specs/011-admin-otp-panel/
├── plan.md              # This file
├── research.md          # Research findings
├── data-model.md        # Data entities
├── quickstart.md        # Setup guide
├── contracts/
│   └── api-contract.md  # API definitions
└── checklists/
    └── requirements.md  # Quality checklist
```

### Source Code

```text
src/vehicle_asset_lib/
├── models.py            # Existing OTPPool
├── services/
│   └── admin.py         # Extend with get_otp_count and seed logic
└── api/
    └── main.py          # Add OTP management endpoints

frontend/
├── src/
│   ├── api/
│   │   └── client.ts    # Add OTP API calls
│   ├── views/
│   │   ├── Dashboard.vue # Add link to header
│   │   └── OTPManagement.vue # NEW: Manage OTPs
│   └── router/
│       └── index.ts     # Add new route
└── tests/
    └── test_admin_otp.py # Backend tests
```

**Structure Decision**: Web application (Option 2). Frontend and backend will be updated to support the new administrative functionality.

## Complexity Tracking

*No violations detected.*
