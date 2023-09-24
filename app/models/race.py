from sqlalchemy import Column, Integer, DateTime, String, Float
from sqlalchemy.orm import relationship

from app.context import Context
from .base import Base


class Race(Base):
    __tablename__ = "races"

    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime)
    finish_time = Column(DateTime)
    boat_name = Column(String)
    start_pos_lat = Column(Float)
    start_pos_lng = Column(Float)
    laps = relationship("Lap", back_populates="race")

    def save(self, ctx: Context):
        ctx.session.add(self)

    @staticmethod
    async def get_current_race(ctx: Context):
        race = ctx.session.query(Race).order_by(Race.start_time.desc()).first()
        return race if race and not race.finish_time else None
