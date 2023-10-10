import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    DB_DRIVER: str = Field(..., env='DB_DRIVER')
    DB_SERVER: str = Field(..., env='DB_SERVER')
    DB_USER: str = Field(..., env='DB_USER')
    DB_PORT: str = Field(..., env='DB_PORT')
    DB_PASSWORD: str = Field(..., env='DB_PASSWORD')
    DB_NAME: str = Field(..., env='DB_NAME')
    DB_URL: str = None


settings = Settings()
settings.DB_URL = f"{settings.DB_DRIVER}://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_SERVER}:{settings.DB_PORT}/{settings.DB_NAME}"
