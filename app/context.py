from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.client.postgres import PostgresDB
from app.client.redis import RedisDB
from app.client.redis.redis_db import RedisSession


class ContextFactory:
    def __init__(self, redis: RedisDB, db: PostgresDB):
        self.redis = redis
        self.session = db

    async def __call__(self):
        ctx = Context(redis=self.redis.get_session(), session=self.session.get_session())
        try:
            yield ctx
        finally:
            await ctx.close()


class Context(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    redis: RedisSession
    session: Session

    async def close(self, *args):
        await self.redis.close()
        self.session.commit()
        self.session.close()

    @staticmethod
    async def done_callback(ctx, *args):
        await ctx.close()
