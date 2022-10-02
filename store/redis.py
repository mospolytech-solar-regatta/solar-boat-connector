import redis.asyncio as redis
from redis import Redis
from store.config import RedisConfig
import asyncio


class RedisDB:
    def __init__(self, cfg: RedisConfig):
        self.config = cfg
        self.redis: Redis = redis.from_url(cfg.dsn, decode_responses=True)

    def __del__(self):
        self._stop_connection()

    def get_redis(self):
        return self.redis

    def _stop_connection(self):
        asyncio.run(self.redis.close())

    # pylint: disable=redefined-builtin
    @staticmethod
    async def set(redis: Redis, key: str, value):
        await redis.set(key, value)

    @staticmethod
    async def get(redis: Redis, key: str):
        return await redis.get(key)
