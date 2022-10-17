from fastapi import APIRouter, Depends

from app.context import AppContext
from app.dependencies import get_context
from app.models.request_models import PointSet, State

router = APIRouter(prefix='/action')


@router.get('/lap_point/', response_model=PointSet)
async def set_lap_point(ctx: AppContext = Depends(get_context)):
    return await State.set_point(ctx)


@router.get('/reset_point/', response_model=str)
async def reset(ctx: AppContext = Depends(get_context)):
    await State.reset_point(ctx)
    return "ok"


@router.get('/reset_distance/', response_model=str)
async def reset(ctx: AppContext = Depends(get_context)):
    await State.reset_distance(ctx)
    return "ok"
