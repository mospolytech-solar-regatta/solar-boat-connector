from app.client import redis_events
from app.dependencies import context_factory
from .event_wrapper import EventWrapper

event_wrapper = EventWrapper(redis_events, context_factory)
