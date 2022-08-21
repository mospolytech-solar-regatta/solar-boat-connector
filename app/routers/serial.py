import json

from fastapi import APIRouter

from background import tasks

router = APIRouter(prefix='/serial')


@router.get("/config/", response_model=tasks.SerialConfig)
async def get_serial_config():
    res = tasks.get_config.delay()
    res = res.get()
    return tasks.SerialConfig(**json.loads(res))


@router.post("/config/", response_model=tasks.SerialConfig)
async def get_serial_config(config: tasks.SerialConfig):
    res = tasks.set_config.delay(config.dict())
    res = res.get()
    res = tasks.SerialConfig(**json.loads(res))
    return res
