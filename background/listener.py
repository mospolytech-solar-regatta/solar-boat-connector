import asyncio
import json
import logging
import traceback

import async_timeout
from redis.asyncio.client import PubSub

from app.BoatAPI.context import AppContext
from app.dependencies import get_context, controllers_dep
from app.entities.telemetry import Telemetry
from app.models.serial import SerialConfig

listener = None


class Listener:

    def __init__(self):
        self.task = None
        self.pubsub = None

    async def get_context(self):
        return await get_context().__anext__()

    async def get_controllers(self):
        return await controllers_dep().__anext__()

    async def listen(self):
        ctx = await self.get_context()
        redis = ctx.redis
        self.pubsub = await redis.pubsub()
        await self.pubsub.subscribe(**{redis.config.telemetry_channel: self.listen_telemetry,
                                       redis.config.config_apply_channel: self.listen_config})
        self.task = asyncio.create_task(self.run(self.pubsub))

    async def listen_telemetry(self, msg):
        data = json.loads(msg['data'])
        telemetry = Telemetry(**data)
        ctx = await self.get_context()
        controllers = await self.get_controllers()
        task = asyncio.create_task(controllers.state_controller.save_current_state(telemetry, ctx))
        task.add_done_callback(lambda context: asyncio.create_task(AppContext.done_callback(ctx)))

    async def listen_config(self, msg):
        data = json.loads(msg['data'])
        cfg = SerialConfig(**data['config'])
        ctx = await self.get_context()
        task = asyncio.create_task(cfg.update(ctx))
        task.add_done_callback(lambda context: asyncio.create_task(AppContext.done_callback(ctx)))

    async def stop(self):
        self.task.cancel()

    async def run(self, channel: PubSub):
        while True:
            try:
                async with async_timeout.timeout(1):
                    message = await channel.get_message(ignore_subscribe_messages=True, timeout=1)
                    if message is not None:
                        print(f"(Reader) Message Received: {message}")
                    await asyncio.sleep(0.01)
            except asyncio.TimeoutError:
                pass
            except Exception as exc:
                logging.log(logging.ERROR, exc)
                traceback.print_exc()


def create_listener():
    global listener
    listener = Listener()
    return listener


def get_listener():
    global listener
    return listener
