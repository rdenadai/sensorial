from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import __version__
from app.business.astronomy.planets.controller import router as solar_system_router
from app.business.astronomy.sattelite.controller import router as sattelite_router
from app.business.earthquake.controller import router as earthquake_router
from app.business.forecast.controller import router as forecast_router
from app.config import DESCRIPTION, TITLE

templates = Jinja2Templates(directory="static/templates")

app = FastAPI(
    title=TITLE,
    version=__version__,
    description=DESCRIPTION,
    redoc_url=None,
)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(sattelite_router)
app.include_router(solar_system_router)
app.include_router(forecast_router)
app.include_router(earthquake_router)


@app.get("/health")
async def health_check():
    return {"success": True}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "name": "main"})


@app.get("/terms", response_class=HTMLResponse)
async def terms(request: Request):
    return templates.TemplateResponse("terms.html", {"request": request, "name": "terms"})
