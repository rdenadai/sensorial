from app.business.astronomy.sattelite.models import Sattelite, Sattelites
from app.business.astronomy.sattelite.rule import SatteliteRules
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/astronomy/sattelite",
    tags=["astronomy", "sattelite"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=Sattelites)
async def get_data(sattelite_rules: SatteliteRules = Depends(SatteliteRules)) -> Sattelites:
    return sattelite_rules.load_all_data()


@router.get("/iss", response_model=Sattelite)
async def get_iss_data(sattelite_rules: SatteliteRules = Depends(SatteliteRules)) -> Sattelite:
    return sattelite_rules.load_iss_data()


@router.get("/hubble", response_model=Sattelite)
async def get_hubble_data(sattelite_rules: SatteliteRules = Depends(SatteliteRules)) -> Sattelite:
    return sattelite_rules.load_hubble_data()
