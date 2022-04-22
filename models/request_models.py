import json
from datetime import datetime, timedelta
from typing import Optional

from pydantic.datetime_parse import parse_datetime
from sqlalchemy.orm import Session

from models.telemetry import Telemetry as pgTelemetry
from pydantic import BaseModel

import constants
from store.redis import *


class Telemetry(BaseModel):
    created_at: datetime
    controller_watts: int
    time_to_go: int
    controller_volts: float
    MPPT_volts: float
    MPPT_watt: float
    motor_temp: float
    motor_revols: float
    speed: Optional[float]
    position_lat: float
    position_lng: float
    distance_travelled: Optional[float]
    laps: Optional[int]
    lap_point_lat: Optional[float]
    lap_point_lng: Optional[float]

    class Config:
        orm_mode = True

    async def save_current_state(self, db: Redis, session: Session):
        cur = await get(db, constants.CURRENT_STATE_KEY)
        if cur is None:
            await set(db, constants.CURRENT_STATE_KEY, self.json())
            return 'OK'

        cur = Telemetry(**json.loads(cur))
        if cur.created_at < self.created_at:
            await set(db, constants.CURRENT_STATE_KEY, self.json())
        if self.created_at - cur.created_at > timedelta(seconds=constants.TELEMETRY_REMEMBER_DELAY):
            pgTelemetry.save_from_schema(self, session)
            return 'OK'
        return 'not latest value'

    @staticmethod
    async def get_current_state(db: Redis):
        cur = await get(db, constants.CURRENT_STATE_KEY)
        if cur is None:
            raise FileNotFoundError("Key not found")
        return Telemetry(**json.loads(cur))
