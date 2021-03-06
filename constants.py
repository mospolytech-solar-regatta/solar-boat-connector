import json
import os
from dataclasses import dataclass

CURRENT_STATE_KEY = 'current_state'
TELEMETRY_REMEMBER_DELAY = 3
HTTP_BASE = os.environ.get('ORIGIN', 'http://localhost:8000')
ALLOWED_ORIGIN = json.loads(os.environ.get('ALLOW_ORIGIN', '["*"]'))

@dataclass
class URLEndpoints:
    STATE_POST = '/current_state/'
