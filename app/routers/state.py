from fastapi.routing import APIRouter
from fastapi import Depends
from fastapi.responses import JSONResponse
from app.dependencies import get_config
from app.models.request_models import State, Telemetry, TelemetrySaveStatus
from background.tasks import send
from app.config.app_config import AppConfig

router = APIRouter(prefix='/state', responses={404: {"description": "Not found"}})


@router.post("/")
async def post_current_state(telemetry: Telemetry, cfg: AppConfig = Depends(get_config)):
    redis = cfg.redis.get_redis()
    session = cfg.db.get_session()
    res = await telemetry.save_current_state(redis, session)
    if res == TelemetrySaveStatus.PERM_SAVED:
        send.delay(telemetry.json())
    return JSONResponse({'status': 'success'})


@router.get("/", response_model=State)
async def get_current_state(cfg: AppConfig = Depends(get_config)):
    redis = cfg.redis.get_redis()
    try:
        return await State.get_current_state(redis)
    except FileNotFoundError:
        return JSONResponse(status_code=404, content={'message': 'key not found'})
