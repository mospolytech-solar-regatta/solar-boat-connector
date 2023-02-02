from app.BoatAPI import BoatAPI


class AppContext:
    def __init__(self, app: BoatAPI):
        self.redis = app.redis.get_session()
        self.session = app.db.get_session()

    async def close(self):
        await self.redis.close()
        self.session.commit()
        self.session.close()

    @staticmethod
    async def done_callback(ctx, *args):
        await ctx.close()
