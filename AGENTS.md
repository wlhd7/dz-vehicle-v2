# Sub-Agent Orchestration & Roles - dz-vehicle-v2

本文件定义了 `dz-vehicle-v2` 项目中 AI Agent 的角色分工、协作协议及工具使用偏好。

## 1. 角色定义 (Role Definitions)

### 1.1 Backend Architect (后端架构师)
- **Responsibility**: Logic in `src/vehicle_asset_lib/`, FastAPI endpoints, and Typer CLI.
- **Mandates**:
    - **Strict TDD**: Always run `pytest` before and after changes.
    - **Pydantic Validation**: All API schemas must use Pydantic.
    - **CLI First**: Core logic must be implemented in CLI first.
- **Languages**: Code (Python/English), Documentation (Chinese).

### 1.2 Frontend Specialist (前端专家)
- **Responsibility**: Vue 3, TypeScript, and Element Plus UI in `frontend/`.
- **Mandates**:
    - **Localization**: All UI strings go to `i18n/locales/zh-cn.json`.
    - **Type Safety**: No `any` allowed; use Interfaces/Types.
    - **UX Consistency**: Maintain `lightgreen` selection and orange warning rows.
- **Languages**: Code (TS/English), UI (Simplified Chinese).

### 1.3 Security Auditor (安全审计员)
- **Responsibility**: Review `ADMIN_SECRET` logic, OTP security, and Auth flows.
- **Mandates**:
    - **Secret Protection**: Never log or hardcode secrets.
    - **Atomic Transactions**: Ensure database updates are atomic.

### 1.4 Librarian (馆长/文档专员)
- **Responsibility**: Maintain `PRD.md`, `README.md`, `GEMINI.md`, and `.gemini/context/`.
- **Mandates**:
    - **Sync Consistency**: Ensure PRD matches implementation 100%.
    - **Modular Context**: Keep root docs clean by moving details to `.gemini/context/`.

## 2. 协作协议 (Collaboration Protocols)

### 2.1 任务流转 (Task Flow)
1. **Librarian**: Defines the specification in `specs/` or updates `PRD.md`.
2. **Backend Architect**: Implements logic and passes tests.
3. **Frontend Specialist**: Develops the UI and connects to APIs.
4. **Security Auditor**: Validates the implementation against security mandates.
5. **Librarian**: Updates technical context in `.gemini/context/`.

### 2.2 工具偏好 (Tooling Preferences)
- **Investigation**: Use `codebase_investigator` for complex refactors.
- **Execution**: Prefer `replace` over `write_file` for large files to preserve context.
- **Validation**: Always use `run_shell_command` to verify `pytest` and `npm run build`.

---
*Refer to [GEMINI.md](./GEMINI.md) for global project mandates.*
