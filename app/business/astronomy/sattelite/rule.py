from functools import lru_cache

import ephem
import httpx
from app.business.astronomy.sattelite.models import HST, ISS, Sattelite, Sattelites
from requests import Response, request

HST_DATA_URL = "http://www.celestrak.com/NORAD/elements/science.txt"
ISS_DATA_URL = "http://www.celestrak.com/NORAD/elements/stations.txt"


@lru_cache(maxsize=128)
def load_data(url: str) -> list[str]:
    data: list[str] = []
    response: Response = httpx.get(url)
    if response.status_code == httpx.codes.OK:
        data = response.text.lower().split("\r\n")
    return data


class CalculateSatteliteMetrics:
    def __init__(self, tle_1: str, tle_2: str):
        ...


class SatteliteRules:
    def load_iss_data(self) -> Sattelite:
        return ISS(load_data(ISS_DATA_URL))

    def load_hubble_data(self) -> Sattelite:
        return HST(load_data(HST_DATA_URL))

    def load_all_data(self) -> Sattelites:
        return Sattelites(
            hst=HST(load_data(HST_DATA_URL)),
            iss=ISS(load_data(ISS_DATA_URL)),
        )
