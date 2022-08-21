from pydantic import BaseSettings


class Config(BaseSettings):
    postgres_db: str
    postgres_password: str
    postgres_server: str
    postgres_user: str
    postgres_port: int
    redis_dsn: str
    celery_config_module: str
    allow_origin: str = '["*"]'
    origin: str = "http://localhost:8000"

    class Config:
        env_file = ".env"


