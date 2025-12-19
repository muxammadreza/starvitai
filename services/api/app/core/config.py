from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MEDPLUM_BASE_URL: str = "http://localhost:8103/"
    MEDPLUM_CLIENT_ID: str = "admin"
    MEDPLUM_CLIENT_SECRET: str
    
    GRAPH_STORE_URL: str
    GRAPH_STORE_TOKEN: str = "secret"

    # API Security
    STARVIT_API_KEY: str

    ANALYTICS_STORE_URL: str = "postgresql://user:password@localhost:5432/starvit_analytics"
    
    class Config:
        env_file = ".env"

settings = Settings()
