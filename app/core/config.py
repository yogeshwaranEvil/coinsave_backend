# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "cross_border_tracker"
    
    class Config:
        env_file = ".env"

settings = Settings()