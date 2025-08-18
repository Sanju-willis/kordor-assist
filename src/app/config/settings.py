# src\app\config\settings.py
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
