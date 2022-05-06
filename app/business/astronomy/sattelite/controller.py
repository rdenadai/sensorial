from fastapi import APIRouter, Depends

from app.business.astronomy.sattelite.models import HST, ISS, Sattelite, Sattelites
from app.business.astronomy.sattelite.rule import SatteliteRules, SattelitesRules

router = APIRouter(
    prefix="/astronomy/sattelite",
    tags=["astronomy", "sattelite"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=Sattelites)
async def get_data(latitude: float, longitude: float, altitude: float) -> Sattelites:
    return SattelitesRules(
        latitude=latitude, longitude=longitude, altitude=altitude
    ).calculate_all()


@router.get("/iss", response_model=Sattelite)
async def get_iss_data(latitude: float, longitude: float, altitude: float) -> Sattelite:
    return SatteliteRules(latitude=latitude, longitude=longitude, altitude=altitude).calculate(
        sattelite_type=ISS
    )


@router.get("/hubble", response_model=Sattelite)
async def get_hubble_data(latitude: float, longitude: float, altitude: float) -> Sattelite:
    return SatteliteRules(latitude=latitude, longitude=longitude, altitude=altitude).calculate(
        sattelite_type=HST
    )
