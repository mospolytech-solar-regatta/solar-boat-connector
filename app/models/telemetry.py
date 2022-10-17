from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import Session
from sqlalchemy.types import DateTime, Integer, Float

from app.context import AppContext
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
    lap_id = Column(Integer, ForeignKey("laps.id"))

    def save(self, ctx: AppContext):
        ctx.session.add(self)

    @staticmethod
    def save_from_schema(schema, ctx: AppContext):
        telemetry = Telemetry(**schema.dict())
        telemetry.save(ctx)

    @staticmethod
    def get_last(ctx: AppContext):
        res = ctx.session.query(Telemetry).order_by(Telemetry.id.desc()).first()
        return res
