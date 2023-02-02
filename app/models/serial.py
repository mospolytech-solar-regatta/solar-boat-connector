import json
from typing import Optional

from pydantic import BaseModel

from app.BoatAPI.context import AppContext

serial_config_key = "serial_config"


class SerialConfig(BaseModel):
    port: str
    baudrate: Optional[int] = 115200
    bytesize: Optional[int] = 8
    parity: Optional[str] = 'N'
    stopbits: Optional[int] = 1
    timeout: Optional[int] = 0

    async def apply(self, ctx: AppContext):
        await ctx.redis.publish(ctx.redis.config.redis_config_channel, self.json())

    async def update(self, ctx: AppContext):
        await ctx.redis.set(serial_config_key, self.json())

    @staticmethod
    async def get(ctx: AppContext) -> "SerialConfig":
        res = await ctx.redis.get(serial_config_key)
        return SerialConfig(**json.loads(res))
