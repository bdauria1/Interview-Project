from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Krevera API"
    ENV: str = "local"
    DEBUG: bool = True
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True,)

settings = Settings()
