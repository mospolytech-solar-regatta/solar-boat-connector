from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_prefix = 'redis_')

    dsn: str = 'redis://localhost/'
    telemetry_channel: str = 'telemetry'
    config_apply_channel: str = 'serial_config'
    config_channel: str = 'serial_config_apply'
    land_queue_channel: str = 'land_queue_channel'
    connector_events_channel: str = "connector_events_channel"
