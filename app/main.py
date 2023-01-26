from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import context
from background.listener import create_listener, get_listener
from app.config.app_config import AppConfig
from app.config.config import Config
from store.migrator import AlembicMigrator
from app.routers import state, serial, actions, websockets, race

app = FastAPI()

app.include_router(state.router)
app.include_router(serial.router)
app.include_router(actions.router)
app.include_router(websockets.router)
app.include_router(race.router)


@app.on_event("startup")
async def startup_event():
    cfg = AppConfig(Config())
    context.set_config(cfg)
    origins = cfg.config.allow_origin
    migrator = AlembicMigrator()
    migrator.migrate_to_latest()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    listener = create_listener()
    await listener.listen()

@app.on_event("shutdown")
async def shutdown_event():
    await get_listener().stop()


@app.get("/")
async def root():
    return {}
