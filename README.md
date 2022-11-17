# Sensorial

This is a free API that can be used to collect the following features

 - Sattelite from Hubble and ISS
 - Solar System data (planets and the moon)
 - Seasons data
 - Earthquake data

## Sources

Hubble and ISS data are taken from [**Celestrak**](https://celestrak.org/).

 - [Hubble Space Telescope (HST)](http://www.celestrak.com/NORAD/elements/science.txt)
 - [International Space Station (ISS)](http://www.celestrak.com/NORAD/elements/stations.txt)

Earthquake Data is taken from [**USGS**](https://www.usgs.gov/programs/earthquake-hazards/earthquakes)

 - [USGS Earthquake (all hour)](https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson)

Solar System and Seasons are calculated using [**pyephem**](https://pypi.org/project/pyephem/)
