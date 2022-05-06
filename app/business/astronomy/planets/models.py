from enum import Enum
from typing import Optional

from ephem import Jupiter, Mars, Mercury, Moon, Neptune, Pluto, Saturn, Sun, Uranus, Venus
from pydantic import BaseModel


class PlanetType(Enum):
    SUN = Sun
    MERCURY = Mercury
    VENUS = Venus
    MOON = Moon
    MARS = Mars
    JUPITER = Jupiter
    SATURN = Saturn
    NEPTUNE = Neptune
    URANUS = Uranus
    PLUTO = Pluto


class Planet(BaseModel):
    name: str
    sun_distance: str
    earth_distance: str
    phase: int
    zodiac: str
    ra: Optional[float] = 0.0
    dec: Optional[float] = 0.0
    altitude: str
    azimut: str
    mag: str
    moon_phase: Optional[int] = 0
    next_new_moon: Optional[int] = 0
    next_full_moon: Optional[int] = 0


class SolarSystem(BaseModel):
    Sun: Planet
    Mercury: Planet
    Venus: Planet
    Moon: Planet
    Mars: Planet
    Jupiter: Planet
    Saturn: Planet
    Uranus: Planet
    Neptune: Planet
    Pluto: Planet
