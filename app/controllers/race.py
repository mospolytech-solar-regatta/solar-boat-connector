from datetime import datetime

from app.BoatAPI.context import AppContext
from app.controllers.laps import LapsController
from app.models.race import Race
from app.entities.state import State


class RaceController:
    def __init__(self, laps_controller: LapsController):
        self.laps = laps_controller

    async def start_new_race(self, ctx: AppContext):
        cur_state = await State.get_current_state(ctx)
        new_race = Race(
            start_time=datetime.now(),
            start_pos_lat=cur_state.position_lat,
            start_pos_lng=cur_state.position_lng)
        new_race.save(ctx)
        await self.laps.create_lap(ctx, new_race)
        return new_race

    async def stop(self, ctx: AppContext):
        race = await Race.get_current_race(ctx)
        if race is None:
            raise ValueError("no race to stop")
        race.finish_time = datetime.now()
        race.save(ctx)
        cur_state = await State.get_current_state(ctx)
        self.laps.finish(cur_state.distance_travelled, ctx)
