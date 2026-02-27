#!/usr/bin/env bash
set -euo pipefail

COMPOSE_FILE="docker/docker-compose.prod.yml"
ENV_FILE="docker/env.production"

if [[ "${PROD_DRY_RUN:-}" == "1" ]]; then
  echo "DRY RUN: docker compose -f ${COMPOSE_FILE} up -d --build"
  exit 0
fi

if [[ ! -f "${ENV_FILE}" ]]; then
  echo "Startup failed: ${ENV_FILE} not found. Copy docker/env.production.example to ${ENV_FILE} and set real values."
  exit 1
fi

# Export variables so they are available as build args in docker-compose
export $(grep -v '^#' "${ENV_FILE}" | xargs)

if ! docker compose -f "${COMPOSE_FILE}" up -d --build; then
  echo "Startup failed: verify Docker is running, required env values are set, and port 8081 is available."
  exit 1
fi
