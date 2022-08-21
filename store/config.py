from pydantic import BaseModel
from app.config.config import Config


class PostgresConfig(BaseModel):
    db: str
    password: str
    server: str
    user: str
    port: int

    @staticmethod
    def from_app_config(cfg: Config):
        return PostgresConfig(user=cfg.postgres_user, password=cfg.postgres_password, server=cfg.postgres_server,
                              port=cfg.postgres_port, db=cfg.postgres_db)


class RedisConfig(BaseModel):
    dsn: str

    @staticmethod
    def from_app_config(cfg: Config):
        return RedisConfig(dsn=cfg.redis_dsn)
