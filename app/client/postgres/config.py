from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_prefix = 'postgres_')

    db: str
    password: str = 'postgres'
    server: str = '127.0.0.1'
    user: str = 'postgres'
    port: int = '5433'
