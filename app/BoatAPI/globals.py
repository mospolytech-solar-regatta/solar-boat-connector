boat_api_app = None
listener = None
controllers = None


def set_app(app):
    global boat_api_app
    boat_api_app = app


def get_app():
    return boat_api_app


def set_controllers(c):
    global controllers
    controllers = c


def get_controllers():
    return controllers
