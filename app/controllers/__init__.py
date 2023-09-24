from .laps import LapsController
from .race import RaceController
from .state import StateController
from .land import LandDataController

laps_controller = LapsController()
race_controller = RaceController(laps_controller)
state_controller = StateController(laps_controller)
land_data_controller = LandDataController()
