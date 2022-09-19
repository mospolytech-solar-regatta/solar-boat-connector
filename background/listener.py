import json
import asyncio
from app.config.app_config import AppConfig
from app.models.request_models import Telemetry


class Listener:
    def __init__(self, config: AppConfig):
        self.config = config
        self.redis = config.redis
        self.db = config.db
        self.task = None
        self.pubsub = self.redis.get_redis().pubsub()

    async def listen(self):
        await self.pubsub.subscribe(**{self.config.config.redis_telemetry_channel: self.listen_telemetry})
        self.task = asyncio.create_task(self.pubsub.run())

    def listen_telemetry(self, msg):
        data = json.loads(msg['data'].decode('UTF-8'))
        telemetry = Telemetry(**data)
        redis = self.redis.get_redis()
        session = self.db.get_session()
        task = asyncio.create_task(telemetry.save_current_state(redis, session))
        task.add_done_callback(lambda ctx: (asyncio.create_task(redis.close()), session.close()))

    async def stop(self):
        self.task.cancel()
        await self.task
