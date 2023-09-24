from fastapi import APIRouter

from app.dependencies import context_dep
from app.models import serial

router = APIRouter(prefix='/serial')


@router.get("/config/", response_model=serial.SerialConfig)
async def get_serial_config(ctx: context_dep):
    res = await serial.SerialConfig.get(ctx)
    return res


@router.post("/config/", response_model=serial.SerialConfig)
async def post_serial_config(config: serial.SerialConfig, ctx: context_dep):
    await config.apply(ctx)
    return config
