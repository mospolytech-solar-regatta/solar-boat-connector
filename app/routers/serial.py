from fastapi import APIRouter, Depends

from app.BoatAPI.context import AppContext
from app.dependencies import get_context
from app.models import serial

router = APIRouter(prefix='/serial')


@router.get("/config/", response_model=serial.SerialConfig)
async def get_serial_config(ctx: AppContext = Depends(get_context)):
    res = await serial.SerialConfig.get(ctx)
    return res


@router.post("/config/", response_model=serial.SerialConfig)
async def post_serial_config(config: serial.SerialConfig, ctx: AppContext = Depends(get_context)):
    await config.apply(ctx)
    return config
