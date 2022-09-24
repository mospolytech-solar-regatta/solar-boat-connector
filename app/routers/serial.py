import json

from fastapi import APIRouter, Depends

from app.config.app_config import AppConfig
from app.context import get_config
from app.models import serial

router = APIRouter(prefix='/serial')


@router.get("/config/", response_model=serial.SerialConfig)
async def get_serial_config(cfg: AppConfig = Depends(get_config)):
    redis = cfg.redis.get_redis()
    res = await serial.get_serial_config(redis)
    res = serial.SerialConfig(**json.loads(res))
    return res


@router.post("/config/", response_model=serial.SerialConfig)
async def post_serial_config(config: serial.SerialConfig, cfg: AppConfig = Depends(get_config)):
    redis = cfg.redis.get_redis()
    await redis.publish(cfg.config.redis_config_channel, config.json())
    return config
