from fastapi import APIRouter, Depends

from app.context import AppContext
from app.dependencies import get_context
from app.models.race import Race

router = APIRouter(prefix='/race')


@router.post("/start")
async def start_race(ctx: AppContext = Depends(get_context)):
    race: Race = await Race.start_new_race(ctx)


@router.post("/stop")
async def stop_race(ctx: AppContext = Depends(get_context)):
    cur_race: Race = await Race.get_current_race(ctx)
    await cur_race.stop(ctx)
