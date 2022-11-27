from pydantic import BaseSettings


class Config(BaseSettings):
    postgres_db: str
    postgres_password: str
    postgres_server: str
    postgres_user: str
    postgres_port: int
    redis_dsn: str
    redis_telemetry_channel: str
    redis_config_channel: str
    redis_config_apply_channel: str
    redis_land_queue_channel: str
    allow_origin: str = '["*"]'
    origin: str = "http://localhost:8000"

    class Config:
        env_file = ".env"


