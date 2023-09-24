from fastapi import APIRouter

from app.controllers import state_controller
from app.dependencies import context_dep
from app.entities import PointSet

router = APIRouter(prefix='/action')


@router.get('/lap_point/', response_model=PointSet)
async def set_lap_point(ctx: context_dep):
    return await state_controller.set_point(ctx)


@router.get('/reset_point/', response_model=str)
async def reset(ctx: context_dep):
    await state_controller.reset_point(ctx)
    return "ok"


@router.get('/reset_distance/', response_model=str)
async def reset(ctx: context_dep):
    await state_controller.reset_distance(ctx)
    return "ok"
