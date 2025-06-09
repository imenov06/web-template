from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    BOT_TOKEN: str
    DOMAIN_NAME: str
    WEBHOOK_PATH: str
    WEBHOOK_SECRET: str

    @property
    def WEBHOOK_URL(self) -> str:
        path = self.WEBHOOK_PATH if self.WEBHOOK_PATH.startswith("/") else f"/{self.WEBHOOK_PATH}"
        return f"https://{self.DOMAIN_NAME}{path}"

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

if __name__ == "__main__":
    print("Загруженные настройки:")
    print(f"BOT_TOKEN: ...{settings.BOT_TOKEN[-5:] if settings.BOT_TOKEN else 'None'}")
    print(f"DOMAIN_NAME: {settings.DOMAIN_NAME}")
    print(f"WEBHOOK_PATH: {settings.WEBHOOK_PATH}")
    print(f"WEBHOOK_URL: {settings.WEBHOOK_URL}")
    print(f"WEBHOOK_SECRET: ...{settings.WEBHOOK_SECRET[-5:] if settings.WEBHOOK_SECRET else 'None'}")