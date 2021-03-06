import json

import serial
from celery import Task
from pydantic import BaseModel

import app_config
from background import helpers
from background.app import app
from models.request_models import Telemetry


class SerialConfig(BaseModel):
    name: str
    rate: int


class SerialTask(Task):
    _port = None
    _portConfig = SerialConfig(name=app_config.serial_port, rate=app_config.serial_rate)

    @staticmethod
    def build_serial():
        return serial.Serial(SerialTask._portConfig.name, SerialTask._portConfig.rate,
                             timeout=0, parity=serial.PARITY_EVEN, rtscts=1)

    @property
    def port(self):
        if SerialTask._port is None:
            SerialTask._port = self.build_serial()
        if not SerialTask._port.isOpen():
            SerialTask._port.open()
        return SerialTask._port

    def set_config(self, config: SerialConfig):
        SerialTask._portConfig = config

    def get_config(self):
        return SerialTask._portConfig

    def reopen_port(self):
        if SerialTask._port is not None:
            SerialTask._port.close()
        SerialTask._port = None

    def read_lines(self):
        if SerialTask._port is None:
            SerialTask._port = self.build_serial()
        if not SerialTask._port.isOpen():
            SerialTask._port.open()
        return SerialTask._port.readlines()

    def send(self, data: str):
        if SerialTask._port is None:
            SerialTask._port = self.build_serial()
        if not SerialTask._port.isOpen():
            SerialTask._port.open()
        SerialTask._port.write(data.encode('utf-8'))


@app.task(bind=True, base=SerialTask)
def read_data(self):
    res = self.read_lines()
    if len(res) < 1:
        return
    res = res[-1].decode('utf-8').strip()
    telemetry = Telemetry(**json.loads(res))
    helpers.post(telemetry.json())


@app.task(bind=True, base=SerialTask)
def get_config(self):
    return self.get_config().json()


@app.task(bind=True, base=SerialTask)
def set_config(self, config: dict):
    config = SerialConfig(**config)
    self.set_config(config)
    self.reopen_port()
    return self.get_config().json()


@app.task(bind=True, base=SerialTask)
def send(self, data: str):
    self.send(data)
