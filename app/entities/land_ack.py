from datetime import datetime

from pydantic import BaseModel


class LandAck(BaseModel):
   id: int
   timestamp: datetime