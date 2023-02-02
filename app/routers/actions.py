from fastapi import APIRouter, Depends

from app.BoatAPI.context import AppContext
from app.controllers import Controllers
from app.dependencies import get_context, controllers_dep
from app.entities import PointSet

router = APIRouter(prefix='/action')


@router.get('/lap_point/', response_model=PointSet)
async def set_lap_point(ctx: AppContext = Depends(get_context),
                        controllers: Controllers = Depends(controllers_dep)):
    return await controllers.state_controller.set_point(ctx)


@router.get('/reset_point/', response_model=str)
async def reset(ctx: AppContext = Depends(get_context),
                controllers: Controllers = Depends(controllers_dep)):
    await controllers.state_controller.reset_point(ctx)
    return "ok"


@router.get('/reset_distance/', response_model=str)
async def reset(ctx: AppContext = Depends(get_context),
                controllers: Controllers = Depends(controllers_dep)):
    await controllers.state_controller.reset_distance(ctx)
    return "ok"
