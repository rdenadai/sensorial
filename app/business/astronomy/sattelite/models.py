from typing import List, Optional

from pydantic import BaseModel, Field


class NextSattelitePasses(BaseModel):
    rise_time: int
    rise_azimuth: float
    rise_altitude: float
    rise_elevation: int
    rise_sun_altitude: float
    max_time: int
    max_azimuth: float
    max_altitude: float
    max_elevation: int
    max_sun_altitude: float
    duration: int


class Sattelite(BaseModel):
    name: str
    tle_1: Optional[str] = ""
    tle_2: Optional[str] = ""
    latitude: Optional[float] = 0.0
    longitude: Optional[float] = 0.0
    elevation: Optional[int] = 0
    next_passes: Optional[List[NextSattelitePasses]] = Field(default_factory=list)

    def _parse_tle_data(self, data: list[str]) -> None:
        if data:
            self.tle_1 = str(data[1].strip())
            self.tle_2 = str(data[2].strip())


class HST(Sattelite):
    def __init__(self, data: list[str]) -> None:
        super().__init__(name="Hubble Space Telescope")
        self._parse_tle_data(data)


class ISS(Sattelite):
    def __init__(self, data: list[str]) -> None:
        super().__init__(name="Internation Space Station")
        self._parse_tle_data(data)


class Sattelites(BaseModel):
    hst: Sattelite
    iss: Sattelite
