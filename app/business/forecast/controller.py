from fastapi import APIRouter, Depends

from app.business.forecast.models import SeasonEvents
from app.business.forecast.rule import SeasonsEventBuilder

router = APIRouter(
    prefix="/forecast",
    tags=["forecast"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_data():
    return {"success": True}


@router.get("/seasons", response_model=SeasonEvents)
async def get_season_events_data(
    season_builder: SeasonsEventBuilder = Depends(SeasonsEventBuilder),
) -> SeasonEvents:
    return season_builder.build()
