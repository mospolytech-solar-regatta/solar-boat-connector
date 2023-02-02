from app.BoatAPI import get_app, get_controllers
from app.BoatAPI.context import AppContext


async def get_context():
    app = get_app()
    if type(app) is None:
        raise NotImplementedError("app not configured")

    ctx = AppContext(app)
    try:
        yield ctx
    finally:
        await ctx.close()


async def controllers_dep():
    c = get_controllers()
    if type(c) is None:
        raise NotImplementedError("controllers not configured")

    yield c
