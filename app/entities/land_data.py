from datetime import datetime
from enum import IntEnum
from typing import Optional

from pydantic import BaseModel

from app.context import Context
from app.entities.state import State
from app.models.land_data import LandData as LandDataModel
from app.models.state import State as StateModel


class LandData(BaseModel):
    class Priority(IntEnum):
        low = 0
        high = 1

    class Config:
        from_attributes = True

    priority: Priority
    created_at: datetime
    id: Optional[int]
    data: str

    def save(self, ctx: Context):
        land_data = LandDataModel(**self.dict())
        land_data.save(ctx)
        ctx.session.commit()
        self.id = land_data.id

    @staticmethod
    def from_state(state: StateModel):
        state_obj = State.from_orm(state)
        data = LandData(id=state.id, priority=LandData.Priority.low, data=state_obj.model_dump_json(), created_at=datetime.now())
        return data
