import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from redis import Redis
from starlette.responses import JSONResponse

app = FastAPI()

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Setup static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Redis connection
redis = Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379, db=0, decode_responses=True)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # Increment visit counter
    visit_count = redis.incr("visit_count")
    
    # Render template with visit count
    return templates.TemplateResponse("index.html", {"request": request, "visit_count": visit_count})

@app.get("/health")
async def health_check():
    try:
        # Check Redis connection
        redis.ping()
        return JSONResponse(content={"status": "healthy", "redis": "connected"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"status": "unhealthy", "redis": str(e)}, status_code=503)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)