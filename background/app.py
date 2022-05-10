from celery import Celery
from dotenv import load_dotenv

load_dotenv(override=True)
load_dotenv('serial.config', override=True)

app = Celery('solar-boat-tasks')
app.config_from_envvar('CELERY_CONFIG_MODULE')
