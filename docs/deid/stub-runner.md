# De-ID stub runner (synthetic only)

Date: 2025-12-29
Owner: Data Platform
Status: Draft

## Purpose
Generate synthetic de-identified payloads for local development and tests. This tool does **not** connect to Medplum or BigQuery.

## Safety constraints
- `APP_ENV` must be `dev`, `test`, or `local`.
- `STARVIT_MODE` must be `stub`.
- Only synthetic fixtures are supported.

## Usage
From `services/api`:

```bash
APP_ENV=local STARVIT_MODE=stub \
python -m app.modules.deid.cli --count 3 --run-id run-synthetic
```

Write payload to a file:

```bash
APP_ENV=local STARVIT_MODE=stub \
python -m app.modules.deid.cli --count 5 --run-id run-synthetic --output /tmp/deid_stub.json
```

## Output
The command emits two JSON objects:
- `deid_observations`: rows aligned with `analytics.deid_observations` contract
- `deid_run_metadata`: run metadata aligned with `analytics.deid_run_metadata` contract

## Limitations
- No PHI handling; synthetic only.
- No persistence to BigQuery.
- Version strings are stub placeholders.
