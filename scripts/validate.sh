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

# For Coolify configs, we need to pass basic env vars or allow failure of variable expansion if not provided.
# But since we used :?required, 'config' command WILL fail if not set.
# So we must verify syntactically by passing dummy vars.

echo "   [Checking Prod/Staging Compose Syntax...]"
POSTGRES_PASSWORD=x MEDPLUM_REDIS_PASSWORD=x MEDPLUM_BASE_URL=x MEDPLUM_APP_BASE_URL=x MEDPLUM_STORAGE_BASE_URL=x MEDPLUM_JWT_ISSUER=x MEDPLUM_JWT_AUDIENCE=x GRAPH_STORE_URL=x GRAPH_STORE_TOKEN=x ANALYTICS_STORE_URL=x \
docker compose -f infra/coolify/medplum/docker-compose.yml config > /dev/null
echo "   [OK] Prod Medplum Compose"

POSTGRES_PASSWORD=x MEDPLUM_REDIS_PASSWORD=x MEDPLUM_BASE_URL=x MEDPLUM_APP_BASE_URL=x MEDPLUM_STORAGE_BASE_URL=x MEDPLUM_JWT_ISSUER=x MEDPLUM_JWT_AUDIENCE=x GRAPH_STORE_URL=x GRAPH_STORE_TOKEN=x ANALYTICS_STORE_URL=x \
docker compose -f infra/coolify/starvit/docker-compose.yml config > /dev/null
echo "   [OK] Prod Starvit Compose"

echo "   [Checking Staging Compose Syntax...]"
POSTGRES_PASSWORD=x MEDPLUM_REDIS_PASSWORD=x MEDPLUM_BASE_URL=x MEDPLUM_APP_BASE_URL=x MEDPLUM_STORAGE_BASE_URL=x MEDPLUM_JWT_ISSUER=x MEDPLUM_JWT_AUDIENCE=x GRAPH_STORE_URL=x GRAPH_STORE_TOKEN=x ANALYTICS_STORE_URL=x \
docker compose -f infra/coolify/medplum-staging/docker-compose.yml config > /dev/null
echo "   [OK] Staging Medplum Compose"

POSTGRES_PASSWORD=x MEDPLUM_REDIS_PASSWORD=x MEDPLUM_BASE_URL=x MEDPLUM_APP_BASE_URL=x MEDPLUM_STORAGE_BASE_URL=x MEDPLUM_JWT_ISSUER=x MEDPLUM_JWT_AUDIENCE=x GRAPH_STORE_URL=x GRAPH_STORE_TOKEN=x ANALYTICS_STORE_URL=x ANALYTICS_PASSWORD=x \
docker compose -f infra/coolify/starvit-staging/docker-compose.yml config > /dev/null
echo "   [OK] Staging Starvit Compose"

echo "   [Checking Dev Remote Backends Compose Syntax...]"
POSTGRES_PASSWORD=x MEDPLUM_REDIS_PASSWORD=x MEDPLUM_BASE_URL=x MEDPLUM_APP_BASE_URL=x MEDPLUM_STORAGE_BASE_URL=x ANALYTICS_PASSWORD=x \
docker compose -f infra/coolify/dev-backends/docker-compose.yml config > /dev/null
echo "   [OK] Dev Remote Backends Compose"

echo "=== All Checks Passed ==="
