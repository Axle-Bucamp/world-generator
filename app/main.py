import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import redis
import uvicorn

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Set up Redis connection
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_client = redis.Redis(host=redis_host, port=redis_port, db=0, decode_responses=True)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # Increment visit counter
    visit_count = redis_client.incr("visit_count")
    
    # Render template with visit count
    return templates.TemplateResponse("index.html", {"request": request, "visit_count": visit_count})

@app.get("/health")
async def health_check():
    try:
        # Check Redis connection
        redis_client.ping()
        return {"status": "healthy", "redis_connection": "ok"}
    except redis.ConnectionError:
        return {"status": "unhealthy", "redis_connection": "failed"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)