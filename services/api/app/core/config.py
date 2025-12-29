from typing import Optional, Tuple

from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict


class Settings(BaseSettings):
    # App Mode
    STARVIT_MODE: str = "stub"  # stub | live
    APP_ENV: str = "dev"

    # GCP Healthcare API (PHI Zone)
    GCP_PROJECT_ID: Optional[str] = None
    GCP_LOCATION: str = "us-central1"
    FHIR_DATASET_ID: str = "starvit-fhir"
    FHIR_STORE_ID: str = "main"

    # TigerGraph Savanna (De-ID Graph)
    TG_API_BASE: Optional[str] = None
    TG_API_KEY: Optional[str] = None
    TG_GRAPH_NAME: str = "Starvit"

    # BigQuery (De-ID Analytics)
    BQ_DATASET_ID: str = "starvit_analytics"

    # Auth (JWT)
    JWT_ISSUER: Optional[str] = None
    JWT_AUDIENCE: Optional[str] = None
    JWKS_URL: Optional[str] = None

    # Internal Security
    STARVIT_API_KEY: Optional[str] = None

    # Medplum
    MEDPLUM_BASE_URL: Optional[str] = None
    MEDPLUM_FHIR_BASE_URL: Optional[str] = None
    MEDPLUM_OAUTH_TOKEN_URL: Optional[str] = None
    MEDPLUM_BACKEND_CLIENT_ID: Optional[str] = None
    MEDPLUM_BACKEND_CLIENT_SECRET: Optional[str] = None
    MEDPLUM_AUTH_ME_URL: Optional[str] = None
    MEDPLUM_POLICY_PATIENT: str = "PatientPortalPolicy"
    MEDPLUM_POLICY_CLINICIAN: str = "ClinicianPolicy"
    MEDPLUM_POLICY_RESEARCH: str = "ResearcherReadOnlyPolicy"
    MEDPLUM_POLICY_BACKEND_SERVICE: str = "BackendServicePolicy"

    USE_SECRET_MANAGER: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        from app.core.secrets_loader import SecretManagerSettingsSource
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            SecretManagerSettingsSource(settings_cls),
            file_secret_settings,
        )


settings = Settings()
