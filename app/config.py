"""
Файл читающий конфигурацию из .env 
"""

from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    """Настройки работы программы"""
    secret_key: str
    algo: str
    access_token_expire_minutes: int
    db_username: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
