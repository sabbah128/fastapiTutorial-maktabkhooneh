from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Annotated
from pydantic import Field


class Settings (BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///../sqlite.db"
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()