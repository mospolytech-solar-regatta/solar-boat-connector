from app.controllers import laps, race, state


class Controllers:

    def __init__(self):
        self.laps_controller = laps.LapsController()
        self.race_controller = race.RaceController(self.laps_controller)
        self.state_controller = state.StateController(self.laps_controller)
