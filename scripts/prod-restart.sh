#!/usr/bin/env bash
set -euo pipefail

COMPOSE_FILE="docker/docker-compose.prod.yml"

if [[ "${PROD_DRY_RUN:-}" == "1" ]]; then
  echo "DRY RUN: docker compose -f ${COMPOSE_FILE} restart"
  exit 0
fi

docker compose -f "${COMPOSE_FILE}" restart
