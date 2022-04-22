import os

redis_dsn = os.environ.get('REDIS_DSN', '')
postgres_dsn = f'postgresql://{os.environ.get("POSTGRES_USER")}:{os.environ.get("POSTGRES_PASSWORD")}@' \
               f'{os.environ.get("POSTGRES_SERVER")}:{os.environ.get("POSTGRES_PORT")}/{os.environ.get("POSTGRES_DB")}'
serial_port = os.environ.get('SERIAL_PORT')
serial_rate = os.environ.get('SERIAL_RATE')
