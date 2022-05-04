import json

from aioredis import Redis
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import constants
from background.tasks import read_data, SerialConfig
from models.request_models import Telemetry
from store.redis import get_redis
from store.postgres import get_db
from background.tasks import get_config, set_config
from fastapi.middleware.cors import CORSMiddleware

load_dotenv('.env', override=True)
origins = constants.ALLOWED_ORIGIN

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/current_state/")
async def post_current_state(telemetry: Telemetry, redis: Redis = Depends(get_redis),
                             session: Session = Depends(get_db)):
    return await telemetry.save_current_state(redis, session)


@app.get("/current_state/", response_model=Telemetry)
async def get_current_state(redis: Redis = Depends(get_redis)):
    try:
        return await Telemetry.get_current_state(redis)
    except FileNotFoundError:
        return JSONResponse(status_code=404, content={'message': 'key not found'})


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
