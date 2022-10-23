from fastapi import APIRouter, Depends

from app.context import AppContext
from app.dependencies import get_context
from app.models.race import Race

router = APIRouter(prefix='/race')


@router.post("/start")
async def start_race(ctx: AppContext = Depends(get_context)):
    race: Race = await Race.start_new_race(ctx)
    race.save(ctx)
