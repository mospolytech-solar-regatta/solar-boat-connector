from app.config.app_config import BaseConfig, AppConfig
from background.listener import Listener

app_config = BaseConfig()
listener = None


def set_config(cfg):
    global app_config
    app_config = cfg


def get_config():
    return app_config


def create_listener(config: AppConfig):
    global listener
    listener = Listener(config)
    return listener


def get_listener():
    global listener
    return listener
