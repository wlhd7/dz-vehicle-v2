# Feature Specification: Security Access Control for CLI and API

## Description
为系统的管理操作添加安全访问控制。通过引入环境变量和请求头校验机制，确保只有获得授权的人员才能通过命令行工具（CLI）或接口（API）执行管理任务（如添加用户、管理资产等）。

## User Scenarios

### Scenario 1: Authorized Admin CLI Operation
**Actor**: System Administrator
1. Admin sets the correct `ADMIN_SECRET` environment variable in their terminal session.
2. Admin executes an administrative command (e.g., `vehicle-asset admin list-users`).
3. System validates the environment variable.
4. System executes the command and returns the requested data.

### Scenario 2: Unauthorized CLI Access Attempt
**Actor**: Unauthorized User
1. User attempts to execute an administrative command without setting `ADMIN_SECRET` or using an incorrect value.
2. System detects the missing or invalid secret.
3. System blocks the execution and displays an "Access Denied" error message.

### Scenario 3: Authorized API Management Request
**Actor**: Management Application/Admin
1. Admin (or authorized application) sends an HTTP request to an admin endpoint (e.g., `POST /admin/assets`).
2. The request includes a specific security header (e.g., `X-Admin-Secret`) with the correct value.
3. System validates the header value against the server-side configuration.
4. System processes the request and returns a successful response.

### Scenario 4: Unauthorized API Access Attempt
**Actor**: External Script/Unauthorized User
1. An unauthorized entity sends a request to an admin endpoint without the required header or with an incorrect value.
2. System identifies the security breach.
3. System rejects the request with a `403 Forbidden` status and an appropriate error message.

## Functional Requirements

### 1. CLI Access Control
- **1.1 Secret Validation**: All commands under the `admin` namespace must require a pre-configured secret to be present in the environment variables.
- **1.2 Explicit Rejection**: If the secret is missing or incorrect, the CLI must exit with a non-zero status code and show a clear security error.
- **1.3 Environment Variable Consistency**: The secret used for CLI must be configurable via the same environment variable used by the API for consistency.

### 2. API Access Control
- **2.1 Header-based Authentication**: All endpoints starting with `/admin` must require a custom security header for every request.
- **2.2 Middleware/Dependency Enforcement**: The security check must be implemented as a reusable component (middleware or dependency) to ensure consistent application across all current and future admin endpoints.
- **2.3 Secure Rejection**: Unauthorized requests must receive a standard `403 Forbidden` response to prevent accidental data leakage.

### 3. Configuration & Maintenance
- **3.1 Centralized Secret Management**: The system must support loading the secret from a `.env` file or system environment variables.
- **3.2 Default Secure State**: If no secret is configured, the system should default to a "deny-all" state for administrative operations rather than "allow-all".

## Success Criteria
1. **Zero-Bypass**: 100% of administrative CLI commands and API requests are blocked when the correct secret is not provided.
2. **Reliable Access**: 100% of requests/commands with the correct secret are processed without additional latency (overhead < 10ms).
3. **Consistent Error Reporting**: All failed attempts return a consistent "Access Denied" message (CLI) or 403 status (API).
4. **Configuration Flexibility**: Administrators can update the secret via environment variables without requiring code changes.

## Key Entities
- **Security Context**: The set of credentials (secret/token) required for access.
- **Admin Endpoint**: Any API route or CLI command restricted to administrative use.

## Assumptions
- **A1**: The server environment (where the API runs) and the admin terminal are considered secure enough to hold the secret in environment variables.
- **A2**: The secret will be a sufficiently long and complex string to prevent brute-force attacks.

## Constraints
- **C1**: The implementation must not interfere with non-administrative operations (e.g., user verification, asset listing for users).
- **C2**: Administrative credentials must not be hardcoded in the source code.
