import json

from fastapi import APIRouter, Depends

from app.dependencies import get_context
from app.context import AppContext, app_config
from app.models import serial

router = APIRouter(prefix='/serial')


@router.get("/config/", response_model=serial.SerialConfig)
async def get_serial_config(ctx: AppContext = Depends(get_context)):
    res = await serial.get_serial_config(ctx)
    res = serial.SerialConfig(**json.loads(res))
    return res


@router.post("/config/", response_model=serial.SerialConfig)
async def post_serial_config(config: serial.SerialConfig, ctx: AppContext = Depends(app_config)):
    await config.apply(ctx)
    return config
