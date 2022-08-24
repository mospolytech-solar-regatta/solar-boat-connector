from fastapi import APIRouter, Depends

from app.config.app_config import AppConfig
from app.dependencies import get_config
from app.models.request_models import PointSet, State

router = APIRouter(prefix='/action')


@router.get('/lap_point/', response_model=PointSet)
async def set_lap_point(cfg: AppConfig = Depends(get_config)):
    redis = cfg.redis.get_redis()
    return await State.set_point(redis)


@router.get('/reset_point/', response_model=str)
async def reset(cfg: AppConfig = Depends(get_config)):
    redis = cfg.redis.get_redis()
    await State.reset(redis)
    return "ok"


@router.get('/reset_distance/', response_model=str)
async def reset(cfg: AppConfig = Depends(get_config)):
    redis = cfg.redis.get_redis()
    await State.reset(redis)
    return "ok"
