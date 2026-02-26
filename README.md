# dz-vehicle-v2: 无人值守车辆资产借还系统

一个高效、安全、完全本地化的无人值守车辆资产（钥匙、加油卡）借还系统。

## 🌟 核心特性 (Key Features)
- **无人值守流程 (Unattended Pickup)**: 极简的车辆与加油卡借还工作流。
- **批量导入工具 (Batch Import)**: 支持通过 CLI 批量导入白名单用户和 OTP 密码池。
- **持久化密码显示 (Persistent OTP Display)**: 嵌入式密码展示，支持 2 小时自动失效与页面刷新持久化。
- **透明化记录 (Transparent Logs)**: 实时监控活动借用，提供带 Excel 风格过滤的公共借还历史面板。
- **预警监控 (Proactive Monitoring)**: 自动追踪保养、年检和保险到期，UI 高亮提醒 + 每周邮件通知。
- **全中文 UI (Simplified Chinese UI)**: 基于 Vue 3 和 Element Plus 的现代中文仪表盘。

## 📁 项目结构 (Project Structure)
- `src/vehicle_asset_lib/`: Backend core logic and Typer CLI.
- `src/vehicle_asset_lib/api/`: FastAPI REST endpoints.
- `frontend/`: Vue 3 + TypeScript + Element Plus frontend.
- `tests/`: TDD test suites (Python/Pytest).
- `specs/`: Historical and current feature specifications.
- `.gemini/context/`: Modular technical documentation library.

## 🚀 Getting Started (快速开始)

### Backend Setup (后端配置)
1. **Create Virtual Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. **Install Dependencies**:
   ```bash
   pip install -e ".[test]"
   ```
3. **Environment Config**:
   Create `.env` with:
   ```bash
   ADMIN_SECRET=your_secure_secret
   ADMIN_NOTIFICATION_EMAIL=admin@example.com
   SMTP_SERVER=smtp.example.com
   SMTP_PORT=587
   SMTP_USER=your_username
   SMTP_PASSWORD=your_password
   SMTP_TLS=True
   ```
4. **Init Database**:
   ```bash
   vehicle-asset admin init
   ```
5. **Start API**:
   ```bash
   uvicorn vehicle_asset_lib.api.main:app --reload
   ```

### Frontend Setup (前端配置)
1. **Install Dependencies**:
   ```bash
   cd frontend
   npm install
   ```
2. **Start Dev Server**:
   ```bash
   npm run dev
   ```

## 🛠 Development Workflow (开发流程)
Strict adherence to TDD (Test-Driven Development):
1. **Write Test**: Under `tests/`.
2. **Run Test**: `pytest` (Expected failure).
3. **Implement**: Code logic in `src/`.
4. **Verify**: Run `pytest` (Ensure all pass).
5. **Quality**: `ruff check .`.

## 🌐 Production Deployment (Docker)
1. **Prod Config**:
   `cp docker/env.production.example docker/env.production`
2. **Launch Services**:
   `./scripts/prod-start.sh`
3. **Access**:
   `http://<server_ip>:8081/`

## 💻 CLI 操作指南 (CLI Operations Guide)

本系统内置了后端 CLI 工具 `vehicle-asset`，用于日常管理。**注意：`admin` 下的所有子命令均需要设置 `ADMIN_SECRET` 环境变量。**

### 1. 基础操作 (Basic)
- **查看资产列表**: `vehicle-asset list` (可选参数 `--type KEY` 或 `GAS_CARD`)
- **查看当前借出**: `vehicle-asset loans`
- **查看借还记录**: `vehicle-asset loan-records --limit 100`
- **生成预警报告**: `vehicle-asset notify-admins --dry-run`

### 2. 管理员资产/用户管理 (Admin - Assets & Users)
- **初始化数据库**: `vehicle-asset admin init`
- **列出所有用户**: `vehicle-asset admin list-users`
- **添加单个用户**: `vehicle-asset admin add-user "张三" "1234"`
- **批量导入用户**: `vehicle-asset admin batch-add-users <csv_file>`
- **添加/更新资产**: `vehicle-asset admin add-asset KEY "粤B12345" --maintenance-date 2024-01-01`

### 3. OTP 密码管理 (Admin - OTP)
- **导入密码池**: `vehicle-asset admin seed-otps --file-path <file_path>`
- **生成随机密码池**: `vehicle-asset admin seed-otps --count 100`

### 4. 生产环境快捷脚本 (Scripts)
- **一键启动/更新**: `./scripts/prod-start.sh`
- **查看后端日志**: `docker compose -f docker/docker-compose.prod.yml logs -f backend`

---
*Follow [GEMINI.md](./GEMINI.md) for AI Agent directives.*
