from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from .dependencies import get_redis

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    redis = get_redis()
    visit_count = redis.incr("visits")
    return templates.TemplateResponse("index.html", {"request": request, "visit_count": visit_count})

@app.get("/health")
async def health_check():
    return {"status": "healthy"}