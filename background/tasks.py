import json

import serial
from celery import Task

import config
from background.app import app
from background import helpers
from models.request_models import Telemetry


class SerialTask(Task):
    _port = None
    _portName = config.serial_port
    _portRate = config.serial_rate

    @property
    def port(self):
        if self._port is None:
            self._port = serial.Serial(self._portName, self._portRate, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)
        if not self._port.isOpen():
            self._port.open()
        return self._port


@app.task(bind=True, base=SerialTask)
def read_data(self):
    res = self.port.readline().decode('utf-8').strip()
    if res == '':
        return
    telemetry = Telemetry(**json.loads(res))
    helpers.post(telemetry.json())
    return telemetry
