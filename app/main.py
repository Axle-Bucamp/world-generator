import os
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import redis
import uvicorn

app = FastAPI()

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Redis connection
redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = os.environ.get('REDIS_PORT', 6379)
redis_client = redis.Redis(host=redis_host, port=redis_port, db=0, decode_responses=True)

def get_redis():
    return redis_client

@app.get("/", response_class=HTMLResponse)
async def root(request: Request, redis: redis.Redis = Depends(get_redis)):
    # Increment the visit counter
    visit_count = redis.incr("visit_count")
    
    # Render the template with the visit count
    return templates.TemplateResponse("index.html", {"request": request, "visit_count": visit_count})

@app.get("/health")
async def health(redis: redis.Redis = Depends(get_redis)):
    try:
        redis.ping()
        return {"status": "healthy", "redis": "connected"}
    except redis.exceptions.ConnectionError:
        return {"status": "unhealthy", "redis": "disconnected"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)