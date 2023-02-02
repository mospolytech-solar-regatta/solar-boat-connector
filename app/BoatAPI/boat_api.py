from app.config.config import Config
from store.config import PostgresConfig, RedisConfig
from store.postgres import PostgresDB
from store.redis_db import RedisDB


class BoatAPI:
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
