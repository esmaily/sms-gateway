import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """
        Represents the application's configuration settings.

        This class defines the settings required for connecting to a database.

        Attributes:
            DB_DRIVER (str): The database driver to be used (e.g., 'mysql', 'postgresql').
            DB_SERVER (str): The server or host where the database is located.
            DB_USER (str): The username used to authenticate with the database.
            DB_PORT (str): The port number on which the database is accessible.
            DB_PASSWORD (str): The password used for authentication.
            DB_NAME (str): The name of the database to connect to.
            DB_URL (str, optional): The full database URL (optional).

        Note:
            All attributes except 'DB_URL' are required and should be provided through environment variables.

        """
    DB_DRIVER: str = Field(..., env='DB_DRIVER')
    DB_SERVER: str = Field(..., env='DB_SERVER')
    DB_USER: str = Field(..., env='DB_USER')
    DB_PORT: str = Field(..., env='DB_PORT')
    DB_PASSWORD: str = Field(..., env='DB_PASSWORD')
    DB_NAME: str = Field(..., env='DB_NAME')
    DB_URL: str = None


settings = Settings()
settings.DB_URL = f"{settings.DB_DRIVER}://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_SERVER}:{settings.DB_PORT}/{settings.DB_NAME}"
