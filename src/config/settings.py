import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    A configuration settings class.

    Attributes:
        PG_USER (str): The username for the PostgreSQL database.
        PG_PASSWORD (str): The password for the PostgreSQL database.
        PG_DB (str): The name of the PostgreSQL database.
        DATABASE_URL (str): The URL of the PostgreSQL database.
        SECRET_KEY (str): The secret key used for JWT token encoding and decoding.
        ALGORITHM (str): The encryption algorithm used for JWT token encoding and decoding.
        ACCESS_TOKEN_EXPIRATION_MINUTES (int): The expiration time (in minutes) for access tokens.
        GENERAL_EXPIRES_IN_MINUTES (int): The expiration time (in minutes) for general tokens.
        EMAIL_HOST (str): The hostname of the email server.
        EMAIL_HOST_USER (str): The username for the email server.
        EMAIL_HOST_PASSWORD (str): The password for the email server.
        EMAIL_PORT (int): The port number for the email server.

    Config:
        env_file (str): The name of the file containing environment variables.
        env_file_encoding (str): The encoding of the environment variables file.
    """

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
