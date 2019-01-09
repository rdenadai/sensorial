from starlette.applications import Starlette
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles


app = Starlette(debug=False, template_directory='./site/templates')
# app.add_middleware(GZipMiddleware, minimum_size=500)
app.add_middleware(CORSMiddleware, allow_origins=['*'])
app.mount('/static', StaticFiles(directory='./site/media/'), name='static')
