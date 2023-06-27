import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL_HOST: str
    DATABASE_URL_PORT: str
    DATABASE_URL_USER: str
    DATABASE_URL_PASSWORD: str
    DATABASE_URL_DB: str

    class Config:
        env_file = os.getenv('ENV_FILE')


settings = Settings()
