from calendar import timegm
from datetime import datetime

from ephem import (
    next_autumnal_equinox,
    next_summer_solstice,
    next_vernal_equinox,
    next_winter_solstice,
)
from pydantic import BaseModel


class Season(BaseModel):
    next_event: int


class VernalEquinox(Season):
    def __init__(self, dtime: datetime = datetime.utcnow()) -> None:
        super().__init__(next_event=timegm(next_vernal_equinox(dtime).datetime().timetuple()))


class AutumnalEquinox(Season):
    def __init__(self, dtime: datetime = datetime.utcnow()) -> None:
        super().__init__(next_event=timegm(next_autumnal_equinox(dtime).datetime().timetuple()))


class SummerSolstice(Season):
    def __init__(self, dtime: datetime = datetime.utcnow()) -> None:
        super().__init__(next_event=timegm(next_summer_solstice(dtime).datetime().timetuple()))


class WinterSolstice(Season):
    def __init__(self, dtime: datetime = datetime.utcnow()) -> None:
        super().__init__(next_event=timegm(next_winter_solstice(dtime).datetime().timetuple()))


class SeasonEvents(BaseModel):
    vernal_equinox: Season
    autumnal_equinox: Season
    summer_solstice: Season
    winter_solstice: Season
