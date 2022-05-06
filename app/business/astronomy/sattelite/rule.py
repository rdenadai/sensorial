from functools import lru_cache

import httpx
from ephem import readtle
from requests import Response

from app.business.astronomy.sattelite.models import HST, ISS, Sattelite, Sattelites
from app.business.geo import dms2dec

HST_DATA_URL = "http://www.celestrak.com/NORAD/elements/science.txt"
ISS_DATA_URL = "http://www.celestrak.com/NORAD/elements/stations.txt"


@lru_cache(maxsize=128)
def load_data(url: str) -> list[str]:
    data: list[str] = []
    response: Response = httpx.get(url)
    if response.status_code == httpx.codes.OK:
        data = response.text.lower().split("\r\n")
    return data


class SatteliteBuilder:
    def build(self, sattelite_type: Sattelite):
        url = HST_DATA_URL
        if isinstance(sattelite_type, ISS):
            url = ISS_DATA_URL
        return sattelite_type(load_data(url))


class SatteliteRules:
    def __init__(self, latitude: float, longitude: float, altitude: float):
        self.sattelite: Sattelite = None
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    def calculate(self, sattelite_type: Sattelite):
        self.sattelite = SatteliteBuilder().build(sattelite_type)
        to_compute = readtle(self.sattelite.name, self.sattelite.tle_1, self.sattelite.tle_2)
        to_compute.compute()
        self.sattelite.latitude = dms2dec(str(to_compute.sublat))
        self.sattelite.longitude = dms2dec(str(to_compute.sublong))
        self.sattelite.elevation = to_compute.elevation
        # COMPUTE NEXT 5 VISIBLE PASSES
        # self.sattelite.next_passes = get_next_visible_passes(self.latitude , self.longitude, self.altitude, hst_data)
        return self.sattelite


class SattelitesRules(SatteliteRules):
    def calculate_all(self):
        return Sattelites(
            hst=self.calculate(HST),
            iss=self.calculate(ISS),
        )
