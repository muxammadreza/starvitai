# Secret Management in Starvit

Starvit uses **Google Cloud Secret Manager** as the source of truth for secrets in staging and production environments.

## Overview

- **Local Development**: Continue to use `.env` files.
- **Production/Staging**: Secrets are fetched from GCP Secret Manager at runtime.

## Backend Integration

The FastAPI backend uses `pydantic-settings` to load configuration. We have injected a custom source `SecretManagerSettingsSource` (`app/core/secrets_loader.py`) that:
1.  Checks if `USE_SECRET_MANAGER=true` and `GCP_PROJECT_ID` is set.
2.  If yes, iterates over requested definition fields (like `TG_API_KEY`).
3.  Fetches the latest version of the secret with the same name from GCP.

### How to Add a New Secret

1.  **Define it in `config.py`**:
    ```python
    class Settings(BaseSettings):
        MY_NEW_SECRET: Optional[str] = None
    ```

2.  **Add it to `scripts/setup_secrets.sh`**:
    Add it to the `SECRETS` array:
    ```bash
    SECRETS=(
        ...
        "MY_NEW_SECRET:Enter value for My New Secret"
        "MEDPLUM_BASE_URL:Enter Medplum Base URL"
    )
    ```

3.  **Run the Setup Script** (or manually create it in GCP Console):
    ```bash
    ./scripts/setup_secrets.sh <GCP_PROJECT_ID>
    ```

## Key Rotation

1.  Add a new version to the secret in GCP Console (or via gcloud).
2.  Restart the Cloud Run service (or backend process). The app creates a new client and fetches the *latest* version on startup.

## Troubleshooting

- **App failing to start**: Check logs for "Warning: Failed to initialize Secret Manager client". Ensure the service account has `Secret Manager Secret Accessor` role.
- **Secret not picked up**: Ensure the secret name in GCP matches the `Settings` field name exactly (case-sensitive).
