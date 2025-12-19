from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MEDPLUM_BASE_URL: str = "http://localhost:8103"
    MEDPLUM_CLIENT_ID: str = "admin"
    MEDPLUM_CLIENT_SECRET: str = "secret"
    
    TIGERGRAPH_URL: str = "http://localhost:9000"
    TIGERGRAPH_TOKEN: str = "secret"
    
    class Config:
        env_file = ".env"

settings = Settings()
