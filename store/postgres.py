from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from store.config import PostgresConfig

Base = declarative_base()


class PostgresDB:
    def __init__(self, cfg: PostgresConfig):
        self.config = cfg
        self.factory = self._make_factory()
        self.session = self.factory()

    def __del__(self):
        self._stop_connection()

    def _stop_connection(self):
        self.session.close()

    def get_session(self):
        return self.session

    def get_factory(self):
        return self.factory

    def _make_factory(self) -> sessionmaker:
        pg_dsn = self._get_dsn()
        engine = create_engine(pg_dsn)
        session_factory = sessionmaker(engine)
        return session_factory

    def _get_dsn(self) -> str:
        return f'postgresql://{self.config.user}:{self.config.password}@' \
               f'{self.config.server}:{self.config.port}/{self.config.db}'
