from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.client import redis_cfg
from app.config import Config
from app.handlers import state, serial, actions, websockets, race, events_handler
from app.wrapper import event_wrapper

api = FastAPI()

api.include_router(state.router)
api.include_router(serial.router)
api.include_router(actions.router)
api.include_router(websockets.router)
api.include_router(race.router)

config = Config()
origins = config.allow_origin
# migrator = AlembicMigrator()
# migrator.migrate_to_latest()
api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.on_event("startup")
async def startup_event():
    event_wrapper.add_subscription(redis_cfg.telemetry_channel, events_handler.handle_telemetry)
    await event_wrapper.listen()


@api.on_event("shutdown")
async def shutdown_event():
    await event_wrapper.stop()


@api.get("/")
async def root():
    return {}
