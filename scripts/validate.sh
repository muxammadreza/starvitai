#!/bin/bash
set -e

echo "=== validating monorepo ==="

echo "1. Installing dependencies..."
pnpm -w install --frozen-lockfile

echo "2. Linting..."
pnpm lint

echo "3. Building..."
pnpm build

echo "4. Validating Docker Compose Configs..."
docker compose -f infra/dev/docker-compose.yml config > /dev/null
echo "   [OK] Dev Compose"

echo "   [Checking Prod/Staging Compose Syntax...]"
GCP_PROJECT_ID=x JWT_ISSUER=x JWT_AUDIENCE=x JWKS_URL=x TG_API_BASE=x TG_API_KEY=x \
docker compose -f infra/coolify/starvit/docker-compose.yml config > /dev/null
echo "   [OK] Prod Starvit Compose"

echo "   [Checking Staging Compose Syntax...]"
GCP_PROJECT_ID=x JWT_ISSUER=x JWT_AUDIENCE=x JWKS_URL=x TG_API_BASE=x TG_API_KEY=x ANALYTICS_STORE_URL=x \
docker compose -f infra/coolify/starvit-staging/docker-compose.yml config > /dev/null
echo "   [OK] Staging Starvit Compose"

echo "   [Checking Dev Backends Compose Syntax...]"
ANALYTICS_PASSWORD=x \
docker compose -f infra/coolify/dev-backends/docker-compose.yml config > /dev/null
echo "   [OK] Dev Backends Compose"

echo "=== All Checks Passed ==="
