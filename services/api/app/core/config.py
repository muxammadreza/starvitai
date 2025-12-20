from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # App Mode
    STARVIT_MODE: str = "stub"  # stub | live
    APP_ENV: str = "dev"

    # Medplum Config
    MEDPLUM_BASE_URL: str = "http://localhost:8103/"
    MEDPLUM_CLIENT_ID: Optional[str] = "admin"
    MEDPLUM_CLIENT_SECRET: Optional[str] = None
    
    # JWT Verification
    MEDPLUM_JWKS_URL: Optional[str] = None
    MEDPLUM_JWT_ISSUER: str = "http://localhost:8103/"
    MEDPLUM_JWT_AUDIENCE: str = "http://localhost:8103/"

    # Backing Services
    GRAPH_STORE_URL: Optional[str] = None
    GRAPH_STORE_TOKEN: Optional[str] = None
    ANALYTICS_STORE_URL: Optional[str] = None
    
    # Internal Security
    STARVIT_API_KEY: Optional[str] = None # Only for internal service-to-service

    class Config:
        env_file = ".env"

settings = Settings()
