from dataclasses import dataclass


@dataclass
class TelemetrySaveStatus:
    TEMP_SAVED = 'temporary saved'
    PERM_SAVED = 'permanently saved'
    FAILED = 'fail'
