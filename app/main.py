from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app import __version__
from app.astronomy.controller import router as astronomy_router
from app.config import DESCRIPTION, TITLE
from app.earthquake.controller import router as earthquake_router
from app.forecast.controller import router as forecast_router


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=TITLE,
        version=__version__,
        description=DESCRIPTION,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = FastAPI(redoc_url=None)
app.openapi = custom_openapi
app.include_router(astronomy_router)
app.include_router(earthquake_router)
app.include_router(forecast_router)
