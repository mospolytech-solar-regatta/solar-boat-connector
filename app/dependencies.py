from app import context
from app.config.app_config import BaseConfig


def get_config():
    if type(context.get_config()) == BaseConfig.__class__:
        raise NotImplementedError("app not configured")
    return context.get_config()
