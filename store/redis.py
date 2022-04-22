import aioredis
from aioredis import Redis

import config

pool = aioredis.ConnectionPool.from_url(config.redis_dsn, max_connections=10)


async def get_redis() -> Redis:
    redis = aioredis.Redis(connection_pool=pool)
    yield redis
    await redis.close()


async def set(redis: Redis, key: str, value):
    val = await redis.set(key, value)


async def get(redis: Redis, key: str):
    return await redis.get(key)
