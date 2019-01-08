from starlette.responses import HTMLResponse
from starlette.responses import JSONResponse
from starlette.responses import Response
import uvicorn
from config import app


@app.route('/')
async def index(request):
    template = app.get_template('index.html')
    content = template.render(request=request)
    return HTMLResponse(content)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8585)
