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
    telemetry_channel: str
    config_apply_channel: str
    config_channel: str

    @staticmethod
    def from_app_config(cfg: Config):
        return RedisConfig(dsn=cfg.redis_dsn, telemetry_channel=cfg.redis_telemetry_channel,
                           config_apply_channel=cfg.redis_config_apply_channel, config_channel=cfg.redis_config_channel)
