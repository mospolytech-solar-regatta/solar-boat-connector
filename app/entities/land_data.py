from datetime import datetime
from enum import IntEnum
from typing import Optional

from pydantic import BaseModel

from app.BoatAPI.context import AppContext
from app.entities.state import State
from app.models.state import State as StateModel
from app.models.land_data import LandData as LandDataModel


class LandData(BaseModel):
    class Priority(IntEnum):
        low = 0
        high = 1

    class Config:
        orm_mode = True

    priority: Priority
    created_at: datetime
    id: Optional[int]
    data: str

    def save(self, ctx: AppContext):
        land_data = LandDataModel(**self.dict())
        land_data.save(ctx)
        ctx.session.commit()
        self.id = land_data.id

    @staticmethod
    def from_state(state: StateModel):
        state = State.from_orm(state)
        data = LandData(priority=LandData.Priority.low, data=state.json(), created_at=datetime.now())
        return data
