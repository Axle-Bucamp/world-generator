import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import redis
import uvicorn

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Setup Redis connection
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = os.getenv("REDIS_PORT", 6379)
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
        return JSONResponse(content={"status": "healthy", "redis": "connected"}, status_code=200)
    except redis.ConnectionError:
        return JSONResponse(content={"status": "unhealthy", "redis": "disconnected"}, status_code=503)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)