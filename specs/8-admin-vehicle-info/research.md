# Research: Admin Vehicle Notifications

## Context
The "Admin Vehicle Information" feature requires sending weekly email notifications to administrators about vehicles with overdue maintenance or upcoming document expirations (inspection, insurance).

## Decisions

### 1. Email Delivery Mechanism
**Decision**: Use Python's built-in `smtplib` and `email.mime` modules.
**Rationale**: 
- Simplifies dependencies (no need to introduce `fastapi-mail` or similar external packages).
- For straightforward, text-based alert emails, the standard library is sufficient and robust.
- Configuration (`SMTP_SERVER`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`) will be driven by environment variables (`.env`).
**Alternatives Considered**:
- `fastapi-mail`: Overkill for a background CLI task that doesn't need to be tightly coupled to FastAPI request/response cycles.
- `yagmail`: Deprecated or less maintained compared to modern alternatives, still an external dependency.

### 2. Scheduling Approach
**Decision**: Implement the notification logic as a CLI command (`vehicle-asset notify-admins`) and recommend external OS-level scheduling (e.g., `cron`).
**Rationale**:
- **Aligns with Project Constitution (Article II)**: By exposing this functionality via the CLI, we adhere to the mandate that library logic must be accessible and verifiable through text-based interfaces.
- **Simplicity (Article VII)**: Avoids introducing complex in-process schedulers (like `APScheduler` or `Celery`) into the FastAPI application, keeping the architecture minimal.
- **Statelessness**: The FastAPI web server remains stateless and focused on responding to HTTP requests, while the periodic task is handled independently.
**Alternatives Considered**:
- `APScheduler` inside FastAPI startup events: Can be fragile during development (reloading) or multi-worker deployments (requires distributed locking or a designated worker).
- Celery + Redis/RabbitMQ: Grossly over-engineered for a simple weekly email task.
