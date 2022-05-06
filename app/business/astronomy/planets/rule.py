from calendar import timegm
from datetime import datetime

from ephem import Moon, Observer, constellation, next_full_moon, next_new_moon
from numpy import rad2deg

from app.business.astronomy.planets.models import Planet, PlanetType, SolarSystem


class ObserverBuilder:
    def __init__(self, lat: str, lng: str, alt: str):
        self.lat = lat
        self.lng = lng
        self.alt = alt

    def build(self) -> Observer:
        observer = Observer()
        observer.lat = self.lat
        observer.lon = self.lng
        observer.elevation = self.alt
        return observer


class PlanetBuilder:
    def __init__(self, observer: Observer) -> None:
        self.__observer = observer

    def build(self, planet_type: PlanetType) -> Planet:
        ephem_planet = planet_type()
        ephem_planet.compute(self.__observer)
        data = {
            "name": ephem_planet.name,
            "sun_distance": "{0:.5f}".format(ephem_planet.sun_distance),
            "earth_distance": "{0:.5f}".format(ephem_planet.earth_distance),
            "phase": int(ephem_planet.phase),
            "zodiac": constellation(ephem_planet)[1].lower(),
            "ra": ephem_planet.ra,
            "dec": ephem_planet.dec,
            "altitude": "{0:.2f}".format(rad2deg(ephem_planet.alt)),
            "azimut": "{0:.2f}".format(rad2deg(ephem_planet.az)),
            "mag": "{0:.2f}".format(ephem_planet.mag),
        }
        planet = Planet(**data)
        if isinstance(ephem_planet, Moon):
            dtime = datetime.utcnow()
            planet.moon_phase = int(ephem_planet.moon_phase * 100)
            planet.next_new_moon = timegm(next_new_moon(dtime).datetime().timetuple())
            planet.next_full_moon = timegm(next_full_moon(dtime).datetime().timetuple())
        return planet


class SolarSystemBuilder:
    def __init__(self, lat: str, lng: str, alt: str):
        self.lat = lat
        self.lng = lng
        self.alt = alt

    def build(self):
        observer = ObserverBuilder(self.lat, self.lng, self.alt).build()
        planet_builder = PlanetBuilder(observer)
        solar_system: dict[str:Planet] = {
            planet_type.name.title(): planet_builder.build(planet_type.value)
            for planet_type in PlanetType
        }
        return SolarSystem(**solar_system)
