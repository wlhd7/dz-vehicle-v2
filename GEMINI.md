# Gemini Agent Context - dz-vehicle-v2

本文件定义了 `dz-vehicle-v2` 项目中 AI Agent 的核心准则、代码规范及上下文。

## 1. 核心准则 (Core Mandates)

### 1.1 语言与本地化 (Language & Localization)
- **Frontend Language**: UI must be **Simplified Chinese** only.
- **UI Strings**: All text in `frontend/src/i18n/locales/zh-cn.json`.
- **Response Language**: All interactions/explanations must be in **中文**.

### 1.2 开发模式 (Development Paradigm)
- **TDD (Test-Driven Development)**: Run `pytest` before and after any backend change.
- **Pydantic Driven**: Use Pydantic for API request/response validation.
- **Type Safety**: TypeScript strictly enforced in frontend; no `any`.

### 1.3 安全规范 (Security Standards)
- **Secrets**: Admin functions require `ADMIN_SECRET`. Never hardcode secrets.
- **Config**: Use `.env` for all environment-specific configurations.

## 2. 技术规格 (Technical Specifications)
Implementation details are offloaded to specialized context files:
- [API Contracts](.gemini/context/api.md)
- [Database Schema](.gemini/context/db.md)
- [Security & Auth](.gemini/context/auth.md)
- [Monitoring & Alerts](.gemini/context/monitoring.md)

## 3. UI & 交互逻辑 (UI & Interaction Logic)

### 3.1 借还流程 (Pickup & Return)
- **Selection**: 1 Vehicle + 1 Gas Card per checkout.
- **Feedback**: Selected rows use `lightgreen` background.
- **Bulk Return**: Single button to return all currently held assets.

### 3.2 密码与预警 (OTP & Alerts)
- **Embedded OTP**: Displayed in UI with a green border (`otp-display-embedded`).
- **Persistence**: Persists across refreshes; auto-expires after 2 hours.
- **Vehicle Alerts**: 
    - **Orange Highlight**: `warning-row` + ⚠️ icon.
    - **Maintenance**: > 6 months.
    - **Compliance**: < 30 days (Inspection/Insurance).

## 4. 常用命令 (Common Workflows)

### Backend (Python/FastAPI)
```bash
pytest
# Check alerts (JSON)
vehicle-asset notify-admins --dry-run --json
```

### Frontend (Vue 3/Vite)
```bash
cd frontend
npm run dev
npm run build # Type checking
```

---
*All modifications must align with roles defined in [AGENTS.md](./AGENTS.md).*

## Active Technologies
- Python 3.12, TypeScript/Vue 3 + FastAPI, SQLAlchemy, Element Plus (011-admin-otp-panel)
- PostgreSQL (SQLAlchemy) (011-admin-otp-panel)

## Recent Changes
- 011-admin-otp-panel: Added Python 3.12, TypeScript/Vue 3 + FastAPI, SQLAlchemy, Element Plus
