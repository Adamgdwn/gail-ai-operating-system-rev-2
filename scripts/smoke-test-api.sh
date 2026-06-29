#!/usr/bin/env bash
# Smoke-test the GAIL OS API. Requires the server to already be running.
# Usage: GAIL_OS_API_KEY=<key> BASE_URL=http://localhost:8123 ./scripts/smoke-test-api.sh

set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8123}"
API_KEY="${GAIL_OS_API_KEY:-}"

echo "Smoke-testing GAIL OS API at $BASE_URL"

# Health check (no auth)
status=$(curl -sf "$BASE_URL/api/v1/health" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['status'])")
if [ "$status" != "ok" ]; then
  echo "FAIL: health check returned status=$status"
  exit 1
fi
echo "PASS: /api/v1/health -> status=ok"

# Authenticated endpoint — connectors list
if [ -n "$API_KEY" ]; then
  http_code=$(curl -sf -o /dev/null -w "%{http_code}" \
    -H "X-Api-Key: $API_KEY" \
    "$BASE_URL/api/v1/connectors")
  if [ "$http_code" != "200" ]; then
    echo "FAIL: GET /api/v1/connectors returned HTTP $http_code"
    exit 1
  fi
  echo "PASS: GET /api/v1/connectors -> HTTP 200"
else
  echo "SKIP: GAIL_OS_API_KEY not set — skipping authenticated smoke tests"
fi

echo "Smoke tests passed."
