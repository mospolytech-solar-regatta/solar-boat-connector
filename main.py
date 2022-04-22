import json
import os

from aioredis import Redis
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from background.tasks import read_data, SerialConfig
from models.request_models import Telemetry
from store.redis import get_redis
from store.postgres import get_db
from background.tasks import get_config

load_dotenv('.env', override=True)

app = FastAPI()


@app.get("/")
async def root():
    res = read_data.delay()
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
