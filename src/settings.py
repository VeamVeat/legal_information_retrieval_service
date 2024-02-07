from functools import lru_cache

from pydantic_settings import BaseSettings


class SettingsApp(BaseSettings):
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 7003

    class Config:
        env_file = '../.env'


@lru_cache
def get_settings_app() -> SettingsApp:
    return SettingsApp()


settings_app = get_settings_app()
