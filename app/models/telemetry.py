from sqlalchemy import Column
from sqlalchemy.orm import Session
from sqlalchemy.types import DateTime, Integer, Float

from store.postgres import Base


class Telemetry(Base):
    __tablename__ = 'telemetry'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    controller_watts = Column(Integer)
    time_to_go = Column(Integer)
    controller_volts = Column(Float)
    MPPT_volts = Column(Float)
    MPPT_watts = Column(Float)
    motor_temp = Column(Float)
    motor_revols = Column(Float)
    speed = Column(Float)
    position_lat = Column(Float)
    position_lng = Column(Float)
    distance_travelled = Column(Float)
    laps = Column(Integer)
    lap_point_lat = Column(Float)
    lap_point_lng = Column(Float)

    def save(self, session: Session):
        session.add(self)
        session.commit()

    @staticmethod
    def save_from_schema(schema, session: Session):
        telemetry = Telemetry(**schema.dict())
        telemetry.save(session)

    @staticmethod
    def get_last(session: Session):
        res = session.query(Telemetry).order_by(Telemetry.id.desc()).first()
        return res
