from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MEDPLUM_BASE_URL: str = "http://localhost:8103/"
    MEDPLUM_CLIENT_ID: str = "admin"
    MEDPLUM_CLIENT_SECRET: str = "secret"
    
    GRAPH_STORE_URL: str = "http://localhost:9000"
    GRAPH_STORE_TOKEN: str = "secret"

    ANALYTICS_STORE_URL: str = "postgresql://user:password@localhost:5432/starvit_analytics"
    
    class Config:
        env_file = ".env"

settings = Settings()
