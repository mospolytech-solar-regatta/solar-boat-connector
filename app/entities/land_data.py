from datetime import datetime
from enum import IntEnum
from typing import Optional

from pydantic import BaseModel

from app.entities.state import State
from app.models.state import State as StateModel


class LandData(BaseModel):
    class Priority(IntEnum):
        low = 0
        high = 1

    class Config:
        orm_mode = True

    priority: Priority
    created_at: datetime
    sent_at: Optional[datetime]
    id: int
    data: str

    @staticmethod
    def from_telemetry(state: StateModel):
        state = State.from_orm(state)
        data = LandData(priority=LandData.Priority.low, data=state.json(), created_at=datetime.now())
        return data
