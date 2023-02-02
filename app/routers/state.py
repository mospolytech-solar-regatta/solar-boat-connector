from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from app.BoatAPI.context import AppContext
from app.controllers import Controllers
from app.dependencies import get_context, controllers_dep
from app.entities import Telemetry, State

router = APIRouter(prefix='/state', responses={404: {"description": "Not found"}})


@router.post("/")
async def post_current_state(telemetry: Telemetry, ctx: AppContext = Depends(get_context),
                             controllers: Controllers = Depends(controllers_dep)):
    res = await controllers.state_controller.save_current_state(telemetry, ctx)
    return JSONResponse({'status': 'success'})


@router.get("/", response_model=State)
async def get_current_state(ctx: AppContext = Depends(get_context)):
    try:
        return await State.get_current_state(ctx)
    except FileNotFoundError:
        return JSONResponse(status_code=404, content={'message': 'key not found'})
