import asyncio
import logging
import traceback

import async_timeout

from app.client.redis import RedisDB


class RedisEventsClient:

    def __init__(self, redis: RedisDB):
        self.task = None
        self.pubsub = None
        self.subscriptions = {}

        self.redis = redis

    def add_subscription(self, topic: str, handler):
        self.subscriptions[topic] = handler

    async def listen(self):
        self.pubsub = await self.redis.get_session().pubsub()

        await self.pubsub.subscribe(**self.subscriptions)
        self.task = asyncio.create_task(self.run())

    async def stop(self):
        self.task.cancel()

    async def run(self):
        while True:
            try:
                async with async_timeout.timeout(1):
                    message = await self.pubsub.get_message(ignore_subscribe_messages=True, timeout=1)
                    if message is not None:
                        print(f"(Reader) Message Received: {message}")
                    await asyncio.sleep(0.01)
            except asyncio.TimeoutError:
                pass
            except Exception as exc:
                logging.log(logging.ERROR, exc)
                traceback.print_exc()
