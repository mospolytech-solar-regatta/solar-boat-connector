import app.utils.coordinates as coord_utils
from app import constants
from app.context import Context
from app.controllers.laps import LapsController
from app.entities.land_data import LandData
from app.entities.state import State, PointSet
from app.entities.status import TelemetrySaveStatus
from app.entities.telemetry import Telemetry
from app.models import Race
from app.models.lap import Lap
from app.models.state import State as StateModel


class StateController:
    def __init__(self, laps_controller: LapsController):
        self.laps = laps_controller

    async def save_current_state(self, telemetry: Telemetry, ctx: Context):
        state = await self.from_telemetry(telemetry, ctx)
        status = await state.save(ctx)
        if status == TelemetrySaveStatus.PERM_SAVED:
            state = StateModel.get_last(ctx)
            land_data = LandData.from_state(state)
            land_data.save(ctx)
            await ctx.redis.publish(ctx.redis.config.land_queue_channel, land_data.json())

    async def count_laps(self, current: State, previous: State, ctx: Context):
        prev_dist = coord_utils.count_distance(previous.position_lat, previous.position_lng,
                                               current.lap_point_lat, current.lap_point_lng).m
        cur_dist = coord_utils.count_distance(current.position_lat, current.position_lng,
                                              current.lap_point_lat, current.lap_point_lng).m
        if prev_dist > constants.LAP_ADD_RADIUS_METERS >= cur_dist:
            current.laps += 1
            prev_lap = Lap.get_current_lap(ctx)
            if prev_lap:
                self.laps.finish_lap(prev_lap, current.distance_travelled, ctx)
                await self.laps.create_lap(ctx, prev_lap.race, prev_lap.lap_number)
            else:
                race = await Race.get_current_race(ctx)
                await self.laps.create_lap(ctx, race, previous.laps)
            ctx.session.commit()

    async def from_telemetry(self, telemetry: Telemetry, ctx: Context):
        res = State(**telemetry.dict())

        try:
            prev = await State.get_current_state(ctx)
        except FileNotFoundError:
            return res

        await self._update_from_previous_state(res, prev, ctx)
        return res

    async def _update_from_previous_state(self, current: State, previous: State, ctx: Context):
        distance = coord_utils.count_distance(previous.position_lat, previous.position_lng,
                                              current.position_lat, current.position_lng)

        current.speed = coord_utils.count_speed(current.created_at, previous.created_at, distance)
        current.distance_travelled = previous.distance_travelled + distance.km
        current.laps = previous.laps
        current.lap_point_lat = previous.lap_point_lat
        current.lap_point_lng = previous.lap_point_lng

        race = await Race.get_current_race(ctx)
        if current.lap_point_lng is not None and current.lap_point_lat is not None and race is not None:
            await self.count_laps(current, previous, ctx)
        current_lap = Lap.get_current_lap(ctx)
        if current_lap:
            current.lap_id = current_lap.id

    @staticmethod
    async def set_point(ctx: Context) -> PointSet:
        prev = await State.get_current_state(ctx)
        prev.lap_point_lng = prev.position_lng
        prev.lap_point_lat = prev.position_lat
        prev.laps = 0
        await prev._save_redis(ctx)
        return PointSet(lng=prev.lap_point_lng, lat=prev.lap_point_lat)

    @staticmethod
    async def reset_point(ctx: Context) -> None:
        prev = await State.get_current_state(ctx)
        prev.lap_point_lng = None
        prev.lap_point_lat = None
        prev.laps = 0
        await prev._save_redis(ctx)

    @staticmethod
    async def reset_distance(ctx: Context) -> None:
        prev = await State.get_current_state(ctx)
        prev.distance_travelled = 0
        await prev._save_redis(ctx)

    @staticmethod
    async def remove_point(ctx: Context):
        prev = await State.get_current_state(ctx)
        prev.lap_point_lng = None
        prev.lap_point_lat = None
        prev.laps = 0
        await prev._save_redis(ctx)
        return PointSet(lng=prev.lap_point_lng, lat=prev.lap_point_lat)

    @staticmethod
    async def clear_distance(ctx: Context):
        prev = await State.get_current_state(ctx)
        prev.distance_travelled = 0
        await prev._save_redis(ctx)
