import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    PG_USER: str = os.getenv("PG_USER", default="")
    PG_PASSWORD: str = os.getenv("PG_PASSWORD", default="")
    PG_DB: str = os.getenv("PG_DB", default="fastapi")
    DATABASE_URL: str = os.getenv("DATABASE_URL", default="")

    SECRET_KEY: str = os.getenv("SECRET_KEY", default="secretkey")
    ALGORITHM: str = os.getenv("ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRATION_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRATION_MINUTES", default=30))
    GENERAL_EXPIRES_IN_MINUTES: int = int(os.getenv("GENERAL_EXPIRES_IN_MINUTES", default=5))

    EMAIL_HOST: str = os.getenv("EMAIL_HOST", default="")
    EMAIL_HOST_USER: str = os.getenv("EMAIL_HOST_USER", default="")
    EMAIL_HOST_PASSWORD: str = os.getenv("EMAIL_HOST_PASSWORD", default="")
    EMAIL_PORT: int = int(os.getenv("EMAIL_PORT", default=2525))

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
