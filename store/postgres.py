from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import config

engine = create_engine(config.postgres_dsn, echo=True)
session_factory = sessionmaker(engine)
Base = declarative_base()


def get_db():
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
