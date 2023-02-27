from datetime import datetime
from enum import IntEnum

from sqlalchemy import Column, Integer, DateTime, String

from app.BoatAPI.context import AppContext
from app.entities.state import State
from app.models.state import State as StateModel
from store.postgres import Base


class LandData(Base):
    __tablename__ = "land_data"
    id = Column(Integer, primary_key=True)
    priority = Column(Integer)
    created_at = Column(DateTime)
    sent_at = Column(DateTime)
    data = Column(String)

    class Priority(IntEnum):
        low = 0
        high = 1

    def save(self, ctx: AppContext):
        ctx.session.add(self)

    @staticmethod
    def from_telemetry(state: StateModel, ctx: AppContext):
        state = State.from_orm(state)
        data = LandData(priority=LandData.Priority.low, data=state.json(), created_at=datetime.now())
        data.save(ctx)
        return data
