import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import redis
from app.world_generator import World

app = FastAPI()

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Setup static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# WebSocket connections
active_connections = []

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for connection in active_connections:
                await connection.send_text(f"Message: {data}")
    except WebSocketDisconnect:
        active_connections.remove(websocket)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    visit_count = redis_client.incr("visit_count")
    return templates.TemplateResponse("index.html", {"request": request, "visit_count": visit_count})

@app.get("/world/{size}")
async def generate_world(size: int):
    world = World(size)
    world.define_tile_types()
    generated_world = world.generate_world()
    return {"world": generated_world}

@app.get("/health")
async def health_check():
    try:
        redis_client.ping()
        return {"status": "healthy", "redis": "connected"}
    except redis.ConnectionError:
        return {"status": "unhealthy", "redis": "disconnected"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)