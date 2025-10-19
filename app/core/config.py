from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Database Configuration
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "bagbankdb"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "sami1233"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    ALLOWED_HOSTS: str = '["http://localhost:3000", "http://127.0.0.1:3000"]'
    
    @property
    def allowed_hosts_list(self) -> List[str]:
        import json
        return json.loads(self.ALLOWED_HOSTS)
    
    # Environment
    ENVIRONMENT: str = "development"
    
    @property
    def database_url(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

