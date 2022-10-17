from app import context
from app.config.app_config import BaseConfig
from app.context import AppContext


async def get_context():
    if type(context.app_config) == BaseConfig.__class__:
        raise NotImplementedError("app not configured")

    ctx = AppContext(context.app_config)
    try:
        yield ctx
    finally:
        await ctx.close()
