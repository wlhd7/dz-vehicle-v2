# Production Deployment

## Prerequisites

- Docker and Docker Compose plugin installed on the server.
- Runtime configuration values prepared (see `docker/env.production.example`).
- Port `8081` available for public access.

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
