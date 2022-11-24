from pydantic import BaseSettings


class PostgresConfig(BaseSettings):
    db: str
    password: str
    server: str
    user: str
    port: int

    class Config:
        env_prefix = 'postgres_'
        env_file = ".env"


class RedisConfig(BaseSettings):
    dsn: str
    telemetry_channel: str
    config_apply_channel: str
    config_channel: str

    class Config:
        env_prefix = 'redis_'
        env_file = ".env"
