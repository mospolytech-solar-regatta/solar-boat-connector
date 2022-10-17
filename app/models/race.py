from sqlalchemy import Column, Integer, DateTime, String, Float
from sqlalchemy.orm import Session

from app.context import AppContext
from store.postgres import Base


class Race(Base):
    __tablename__ = "races"

    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime)
    finish_time = Column(DateTime)
    boat_name = Column(String)
    start_pos_lat = Column(Float)
    start_pos_lng = Column(Float)

    def save(self, ctx: AppContext):
        ctx.session.add(self)
