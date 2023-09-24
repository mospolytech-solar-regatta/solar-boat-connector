from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from app.controllers import state_controller
from app.dependencies import context_dep
from app.entities import Telemetry, State

router = APIRouter(prefix='/state', responses={404: {"description": "Not found"}})


@router.post("/")
async def post_current_state(telemetry: Telemetry, ctx: context_dep):
    res = await state_controller.save_current_state(telemetry, ctx)
    return JSONResponse({'status': 'success'})


@router.get("/", response_model=State)
async def get_current_state(ctx: context_dep):
    try:
        return await State.get_current_state(ctx)
    except FileNotFoundError:
        return JSONResponse(status_code=404, content={'message': 'key not found'})
