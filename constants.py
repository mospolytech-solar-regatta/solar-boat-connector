from dataclasses import dataclass

CURRENT_STATE_KEY = 'current_state'
TELEMETRY_REMEMBER_DELAY = 3
HTTP_BASE = 'http://localhost:8000'


@dataclass
class URLEndpoints:
    STATE_POST = '/current_state/'
