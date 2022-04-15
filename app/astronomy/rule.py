import httpx
from app.astronomy.models import HST, ISS, Sattelites

HST_DATA_URL = "http://www.celestrak.com/NORAD/elements/science.txt"
ISS_DATA_URL = "http://www.celestrak.com/NORAD/elements/stations.txt"


def load_data(url) -> list[str]:
    data: list = []
    response = httpx.get(url)
    if response.status_code == httpx.codes.OK:
        data = response.text.lower().split("\r\n")
    return data


def load_sattelite_data() -> Sattelites:
    return Sattelites(
        hst=HST(load_data(HST_DATA_URL)),
        iss=ISS(load_data(ISS_DATA_URL)),
    )
