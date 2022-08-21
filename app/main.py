import json

from aioredis import Redis
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

import constants
from background.tasks import get_config, set_config, SerialConfig
from app.models.request_models import State, PointSet
from app import context
from app.config.app_config import AppConfig
from app.config.config import Config
from app.routers import state

origins = constants.ALLOWED_ORIGIN

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(state.router)


@app.on_event("startup")
def startup_event():
    cfg = Config()
    context.set_config(AppConfig(cfg))


@app.get("/")
async def root():
    return {}


@app.get("/serial_config/", response_model=SerialConfig)
async def get_serial_config():
    res = get_config.delay()
    res = res.get()
    return SerialConfig(**json.loads(res))


@app.post("/serial_config/", response_model=SerialConfig)
async def get_serial_config(config: SerialConfig):
    res = set_config.delay(config.dict())
    res = res.get()
    res = SerialConfig(**json.loads(res))
    return res


# @app.get('/set_lap_point/', response_model=PointSet)
# async def set_lap_point(redis: Redis = Depends(get_redis)):
#     return await State.set_point(redis)
