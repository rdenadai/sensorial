import re
from math import asin, cos, pow, radians, sin, sqrt


def decdeg2dms(decdeg: float) -> tuple[float, float, float]:
    negative: bool = decdeg < 0
    decdeg = abs(decdeg)
    minutes, seconds = divmod(decdeg * 3600, 60)
    degrees, minutes = divmod(minutes, 60)
    if negative:
        if degrees > 0:
            degrees = -degrees
        elif minutes > 0:
            minutes = -minutes
        else:
            seconds = -seconds
    return (degrees, minutes, seconds)


# Given a comma separated DMS coordinate "lat,lng",
# returns a array of decimals [lat,lng]
# Ex: "48°53'10.18"N,2°20'35.09"E" to "48.8866, 2.34330"
# https://gist.github.com/adamraudonis/7671459
def dms_coord_2_dec_array(dms_coord_str: str) -> tuple[float, float]:
    lat, lng = dms_coord_str.split(",")
    return (dms2dec(lat), dms2dec(lng))


# Given a comma separated DMS coordinate "lat,lng",
# returns a decimal coordinate string
# Ex: "48°53'10.18"N,2°20'35.09"E" to "48.8866, 2.34330"
# https://gist.github.com/adamraudonis/7671459
def dms_coord_2_dec_str(dms_coord_str: str) -> str:
    lat, lng = dms_coord_str.split(",")
    return f"{dms2dec(lat)},{dms2dec(lng)}"


# Returns decimal representation of DMS
# https://gist.github.com/adamraudonis/7671459
# http://en.wikipedia.org/wiki/Geographic_coordinate_conversion
def dms2dec_n(dms_str: str) -> float:
    if dms_str.find("'") == -1:
        return float(dms_str)

    sign = 1
    if re.match("[swSW]", dms_str) or re.match("[-]", dms_str):
        sign = -1

    # Remove possible ending cardinal direction
    dms_str = re.sub("[swSWneNE]", "", dms_str).strip()
    # Split based on ° ' "
    dms_array = re.split("\xc2\xb0|'|\"", dms_str)

    degree = dms_array[0].strip()
    minute = dms_array[1].strip()
    second = 0
    if len(dms_array) > 2 and len(dms_array[2]) > 0:
        second = dms_array[2]

    return sign * (int(degree) + float(minute) / 60 + float(second) / 3600)


# http://en.wikipedia.org/wiki/Geographic_coordinate_conversion
def dms2dec(dms_str: str) -> float:
    """Return decimal representation of DMS

    >>> dms2dec(utf8(48°53'10.18"N))
    48.8866111111F
    >>> dms2dec(utf8(2°20'35.09"E))
    2.34330555556F
    >>> dms2dec(utf8(48°53'10.18"S))
    -48.8866111111F
    >>> dms2dec(utf8(2°20'35.09"W))
    -2.34330555556F
    """
    sign = 1
    dms_str = re.sub(r"\s", "", dms_str)
    if re.match("[swSW-]", dms_str):
        sign = -1

    dms_str = dms_str.replace("-", "")
    (degree, minute, second, frac_seconds) = re.split("\D+", dms_str, maxsplit=4)
    frac_seconds_len = len(frac_seconds)
    frac_seconds = float(frac_seconds)
    frac_seconds /= pow(10, frac_seconds_len)
    return sign * (int(degree) + float(minute) / 60 + float(second) / 3600 + float(frac_seconds) / 36000)


def haversine(lng1: float, lat1: float, lng2: float, lat2: float) -> int:
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    dlat = radians(lat2 - lat1)
    dlon = radians(lng2 - lng1)
    # convert to radians
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    # haversine formula
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return int(c * r)
