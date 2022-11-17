from calendar import timegm
from datetime import datetime
from typing import Any, Type

from ephem import Moon, Observer, constellation, next_full_moon, next_new_moon
from numpy import rad2deg

from app.business.astronomy.planets.models import Planet, PlanetType, SolarSystem


class ObserverBuilder:
    def __init__(self, latitude: float, longitude: float, altitude: float):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    def build(self) -> Observer:
        observer = Observer()
        observer.lat = self.latitude
        observer.lon = self.longitude
        observer.elevation = self.altitude
        return observer


class PlanetBuilder:
    def __init__(self, observer: Observer) -> None:
        self.__observer = observer

    def build(self, planet_type: Type[PlanetType]) -> Planet:
        ephem_planet: Any = planet_type()
        ephem_planet.compute(self.__observer)
        data = {
            "name": ephem_planet.name,
            "sun_distance": float(f"{ephem_planet.sun_distance:.6f}"),
            "earth_distance": float(f"{ephem_planet.earth_distance:.6f}"),
            "phase": int(ephem_planet.phase),
            "zodiac": constellation(ephem_planet)[1].lower(),
            "ra": ephem_planet.ra,
            "dec": ephem_planet.dec,
            "altitude": float(f"{rad2deg(ephem_planet.alt):.3f}"),
            "azimut": float(f"{rad2deg(ephem_planet.az):.3f}"),
            "mag": float(f"{ephem_planet.mag:.3f}"),
        }
        planet = Planet(**data)
        if isinstance(ephem_planet, Moon):
            dtime = datetime.utcnow()
            planet.moon_phase = int(ephem_planet.moon_phase * 100)
            planet.next_new_moon = timegm(next_new_moon(dtime).datetime().timetuple())
            planet.next_full_moon = timegm(next_full_moon(dtime).datetime().timetuple())
        return planet


class SolarSystemBuilder:
    def __init__(self, latitude: float, longitude: float, altitude: float):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    def build(self):
        observer = ObserverBuilder(self.latitude, self.longitude, self.altitude).build()
        planet_builder = PlanetBuilder(observer)
        solar_system: dict[str:Planet] = {
            planet_type.name.title(): planet_builder.build(planet_type.value) for planet_type in PlanetType
        }
        return SolarSystem(**solar_system)
