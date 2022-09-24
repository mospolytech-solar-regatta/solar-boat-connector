from typing import Optional

from pydantic import BaseModel
from redis.client import Redis

serial_config_key = "serial_config"


class SerialConfig(BaseModel):
    port: str
    baudrate: Optional[int] = 115200
    bytesize: Optional[int] = 8
    parity: Optional[str] = 'N'
    stopbits: Optional[int] = 1
    timeout: Optional[int] = 0


async def get_serial_config(redis: Redis):
    return await redis.get(serial_config_key)
