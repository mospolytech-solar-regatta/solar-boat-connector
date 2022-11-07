import json
from dataclasses import dataclass
from datetime import datetime, timedelta
import geopy.distance
from pydantic import BaseModel

from app import constants
from app.context import AppContext
from app.models.lap import Lap
from app.models.telemetry import Telemetry as pgTelemetry


@dataclass
class TelemetrySaveStatus:
    TEMP_SAVED = 'temporary saved'
    PERM_SAVED = 'permanently saved'
    FAILED = 'fail'


class Telemetry(BaseModel):
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

    async def save_current_state(self, ctx: AppContext):
        state = await State.from_telemetry(self, ctx)
        await state.save(ctx)


class PointSet(BaseModel):
    lng: float
    lat: float


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
        return pgTelemetry.get_last(ctx)

    async def update_from_previous(self, prev, ctx: AppContext):
        cur_coord = (self.position_lat, self.position_lng)
        prev_coord = (prev.position_lat, prev.position_lng)
        delta = (self.created_at - prev.created_at).seconds / 3600
        distance = geopy.distance.geodesic(cur_coord, prev_coord).km

        self.speed = distance / max(delta, 1)
        self.distance_travelled = prev.distance_travelled + distance
        self.laps = prev.laps
        self.lap_point_lat = prev.lap_point_lat
        self.lap_point_lng = prev.lap_point_lng
        self.lap_id = prev.lap_id
        if self.lap_point_lng is not None and self.lap_point_lat is not None:
            await self.count_laps(prev, ctx)

    async def count_laps(self, prev, ctx: AppContext):
        lap_coord = (self.lap_point_lat, self.lap_point_lng)
        prev_coord = (prev.position_lat, prev.position_lng)
        cur_coord = (self.position_lat, self.position_lng)
        prev_dist = geopy.distance.geodesic(prev_coord, lap_coord).m
        cur_dist = geopy.distance.geodesic(cur_coord, lap_coord).m
        if prev_dist > constants.LAP_ADD_RADIUS_METERS >= cur_dist:
            self.laps += 1
            prev_lap = Lap.get_current_lap(ctx)
            prev_lap.finish(self.distance_travelled, ctx)
            new_lap = await Lap.create_lap(ctx, prev_lap.race_id, prev_lap.lap_number)
            self.lap_id = new_lap.id

    @staticmethod
    async def from_telemetry(telemetry: Telemetry, ctx: AppContext):
        res = State(**telemetry.dict())

        try:
            prev = await State.get_current_state(ctx)
        except FileNotFoundError:
            return res
        await res.update_from_previous(prev, ctx)
        return res

    async def _save_redis(self, ctx: AppContext):
        await ctx.redis.set(constants.CURRENT_STATE_KEY, self.json())

    def _save_pg(self, ctx: AppContext):
        pgTelemetry.save_from_schema(self, ctx)

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
            return TelemetrySaveStatus.PERM_SAVED
        else:
            return TelemetrySaveStatus.TEMP_SAVED

    @staticmethod
    async def set_point(ctx: AppContext) -> PointSet:
        prev = await State.get_current_state(ctx)
        prev.lap_point_lng = prev.position_lng
        prev.lap_point_lat = prev.position_lat
        prev.laps = 0
        await prev._save_redis(ctx)
        return PointSet(lng=prev.lap_point_lng, lat=prev.lap_point_lat)

    @staticmethod
    async def reset_point(ctx: AppContext) -> None:
        prev = await State.get_current_state(ctx)
        prev.lap_point_lng = None
        prev.lap_point_lat = None
        prev.laps = 0
        await prev._save_redis(ctx)

    @staticmethod
    async def reset_distance(ctx: AppContext) -> None:
        prev = await State.get_current_state(ctx)
        prev.distance_travelled = 0
        await prev._save_redis(ctx)

    @staticmethod
    async def remove_point(ctx: AppContext):
        prev = await State.get_current_state(ctx)
        prev.lap_point_lng = None
        prev.lap_point_lat = None
        prev.laps = 0
        await prev._save_redis(ctx)
        return PointSet(lng=prev.lap_point_lng, lat=prev.lap_point_lat)

    @staticmethod
    async def clear_distance(ctx: AppContext):
        prev = await State.get_current_state(ctx)
        prev.distance_travelled = 0
        await prev._save_redis(ctx)
