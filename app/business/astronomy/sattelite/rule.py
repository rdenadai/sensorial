from calendar import timegm
from functools import lru_cache
from typing import Type

from ephem import Observer, Sun, degrees, minute, readtle, second
from httpx import Response, codes, get
from numpy import rad2deg

from app.business.astronomy.sattelite.models import HST, ISS, Sattelite, Sattelites
from app.business.geo import dms2dec

HST_DATA_URL = "http://www.celestrak.com/NORAD/elements/science.txt"
ISS_DATA_URL = "http://www.celestrak.com/NORAD/elements/stations.txt"


@lru_cache(maxsize=32)
def load_data(url: str) -> list[str]:
    data: list[str] = []
    response: Response = get(url, follow_redirects=True)
    if response.status_code == codes.OK:
        data = response.text.lower().split("\r\n")
    return data


class SatteliteBuilder:
    def build(self, sattelite_type: Type[Sattelite]) -> Type[Sattelite]:
        url = HST_DATA_URL
        if issubclass(sattelite_type, ISS):
            url = ISS_DATA_URL
        return sattelite_type(load_data(url))


class SatteliteRules:
    def __init__(self, latitude: float, longitude: float, altitude: float) -> None:
        self.sattelite: Type[Sattelite] | None = None
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    def calculate(self, sattelite_type: Type[Sattelite]) -> Type[Sattelite]:
        self.sattelite = SatteliteBuilder().build(sattelite_type)
        computed_tle = readtle(self.sattelite.name, self.sattelite.tle_1, self.sattelite.tle_2)
        computed_tle.compute()
        self.sattelite.latitude = float(f"{dms2dec(str(computed_tle.sublat)):.6f}")
        self.sattelite.longitude = float(f"{dms2dec(str(computed_tle.sublong)):.6f}")
        self.sattelite.elevation = computed_tle.elevation
        # COMPUTE NEXT 5 VISIBLE PASSES
        self.sattelite.next_passes = self.__get_next_visible_passes()
        return self.sattelite

    # http://www.stjarnhimlen.se/comp/tutorial.html
    # http://space.stackexchange.com/questions/4339/calculating-which-satellite-passes-are-visible/4347#4347
    # http://spotthestation.nasa.gov/sightings/view.cfm?country=Australia&region=New_South_Wales&city=Sydney#.VF39trtyi8M
    # https://bugs.launchpad.net/pyephem/+bug/572402
    def __get_next_visible_passes(self) -> list[dict]:
        number_passes: list[dict] = []
        sun = Sun()
        computed_tle = readtle(self.sattelite.name, self.sattelite.tle_1, self.sattelite.tle_2)

        home = Observer()
        home.lat = degrees(str(self.latitude))
        home.lon = degrees(str(self.longitude))
        home.elevation = self.altitude

        computed_mins = 45 * minute
        computed_secs = 45 * second
        n_pass_count = 0
        while n_pass_count < 2:
            tr, azr, tt, altt, ts, azs = home.next_pass(computed_tle)
            rise_time = tr.datetime()
            max_time = tt.datetime()
            set_time = ts.datetime()
            duration = (set_time - rise_time).total_seconds()

            # Compute for the rise time
            home.date = tr
            sun.compute(home)
            computed_tle.compute(home)

            # rise time values
            r_sun_alt = rad2deg(sun.alt)
            r_sat_eclipsed = computed_tle.eclipsed
            r_sat_az = rad2deg(computed_tle.az)
            r_sat_alt = rad2deg(computed_tle.alt)
            r_sat_elevation = computed_tle.elevation

            # We must find when the satellite will be visible, because in the max could not be!
            max_iter = 0
            while r_sat_eclipsed or max_iter >= 5000:
                tr += computed_secs
                home.date = tr
                sun.compute(home)
                computed_tle.compute(home)

                r_sun_alt = rad2deg(sun.alt)
                r_sat_eclipsed = computed_tle.eclipsed
                r_sat_az = rad2deg(computed_tle.az)
                r_sat_alt = rad2deg(computed_tle.alt)
                r_sat_elevation = computed_tle.elevation
                max_iter += 1

            # Now we must compute for the max time
            home.date = tt
            sun.compute(home)
            computed_tle.compute(home)

            # max time values
            m_sun_alt = rad2deg(sun.alt)
            m_sat_eclipsed = computed_tle.eclipsed
            m_sat_az = rad2deg(computed_tle.az)
            m_sat_alt = rad2deg(computed_tle.alt)
            m_sat_elevation = computed_tle.elevation

            # We must find when the satellite will be visible, because in the max could not be!
            max_iter = 0
            while m_sat_eclipsed or max_iter >= 5000:
                tt -= computed_secs
                home.date = tt
                sun.compute(home)
                computed_tle.compute(home)

                m_sun_alt = rad2deg(sun.alt)
                m_sat_eclipsed = computed_tle.eclipsed
                m_sat_az = rad2deg(computed_tle.az)
                m_sat_alt = rad2deg(computed_tle.alt)
                m_sat_elevation = computed_tle.elevation
                max_iter += 1

            home.date = ts + computed_mins

            if (
                (r_sat_eclipsed is False and m_sat_eclipsed is False)
                and (-55 <= r_sun_alt < 5 and -35 <= m_sun_alt < -6)
                and m_sat_alt > 8
                and duration >= 60
            ):
                number_passes.append(
                    {
                        "rise_time": timegm(rise_time.timetuple()),
                        "rise_azimuth": float(f"{r_sat_az:.3f}"),
                        "rise_altitude": float(f"{r_sat_alt:.3f}"),
                        "rise_elevation": int(r_sat_elevation),
                        "rise_sun_altitude": float(f"{r_sun_alt:.3f}"),
                        "max_time": timegm(max_time.timetuple()),
                        "max_azimuth": float(f"{m_sat_az:.3f}"),
                        "max_altitude": float(f"{m_sat_alt:.3f}"),
                        "max_elevation": int(m_sat_elevation),
                        "max_sun_altitude": float(f"{m_sun_alt:.3f}"),
                        "duration": int(duration / 60),
                    }
                )
                n_pass_count += 1
        return number_passes


class SattelitesRules(SatteliteRules):
    def calculate_all(self) -> Sattelites:
        return Sattelites(
            hst=self.calculate(HST),
            iss=self.calculate(ISS),
        )
