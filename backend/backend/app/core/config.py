import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_KEY: str = os.getenv("API_KEY", "your-default-api-key-here")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    class Config:
        env_file = ".env"

settings = Settings() 