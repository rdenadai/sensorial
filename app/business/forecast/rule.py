from datetime import datetime

from app.business.forecast.models import (
    AutumnalEquinox,
    SeasonEvents,
    SummerSolstice,
    VernalEquinox,
    WinterSolstice,
)


class SeasonsEventBuilder:
    def __init__(self, dtime: datetime = datetime.utcnow()):
        self.dtime = dtime

    def build(self):
        return SeasonEvents(
            vernal_equinox=VernalEquinox(self.dtime),
            autumnal_equinox=AutumnalEquinox(self.dtime),
            summer_solstice=SummerSolstice(self.dtime),
            winter_solstice=WinterSolstice(self.dtime),
        )
