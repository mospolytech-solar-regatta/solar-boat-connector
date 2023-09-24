from fastapi import APIRouter

from app.controllers import race_controller
from app.dependencies import context_dep
from app.models import Race

router = APIRouter(prefix='/race')


@router.get("/start/")
async def start_race(ctx: context_dep):
    race: Race = await race_controller.start_new_race(ctx)


@router.get("/stop/")
async def stop_race(ctx: context_dep):
    await race_controller.stop(ctx)
