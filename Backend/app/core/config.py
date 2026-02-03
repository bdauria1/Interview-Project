from pydantic import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Krevera API"
    ENV: str = "local"
    DEBUG: bool = True

    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/krevera"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()
