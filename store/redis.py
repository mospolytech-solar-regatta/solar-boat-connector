import aioredis
from aioredis import Redis
from store.config import RedisConfig


class RedisDB:
    def __init__(self, cfg: RedisConfig):
        self.config = cfg
        self.pool = aioredis.ConnectionPool.from_url(cfg.dsn, max_connections=10)
        self.redis = self._create_redis()

    def __del__(self):
        self._stop_connection()

    def get_redis(self):
        return self.redis

    def _stop_connection(self):
        self.redis.close()

    def _create_redis(self) -> Redis:
        redis = aioredis.Redis(connection_pool=self.pool)
        return redis

    # pylint: disable=redefined-builtin
    @staticmethod
    async def set(redis: Redis, key: str, value):
        await redis.set(key, value)

    @staticmethod
    async def get(redis: Redis, key: str):
        return await redis.get(key)
