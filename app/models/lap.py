from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.BoatAPI.context import AppContext
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
    def get_current_lap(ctx: AppContext):
        lap = ctx.session.query(Lap).order_by(Lap.start_time.desc()).first()
        return lap if lap and not lap.end_time else None
