from datetime import datetime

from app.context import Context
from app.models.lap import Lap
from app.models.race import Race


class LapsController:
    @staticmethod
    async def create_lap(ctx: Context, race: Race, last_lap_number=-1):
        new_lap = Lap(start_time=datetime.now(), lap_number=last_lap_number + 1)
        new_lap.race = race
        new_lap.save(ctx)
        return new_lap

    def finish(self, distance, ctx: Context):
        lap = Lap.get_current_lap(ctx)
        if lap is None:
            raise ValueError("Noting to finish")
        lap.end_time = datetime.now()
        lap.distance = distance
        lap.save(ctx)

    def finish_lap(self, lap: Lap, distance, ctx: Context):
        lap.end_time = datetime.now()
        lap.distance = distance
        lap.save(ctx)
