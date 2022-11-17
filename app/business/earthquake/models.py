from typing import Optional

from pydantic import BaseModel


class Earthquake(BaseModel):
    magnitude: float
    place: str
    tsunami: bool
    distance: float
    depth: float
    latitude: float
    longitude: float


class EarthquakeEvents(BaseModel):
    earthquakes: list[Optional[Earthquake]]
