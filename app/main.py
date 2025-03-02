from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import redis
import uvicorn

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Setup Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # Increment visit counter
    visit_count = redis_client.incr('visit_count')
    
    # Render template with visit count
    return templates.TemplateResponse("index.html", {"request": request, "visit_count": visit_count})

@app.get("/health")
async def health_check():
    try:
        redis_client.ping()
        return {"status": "healthy", "redis": "connected"}
    except redis.ConnectionError:
        return {"status": "unhealthy", "redis": "disconnected"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)