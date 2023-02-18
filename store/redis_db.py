import logging

import redis.asyncio as redis
from fastapi import WebSocket
from redis.asyncio import ConnectionPool, Redis
from redis.asyncio.client import PubSub

from store.config import RedisConfig


class RedisDB:
    def __init__(self, cfg: RedisConfig):
        self.config = cfg
        self.pool = ConnectionPool.from_url(cfg.dsn, decode_responses=True)

    def get_redis(self) -> Redis:
        return redis.Redis(connection_pool=self.pool)

    def get_session(self) -> "RedisContext":
        return RedisContext(self)


class RedisContext:
    def __init__(self, redisDB: RedisDB):
        self.config = redisDB.config
        self.redis = redisDB.get_redis()

    async def close(self):
        return await self.redis.close()

    # pylint: disable=redefined-builtin
    async def set(self, key: str, value):
        return await self.redis.set(key, value)

    async def get(self, key: str):
        return await self.redis.get(key)

    async def publish(self, channel: str, data: str):
        await self.redis.publish(channel, data)

    async def pubsub(self) -> PubSub:
        return self.redis.pubsub()

    async def ws_consume(self, ws: WebSocket, chan):
        pubsub = await self.pubsub()
        await pubsub.subscribe(chan)
        try:
            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1)
                if message:
                    await ws.send_text(message['data'])
        except Exception as exc:
            logging.log(logging.ERROR, exc)
