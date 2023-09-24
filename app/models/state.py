from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import DateTime, Integer, Float

from app.context import Context
from .base import Base


class State(Base):
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

    def save(self, ctx: Context):
        ctx.session.add(self)

    @staticmethod
    def save_from_schema(schema, ctx: Context):
        telemetry = State(**schema.dict())
        telemetry.save(ctx)

    @staticmethod
    def get_last(ctx: Context):
        res = ctx.session.query(State).order_by(State.id.desc()).first()
        return res
