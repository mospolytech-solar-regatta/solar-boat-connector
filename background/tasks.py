import json
from dataclasses import dataclass

import serial
from celery import Task
from pydantic import BaseModel

import app_config
from background.app import app
from background import helpers
from models.request_models import Telemetry


class SerialConfig(BaseModel):
    name: str
    rate: int


class SerialTask(Task):
    _port = None
    _portConfig = SerialConfig(name=app_config.serial_port, rate=app_config.serial_rate)

    @property
    def port(self):
        if self._port is None:
            self._port = serial.Serial(self._portConfig.name, self._portConfig.rate, timeout=0,
                                       parity=serial.PARITY_EVEN, rtscts=1)
        if not self._port.isOpen():
            self._port.open()
        return self._port


@app.task(bind=True, base=SerialTask)
def read_data(self):
    res = self.port.readlines()
    if len(res) < 1:
        return
    res = res[-1].decode('utf-8').strip()
    telemetry = Telemetry(**json.loads(res))
    print(telemetry.json())
    helpers.post(telemetry.json())


@app.task(bind=True, base=SerialTask)
def get_config(self):
    return self._portConfig.json()
