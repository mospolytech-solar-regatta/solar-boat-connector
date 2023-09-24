from app.client import RedisEventsClient
from app.context import ContextFactory, Context


class EventWrapper:
    def __init__(self, client: RedisEventsClient, context_factory: ContextFactory):
        self.client = client
        self.context_factory = context_factory

    def add_subscription(self, topic: str, handler):
        self.client.add_subscription(topic, self.__subscription_wrapper(handler))

    def listen(self):
        return self.client.listen()

    def stop(self):
        return self.client.stop()

    def __subscription_wrapper(self, func):
        async def f(msg):
            ctx = await self.get_context()
            return await func(ctx, msg)

        return f

    async def get_context(self) -> Context:
        return await self.context_factory.__call__().__anext__()
