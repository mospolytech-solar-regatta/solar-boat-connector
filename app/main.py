from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.BoatAPI import BoatAPI
from app.BoatAPI import set_app, set_controllers
from app.config.config import Config
from app.controllers import Controllers
from app.routers import state, serial, actions, websockets, race
from background.listener import create_listener, get_listener
from store.migrator import AlembicMigrator

api = FastAPI()

api.include_router(state.router)
api.include_router(serial.router)
api.include_router(actions.router)
api.include_router(websockets.router)
api.include_router(race.router)


@api.on_event("startup")
async def startup_event():
    app = BoatAPI(Config())
    set_app(app)
    set_controllers(Controllers())
    origins = app.config.allow_origin
    # migrator = AlembicMigrator()
    # migrator.migrate_to_latest()
    api.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    listener = create_listener()
    await listener.listen()


@api.on_event("shutdown")
async def shutdown_event():
    await get_listener().stop()


@api.get("/")
async def root():
    return {}
