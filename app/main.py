from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import context
from app.config.app_config import AppConfig
from app.config.config import Config
from app.routers import state, serial, actions

app = FastAPI()

app.include_router(state.router)
app.include_router(serial.router)
app.include_router(actions.router)


@app.on_event("startup")
def startup_event():
    cfg = AppConfig(Config())
    context.set_config(cfg)
    origins = cfg.config.allow_origin
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/")
async def root():
    return {}
