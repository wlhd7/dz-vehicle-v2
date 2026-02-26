# Quickstart: Production Container Startup

## Prerequisites

- Production server access to `124.70.179.238`.
- Runtime configuration values available for production.
- Public network access to port `8081`.

## Steps

1. Copy `docker/env.production.example` to `docker/env.production` and fill in values.
2. Start the service using `./scripts/prod-start.sh`.
3. Verify the web UI loads at `http://124.70.179.238:8081/`.
4. Restart the service using `./scripts/prod-restart.sh` and confirm the endpoint remains available.

## Expected Result

- The web UI is reachable at the root path `/` on `124.70.179.238:8081`.
- Startup failures provide a user-facing error message with the likely cause.
