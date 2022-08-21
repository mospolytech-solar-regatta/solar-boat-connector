from app.config.app_config import BaseConfig

app_config = BaseConfig()


def set_config(cfg):
    global app_config
    app_config = cfg


def get_config():
    return app_config
