from app.business.astronomy.planets.models import SolarSystem
from app.business.astronomy.planets.rule import SolarSystemBuilder
from fastapi import APIRouter

router = APIRouter(
    prefix="/astronomy/solar_system",
    tags=["astronomy", "solar_system"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=SolarSystem)
async def get_data(latitude: float, longitude: float, altitude: float) -> SolarSystem:
    solar_system_builder = SolarSystemBuilder(lat=latitude, lng=longitude, alt=altitude)
    solar_system: SolarSystem = solar_system_builder.build()
    return solar_system
