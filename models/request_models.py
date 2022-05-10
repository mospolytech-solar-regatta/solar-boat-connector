import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from aioredis import Redis
from pydantic import BaseModel
from sqlalchemy.orm import Session

import constants
from models.telemetry import Telemetry as pgTelemetry
# pylint: disable=redefined-builtin
from store.redis import get, set


@dataclass
class TelemetrySaveStatus:
    TEMP_SAVED = 'temporary saved'
    PERM_SAVED = 'permanently saved'
    FAILED = 'fail'


class Telemetry(BaseModel):
    created_at: datetime
    controller_watts: int
    time_to_go: int
    controller_volts: float
    MPPT_volts: float
    MPPT_watts: float
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
            return TelemetrySaveStatus.PERM_SAVED

        cur = Telemetry(**json.loads(cur))
        if cur.created_at < self.created_at:
            await set(db, constants.CURRENT_STATE_KEY, self.json())
        if self.created_at - cur.created_at > timedelta(seconds=constants.TELEMETRY_REMEMBER_DELAY):
            pgTelemetry.save_from_schema(self, session)
            return TelemetrySaveStatus.PERM_SAVED
        return TelemetrySaveStatus.FAILED

    @staticmethod
    async def get_current_state(db: Redis):
        cur = await get(db, constants.CURRENT_STATE_KEY)
        if cur is None:
            raise FileNotFoundError("Key not found")
        return Telemetry(**json.loads(cur))
