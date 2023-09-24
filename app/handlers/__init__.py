from app.controllers import state_controller, land_data_controller
from .background import EventHandler

events_handler = EventHandler(state_controller, land_data_controller)
