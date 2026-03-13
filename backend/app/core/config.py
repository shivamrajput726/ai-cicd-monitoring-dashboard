from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI CI/CD Monitoring API"
    env: str = "development"
    debug: bool = True

    backend_cors_origins: list[str] = ["http://localhost:5173"]

    database_url: str = "postgresql+psycopg://app:app@db:5432/app"

    jwt_secret_key: str = "CHANGE_ME_SECRET"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 24 * 7

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()

