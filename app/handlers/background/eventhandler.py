import asyncio
import json

from app.context import Context
from app.controllers import StateController, LandDataController
from app.entities.land_ack import LandAck
from app.entities.telemetry import Telemetry
from app.models.serial import SerialConfig


class EventHandler:
    def __init__(self,
                 state_controller: StateController,
                 land_data_controller: LandDataController):
        self.state = state_controller
        self.land = land_data_controller

    async def handle_telemetry(self, ctx: Context, msg):
        data = json.loads(msg['data'])
        telemetry = Telemetry(**data)

        await self.state.save_current_state(telemetry, ctx)
        await asyncio.create_task(ctx.close())

    async def listen_config(self, msg):
        data = json.loads(msg['data'])
        cfg = SerialConfig(**data['config'])
        ctx = await self.get_context()
        task = asyncio.create_task(cfg.update(ctx))
        task.add_done_callback(lambda context: asyncio.create_task(ctx.close()))

    async def listen_connector_events(self, msg):
        data = json.loads(msg['data'])
        ack = LandAck(**data)
        ctx = await self.get_context()
        task = asyncio.create_task(self.land.save_sending_time(ack, ctx))
        task.add_done_callback(lambda context: asyncio.create_task(ctx.close()))
