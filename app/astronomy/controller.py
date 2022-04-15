from app.astronomy.models import Sattelites
from app.astronomy.rule import load_sattelite_data
from fastapi import APIRouter

router = APIRouter(
    prefix="/astronomy",
    tags=["astronomy"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=Sattelites)
async def get_data():
    return load_sattelite_data()
