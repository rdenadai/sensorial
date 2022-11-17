from functools import lru_cache

from httpx import Response, codes, get

from app.business.earthquake.models import Earthquake, EarthquakeEvents
from app.business.geo import haversine

EARTHQUAKE_DATA_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"


@lru_cache(maxsize=32)
def load_data(url: str) -> dict:
    data: dict = {}
    response: Response = get(url, follow_redirects=True)
    if response.status_code == codes.OK:
        data = response.json()
    return data


class EarthquakeEventBuilder:
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

    def build(self) -> EarthquakeEvents:
        data = load_data(EARTHQUAKE_DATA_URL)
        return EarthquakeEvents(earthquakes=self._get_earthquakes(data))

    def _get_earthquakes(self, data: dict) -> list[Earthquake]:
        earthquakes: list[Earthquake] = []
        for earthquake in data.get("features"):
            properties = earthquake.get("properties", {})
            geomertry = earthquake.get("geometry", {})

            latitude, longitude, depth = geomertry.get("coordinates", [0.0, 0.0, 0.0])
            distance = haversine(self.latitude, self.longitude, latitude, longitude)

            earthquakes.append(
                Earthquake(
                    magnitude=float(f"{properties.get('mag', 0.0):.3f}"),
                    place=properties.get("place", ""),
                    tsunami=bool(properties.get("tsunami", False)),
                    latitude=float(f"{latitude:.5f}"),
                    longitude=float(f"{longitude:.5f}"),
                    depth=float(f"{depth:.5f}"),
                    distance=distance,
                )
            )
        return earthquakes
