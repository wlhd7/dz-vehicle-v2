#!/usr/bin/env bash
set -euo pipefail

ENDPOINT="${PROD_ENDPOINT:-http://124.70.179.238:8081/}"

status=$(curl -s -o /tmp/prod_response.html -w "%{http_code}" "${ENDPOINT}")
content_type=$(curl -sI "${ENDPOINT}" | tr -d '\r' | awk -F': ' 'tolower($1)=="content-type"{print $2}')

if [[ "${status}" != "200" ]]; then
  echo "Endpoint validation failed: expected 200, got ${status}."
  exit 1
fi

if [[ "${content_type}" != *"text/html"* ]]; then
  echo "Endpoint validation failed: expected text/html, got ${content_type:-unknown}."
  exit 1
fi

echo "Endpoint validation succeeded: ${ENDPOINT}"
