import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv(override=True)
load_dotenv('serial.config', override=True)

app = Celery('solar-boat-tasks')
# print(app.config_from_object(Config))
app.config_from_envvar('CELERY_CONFIG_MODULE')
print(app.conf.beat_schedule)
