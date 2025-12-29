import pytest
from unittest.mock import MagicMock, patch

from app.core import secrets_loader
from app.core.config import Settings
from app.core.secrets_loader import SecretManagerSettingsSource

def test_secret_manager_loader_disabled():
    """Verify loader does nothing if USE_SECRET_MANAGER is false"""
    with patch.dict("os.environ", {"USE_SECRET_MANAGER": "false", "GCP_PROJECT_ID": "test-proj"}):
        source = SecretManagerSettingsSource(Settings)
        data = source()
        assert data == {}

def test_secret_manager_loader_enabled():
    """Verify loader fetches secrets when enabled"""
    if secrets_loader.secretmanager is None:
        pytest.skip("google-cloud-secret-manager not installed")
    with patch("app.core.secrets_loader.secretmanager.SecretManagerServiceClient") as mock_client_cls:
        # Setup mock client
        mock_client = MagicMock()
        mock_client_cls.return_value = mock_client

        # Setup mock response for access_secret_version
        mock_response = MagicMock()
        mock_response.payload.data.decode.return_value = "secret-value-from-gcp"
        mock_client.access_secret_version.return_value = mock_response

        # Force enable
        with patch.dict("os.environ", {"USE_SECRET_MANAGER": "true", "GCP_PROJECT_ID": "test-proj"}):
            source = SecretManagerSettingsSource(Settings)

            # Test finding a specific secret, e.g. TG_API_KEY
            # Note: The source iterates over ALL fields in settings.
            # We mock the client to return 'secret-value-from-gcp' for ANY secret request.

            data = source()

            # We expect the loader to have tried to fetch TG_API_KEY
            # and populate it in the returned dict
            assert data.get("TG_API_KEY") == "secret-value-from-gcp"

            # Verify Medplum secrets are also attempted
            assert data.get("MEDPLUM_BASE_URL") == "secret-value-from-gcp"

            # Verify call arguments
            mock_client.access_secret_version.assert_any_call(
                request={"name": "projects/test-proj/secrets/TG_API_KEY/versions/latest"}
            )
            mock_client.access_secret_version.assert_any_call(
                request={"name": "projects/test-proj/secrets/MEDPLUM_BASE_URL/versions/latest"}
            )
