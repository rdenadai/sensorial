from typing import Optional

from pydantic import BaseModel


class Sattelite(BaseModel):
    name: str
    tle_1: Optional[str] = ""
    tle_2: Optional[str] = ""


class HST(Sattelite):
    def __init__(self, data: list[str]) -> None:
        super().__init__(name="Hubble Space Telescope")
        self._parse_tle_data(data)

    def _parse_tle_data(self, data: list[str]):
        self.tle_1 = str(data[1].strip())
        self.tle_2 = str(data[2].strip())


class ISS(Sattelite):
    def __init__(self, data: list[str]) -> None:
        super().__init__(name="Internation Space Station")
        self._parse_tle_data(data)

    def _parse_tle_data(self, data: list[str]):
        self.tle_1 = data[1].strip()
        self.tle_2 = data[2].strip()


class Sattelites(BaseModel):
    hst: Sattelite
    iss: Sattelite
