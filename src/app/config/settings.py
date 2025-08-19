# src\app\config\settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ValidationError as PydValidationError
from app.middleware.exceptions import ConfigError

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    APP_NAME: str
    HOST: str
    PORT: int
    DEBUG: bool
    JWT_SECRET: str
    JWT_ALGORITHM: str 

try:
    settings: Settings = Settings()  # pyright: ignore[reportCallIssue]
    # alternatively:  # type: ignore[call-arg]
except PydValidationError as e:
    missing = [str(err["loc"][0]) for err in e.errors() if err.get("type") == "missing"]
    if missing:
        raise ConfigError(f"Missing required env vars: {', '.join(missing)}")
    msgs = [f"{'.'.join(map(str, err.get('loc', ())))}: {err.get('msg')}" for err in e.errors()]
    raise ConfigError("Config error: " + "; ".join(msgs))
