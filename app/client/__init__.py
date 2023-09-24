from .postgres import PostgresDB, PostgresConfig
from .redis import RedisDB, RedisConfig
from .redis_events import RedisEventsClient

redis_cfg = RedisConfig()
postgres_cfg = PostgresConfig()

redis = RedisDB(redis_cfg)
postgres = PostgresDB(postgres_cfg)

redis_events = RedisEventsClient(redis)
