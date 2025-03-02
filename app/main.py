import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
import redis
import json
from typing import List
from app.world_generator import World

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Redis connection
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_client = redis.Redis(host=redis_host, port=6379, db=0)

# WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client left the chat")

@app.get("/")
async def root(request: Request):
    visits = redis_client.incr("visit_count")
    return templates.TemplateResponse("index.html", {"request": request, "visits": visits})

@app.get("/world/{size}")
async def generate_world(size: int):
    world = World(size)
    world.define_tile_types()
    world.generate_world()
    return JSONResponse(content={"world": world.get_world_grid()})

@app.get("/health")
async def health_check():
    try:
        redis_client.ping()
        return JSONResponse(content={"status": "healthy", "redis": "connected"})
    except redis.ConnectionError:
        return JSONResponse(content={"status": "unhealthy", "redis": "disconnected"}, status_code=503)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)