from app.config.config import Config
from store.postgres import PostgresDB, PostgresConfig
from store.redis_db import RedisDB, RedisConfig


class BaseConfig:
    def _create_db(self):
        raise NotImplementedError()

    def _create_redis(self):
        raise NotImplementedError()


class AppConfig(BaseConfig):
    def __init__(self, config: Config):
        self.config = config
        self._create_db()
        self._create_redis()

    def _create_db(self):
        cfg = PostgresConfig()
        self.db = PostgresDB(cfg)

    def _create_redis(self):
        cfg = RedisConfig()
        self.redis = RedisDB(cfg)
