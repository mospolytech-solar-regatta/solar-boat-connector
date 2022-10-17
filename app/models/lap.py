from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey

from app.context import AppContext
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
