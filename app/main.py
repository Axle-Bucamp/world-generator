from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
from app.dependencies import get_redis

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, redis=Depends(get_redis)):
    visits = await redis.incr("visits")
    return templates.TemplateResponse("index.html", {"request": request, "visits": visits})

@app.get("/health")
async def health_check(redis=Depends(get_redis)):
    try:
        await redis.ping()
        return {"status": "healthy"}
    except:
        return {"status": "unhealthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)