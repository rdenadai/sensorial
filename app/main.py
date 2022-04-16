from uuid import uuid4

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app import __version__
from app.business.astronomy.controller import router as astronomy_router
from app.business.earthquake.controller import router as earthquake_router
from app.business.forecast.controller import router as forecast_router
from app.components.aws.dynamodb import DynamoDBService
from app.config import DESCRIPTION, TITLE

app = FastAPI(
    title=TITLE,
    version=__version__,
    description=DESCRIPTION,
    redoc_url=None,
    root_path="/api",
)
app.include_router(astronomy_router)
app.include_router(earthquake_router)
app.include_router(forecast_router)


@app.get("/")
async def health_check():
    return {"success": True}
