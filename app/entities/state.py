import json
from datetime import datetime, timedelta

from pydantic import BaseModel

from app import constants
from app.BoatAPI.context import AppContext
from app.entities.status import TelemetrySaveStatus
from app.models.state import State as StateModel


class State(BaseModel):
    created_at: datetime
    controller_watts: int
    time_to_go: int
    controller_volts: float
    MPPT_volts: float
    MPPT_watts: float
    motor_temp: float
    motor_revols: float
    position_lat: float
    position_lng: float
    speed: float = 0
    distance_travelled: float = 0
    laps: int = 0
    lap_point_lat: float = None
    lap_point_lng: float = None
    lap_id: int = None

    class Config:
        orm_mode = True

    @staticmethod
    async def get_current_state(ctx: AppContext):
        cur = await ctx.redis.get(constants.CURRENT_STATE_KEY)
        if cur is None:
            raise FileNotFoundError("Key not found")
        return State(**json.loads(cur))

    @staticmethod
    def get_pg_state(ctx: AppContext):
        return StateModel.get_last(ctx)

    async def _save_redis(self, ctx: AppContext):
        await ctx.redis.set(constants.CURRENT_STATE_KEY, self.json())

    def _save_pg(self, ctx: AppContext):
        StateModel.save_from_schema(self, ctx)

    async def save(self, ctx: AppContext):
        try:
            prev = await State.get_current_state(ctx)
        except FileNotFoundError:
            await self._save_redis(ctx)
            self._save_pg(ctx)
            return TelemetrySaveStatus.PERM_SAVED

        if prev.created_at < self.created_at:
            await self._save_redis(ctx)
        prev = State.get_pg_state(ctx)
        if prev is None or self.created_at - prev.created_at > timedelta(seconds=constants.TELEMETRY_REMEMBER_DELAY):
            self._save_pg(ctx)
            ctx.session.commit()
            return TelemetrySaveStatus.PERM_SAVED
        else:
            return TelemetrySaveStatus.TEMP_SAVED


class PointSet(BaseModel):
    lng: float
    lat: float
