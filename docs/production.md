# Production Deployment

## Prerequisites

- Docker and Docker Compose plugin installed on the server.
- Runtime configuration values prepared (see `docker/env.production.example`).
- Port `8081` available for public access.

## Configuration

Make sure to set the designated administrator name for the OTP Management Panel in your environment file:
- `VITE_OTP_ADMIN_NAME`: The name of the user who is allowed to access the OTP Management Panel.

## Startup

1. Copy `docker/env.production.example` to `docker/env.production` and fill in real values.
2. Run the production startup script:

```bash
./scripts/prod-start.sh
```

## Restart

```bash
./scripts/prod-restart.sh
```

## Failure Feedback

If startup fails, the script prints a user-facing message with the likely cause. Check Docker status, missing env values, and port availability.
