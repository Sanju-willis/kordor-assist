# src\app\config\settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

settings: Settings = Settings()  # type: ignore[call-arg]
