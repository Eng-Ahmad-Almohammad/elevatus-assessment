"""A module that contain global setting to use."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Setting class that will set the values from .env file."""

    DATABASE_URL: str
    SECRET_KEY: str = "add_your_secrete_key_for_hashing"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
