import json
import asyncio

import async_timeout
import redis

from app.config.app_config import AppConfig
from app.models.request_models import Telemetry
from app.models.serial import SerialConfig, serial_config_key


class Listener:

    def __init__(self, config: AppConfig):
        self.config = config
        self.redis = config.redis
        self.db = config.db
        self.task = None
        self.pubsub = self.redis.get_redis().pubsub()

    async def listen(self):
        await self.pubsub.subscribe(**{self.config.config.redis_telemetry_channel: self.listen_telemetry,
                                       self.config.config.redis_config_apply_channel: self.listen_config})
        self.task = asyncio.create_task(self.run(self.pubsub))

    def listen_telemetry(self, msg):
        data = json.loads(msg['data'])
        telemetry = Telemetry(**data)
        redis = self.redis.get_redis()
        session = self.db.get_session()
        task = asyncio.create_task(telemetry.save_current_state(redis, session))
        task.add_done_callback(lambda ctx: (asyncio.create_task(redis.close()), session.close()))

    def listen_config(self, msg):
        data = json.loads(msg['data'])
        cfg = SerialConfig(**data['config'])
        redis = self.redis.get_redis()
        task = asyncio.create_task(redis.set(serial_config_key, cfg.json()))
        task.add_done_callback(lambda ctx: (asyncio.create_task(redis.close())))

    async def stop(self):
        self.task.cancel()

    async def run(self, channel: redis.client.PubSub):
        while True:
            try:
                async with async_timeout.timeout(1):
                    message = await channel.get_message(ignore_subscribe_messages=True, timeout=1)
                    if message is not None:
                        print(f"(Reader) Message Received: {message}")
                    await asyncio.sleep(0.01)
            except asyncio.TimeoutError:
                pass
