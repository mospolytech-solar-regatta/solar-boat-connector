from app.controllers import laps, race, state, land_data


class Controllers:

    def __init__(self):
        self.laps_controller = laps.LapsController()
        self.race_controller = race.RaceController(self.laps_controller)
        self.state_controller = state.StateController(self.laps_controller)
        self.land_data_controller = land_data.LandDataController()
