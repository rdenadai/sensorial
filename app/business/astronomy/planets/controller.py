from fastapi import APIRouter

from app.business.astronomy.planets.models import SolarSystem
from app.business.astronomy.planets.rule import SolarSystemBuilder

router = APIRouter(
    prefix="/astronomy/solar_system",
    tags=["astronomy", "solar_system"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=SolarSystem)
async def get_data(latitude: float, longitude: float, altitude: float) -> SolarSystem:
    solar_system: SolarSystem = SolarSystemBuilder(
        latitude=latitude,
        longitude=longitude,
        altitude=altitude,
    ).build()
    return solar_system
