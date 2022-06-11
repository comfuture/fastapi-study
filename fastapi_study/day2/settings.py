from typing import Union
from functools import lru_cache
from pydantic import BaseSettings, FileUrl, PostgresDsn, AnyUrl


class Settings(BaseSettings):
    """local config"""
    # database_dsn: Union[FileUrl, PostgresDsn] = 'sqlite:///./test.db'
    database_dsn: str = 'sqlite:///./test.db'

    class Config:
        env_file = 'fastapi_study/day2/.env'


@lru_cache()
def use_settings():
    """injects settings dependency"""
    return Settings()
