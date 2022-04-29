from uuid import uuid4

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app import __version__
from app.business.astronomy.planets.controller import router as solar_system_router
from app.business.astronomy.sattelite.controller import router as sattelite_router
from app.business.earthquake.controller import router as earthquake_router
from app.business.forecast.controller import router as forecast_router
from app.config import DESCRIPTION, TITLE

app = FastAPI(
    title=TITLE,
    version=__version__,
    description=DESCRIPTION,
    redoc_url=None,
    root_path="/api",
)
app.include_router(sattelite_router)
app.include_router(solar_system_router)
app.include_router(forecast_router)
app.include_router(earthquake_router)


@app.get("/")
async def health_check():
    return {"success": True}
