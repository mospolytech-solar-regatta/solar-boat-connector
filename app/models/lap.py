import datetime

from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey

from app.context import AppContext
from app.models.race import Race
from app.models.request_models import State
from store.postgres import Base


class Lap(Base):
    __tablename__ = "laps"

    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    distance = Column(Float)
    lap_number = Column(Integer)
    race_id = Column(Integer, ForeignKey("races.id"))

    def save(self, ctx: AppContext):
        ctx.session.add(self)

    @staticmethod
    async def create_lap(ctx: AppContext, last_lap_number=-1):
        cur_race = await Race.get_current_race(ctx)
        new_lap = Lap(race_id=cur_race.id, start_time=datetime.datetime.now(), lap_number=last_lap_number + 1)
        new_lap.save(ctx)
        cur_state = await State.get_current_state(ctx)
        cur_state.lap_id = new_lap.id
        return new_lap

    def finish(self, ctx: AppContext):
        self.end_time = datetime.datetime.now()
        # self.distance =
        self.save(ctx)

    @staticmethod
    def get_current_lap(ctx: AppContext):
        lap = ctx.session.query(Lap).order_by(Lap.start_time.desc()).first()
        return lap
