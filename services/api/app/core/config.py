from pydantic_settings import BaseSettings
from typing import Optional

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

    class Config:
        env_file = ".env"

settings = Settings()
