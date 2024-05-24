import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    class RedisSettings(BaseSettings):
        host: str = os.environ.get('REDIS_SERVER', 'localhost')
        port: int = os.environ.get('REDIS_PORT', '6379')
        db: int = os.environ.get('REDIS_DB', '1')

    LOG_LEVEL: str = os.environ.get('LOG_LEVEL', 'DEBUG')  # CRITICAL -> ERROR -> WARNING -> INFO -> DEBUG -> NOTSET

    Redis: RedisSettings = RedisSettings()

    model_config = SettingsConfigDict(env_file='.env',
                                      extra='ignore')


settings = Settings()
