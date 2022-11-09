import datetime

from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.context import AppContext
from store.postgres import Base


class Lap(Base):
    __tablename__ = "laps"

    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    distance = Column(Float)
    lap_number = Column(Integer)
    race_id = Column(Integer, ForeignKey("races.id"))
    race = relationship("Race", back_populates="laps")

    def save(self, ctx: AppContext):
        ctx.session.add(self)

    @staticmethod
    async def create_lap(ctx: AppContext, race, last_lap_number=-1):
        new_lap = Lap(start_time=datetime.datetime.now(), lap_number=last_lap_number + 1)
        new_lap.race = race
        new_lap.save(ctx)
        return new_lap

    def finish(self, distance, ctx: AppContext):
        self.end_time = datetime.datetime.now()
        self.distance = distance
        self.save(ctx)

    @staticmethod
    def get_current_lap(ctx: AppContext):
        lap = ctx.session.query(Lap).order_by(Lap.start_time.desc()).first() #.where(Lap.end_time is not None)
        return lap if lap and not lap.end_time else None
