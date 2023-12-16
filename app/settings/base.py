import secrets

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Test Fastapi"

    # minutes * hours * days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    TOKEN_URL = "/login/access-token"

    # database connection
    DATABASE_USER: str = None
    DATABASE_PASSWORD:str = None
    DATABASE_HOST:str = None
    DATABASE_PORT:str = None
    DATABASE_NAME:str = None

    ALGORITHM = "HS256"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
