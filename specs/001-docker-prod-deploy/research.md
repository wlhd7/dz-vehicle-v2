# Research: Production Container Startup

## Decisions

### Runtime and framework alignment
- **Decision**: Use the existing Python FastAPI service and Vue frontend as-is, packaged for container deployment.
- **Rationale**: Aligns with current architecture and avoids introducing new runtime assumptions.
- **Alternatives considered**: Rewriting or splitting into separate runtimes for deployment only.

### Public endpoint behavior
- **Decision**: Expose the service publicly on `124.70.179.238:8081` with the web UI served at the root path `/`.
- **Rationale**: Matches the feature requirements and keeps validation straightforward.
- **Alternatives considered**: Internal-only access or non-root primary endpoint.

### Operational validation scope
- **Decision**: Validate both initial startup and restart behavior in production.
- **Rationale**: Confirms the service can be safely restarted without manual intervention.
- **Alternatives considered**: Validate only initial startup.

### Failure feedback expectations
- **Decision**: Provide a user-facing error message with a likely cause when startup fails.
- **Rationale**: Improves operator confidence and speeds troubleshooting.
- **Alternatives considered**: Log-only or remediation-heavy messaging.
