import datetime

from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey

from app.context import AppContext
from app.dependencies import get_context
from store.postgres import Base


class Lap(Base):
    __tablename__ = "laps"

    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    distance = Column(Float)
    race_id = Column(Integer, ForeignKey("races.id"))

    def save(self, ctx: AppContext):
        ctx.session.add(self)

    @staticmethod
    def create_lap(race_id, ctx: AppContext):
        new_lap = Lap(race_id=race_id, start_time=datetime.datetime.now())
        new_lap.save(ctx)
        return new_lap

    def finish(self, ctx: AppContext):
        self.end_time = datetime.datetime.now()
        # self.distance =
        self.save(ctx)

    @staticmethod
    def get_current_lap(ctx: AppContext):
        lap = ctx.session.query(Lap).order_by(Lap.start_time.desc()).first()
        return lap
