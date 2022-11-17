from fastapi import APIRouter

from app.business.earthquake.models import EarthquakeEvents
from app.business.earthquake.rule import EarthquakeEventBuilder

router = APIRouter(
    prefix="/earthquake",
    tags=["earthquake"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_data(latitude: float, longitude: float) -> EarthquakeEvents:
    return EarthquakeEventBuilder(latitude, longitude).build()
