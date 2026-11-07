"""Settings come from environment variables; the same image runs locally and on a server."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)

    database_url: str = "postgresql+psycopg://allinfarm:allinfarm@localhost:54320/allinfarm"
    smtp_host: str = "localhost"
    smtp_port: int = 1025


@lru_cache
def get_settings() -> Settings:
    return Settings()
