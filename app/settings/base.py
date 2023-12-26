from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Test Fastapi"
    SECRET_KEY: str = ""

    # token
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # minutes * hours * days
    TOKEN_URL: str = "/login/access-token"

    # database connection
    DATABASE_USER: str = ""
    DATABASE_PASSWORD: str = ""
    DATABASE_HOST: str = ""
    DATABASE_PORT: str = ""
    DATABASE_NAME: str = ""

    SQLALCHEMY_DATABASE_URL: str = ""

    CORS_ORIGINS: list = []

    # test user
    FIRST_SUPERUSER_EMAIL: str = ""
    FIRST_SUPERUSER_PASSWORD: str = ""
    TEST_USER_EMAIL: str = ""
    TEST_USER_PASSWORD: str = ""
    USERS_OPEN_REGISTRATION: bool = True

    model_config = SettingsConfigDict(
        env_file='.credentials/.env',
        extra='allow',
        env_file_encoding='utf-8',
    )


settings = Settings()
