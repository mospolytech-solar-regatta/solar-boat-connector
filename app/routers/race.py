from fastapi import APIRouter, Depends

from app.BoatAPI.context import AppContext
from app.controllers import Controllers
from app.dependencies import get_context, controllers_dep
from app.models import Race

router = APIRouter(prefix='/race')


@router.get("/start")
async def start_race(ctx: AppContext = Depends(get_context),
                     controllers: Controllers = Depends(controllers_dep)):
    race: Race = await controllers.race_controller.start_new_race(ctx)


@router.get("/stop")
async def stop_race(ctx: AppContext = Depends(get_context),
                    controllers: Controllers = Depends(controllers_dep)):
    await controllers.race_controller.stop(ctx)
