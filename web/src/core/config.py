from functools import lru_cache
from pydantic import computed_field # Для вычисляемых полей в Pydantic v2
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- Telegram Bot Settings ---
    BOT_TOKEN: str
    DOMAIN_NAME: str
    WEBHOOK_PATH: str
    WEBHOOK_SECRET: str

    # --- PostgreSQL Settings ---
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int

    # --- Redis Settings ---
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PASSWORD: str

    # --- Nginx & SSL Settings---
    ALLOWED_HOST: str | None
    LETSENCRYPT_EMAIL: str | None

    @computed_field
    @property
    def WEBHOOK_URL(self) -> str:
        path = self.WEBHOOK_PATH if self.WEBHOOK_PATH.startswith("/") else f"/{self.WEBHOOK_PATH}"
        return f"https://{self.DOMAIN_NAME}{path}"

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @computed_field
    @property
    def REDIS_URL(self) -> str:
        password_part = f":{self.REDIS_PASSWORD}@" if self.REDIS_PASSWORD else ""
        return f"redis://{password_part}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra='ignore'
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
