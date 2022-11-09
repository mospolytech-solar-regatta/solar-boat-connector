import asyncio

from sqlalchemy.orm import Session
from store.redis_db import RedisContext

app_config = None
listener = None


class AppContext:
    def __init__(self, cfg):
        self.redis = RedisContext(cfg.redis)
        self.session: Session = cfg.db.get_session()

    async def close(self):
        await self.redis.close()
        self.session.commit()
        self.session.close()

    @staticmethod
    async def done_callback(ctx, *args):
        await ctx.close()


def set_config(cfg):
    global app_config
    app_config = cfg


def get_config():
    return app_config
