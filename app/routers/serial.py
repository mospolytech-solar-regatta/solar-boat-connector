import json

from fastapi import APIRouter, Depends

from app.config.app_config import AppConfig
from app.context import get_config
from app.models.serial import SerialConfig

router = APIRouter(prefix='/serial')


# @router.get("/config/", response_model=SerialConfig)
# async def get_serial_config():
#     res = tasks.get_config.delay()
#     res = res.get()
#     return tasks.SerialConfig(**json.loads(res))


@router.post("/config/", response_model=SerialConfig)
async def post_serial_config(config: SerialConfig, cfg: AppConfig = Depends(get_config)):
    redis = cfg.redis.get_redis()
    await redis.publish(cfg.config.redis_config_channel, config.json())
