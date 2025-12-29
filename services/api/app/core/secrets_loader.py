import os
from typing import Any, Dict, Tuple

try:
    from google.cloud import secretmanager
except Exception:  # pragma: no cover - dependency may be absent in local tooling
    secretmanager = None
from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource

class SecretManagerSettingsSource(PydanticBaseSettingsSource):
    """
    A Pydantic Settings Source that loads secrets from Google Cloud Secret Manager.
    It maps environment variable names to Secret Manager secret names.
    """
    def __init__(self, settings_cls: type[BaseSettings]):
        super().__init__(settings_cls)
        self.project_id = os.getenv("GCP_PROJECT_ID")
        self.use_secret_manager = os.getenv("USE_SECRET_MANAGER", "false").lower() == "true"
        self._client = None

    @property
    def client(self):
        if self._client is None and self.use_secret_manager and self.project_id:
            if secretmanager is None:
                print("Warning: google-cloud-secret-manager is not installed; skipping Secret Manager.")
                return None
            try:
                self._client = secretmanager.SecretManagerServiceClient()
            except Exception as e:
                # Fallback or log if client init fails (e.g. no creds)
                # In strict mode we might want to raise, but for now we warn
                print(f"Warning: Failed to initialize Secret Manager client: {e}")
        return self._client

    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> Tuple[Any, str, bool]:
        # Not used directly in this implementation pattern for Pydantic v2 usually,
        # but required by abstract base class if we don't override __call__ differently.
        # We'll implement the main logic in __call__.
        return None, field_name, False

    def __call__(self) -> Dict[str, Any]:
        """
        Load settings from Secret Manager.
        """
        if not self.use_secret_manager or not self.project_id or not self.client:
            return {}

        d: Dict[str, Any] = {}
        
        # Iterate over all fields in the settings model
        for field_name, field in self.settings_cls.model_fields.items():
            # We assume the secret name in GCP matches the field name (or env var name)
            # You could add a prefix here if needed, e.g. f"starvit-backend-{field_name}"
            secret_id = field_name
            
            try:
                name = f"projects/{self.project_id}/secrets/{secret_id}/versions/latest"
                response = self.client.access_secret_version(request={"name": name})
                value = response.payload.data.decode("UTF-8")
                d[field_name] = value
            except Exception:
                # If secret doesn't exist or we can't access it, skip.
                # Pydantic will fall back to env vars or defaults.
                pass
                
        return d

    def prepare_field_value(
        self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool
    ) -> Any:
        return value
