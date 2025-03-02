import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from redis import Redis
from pydantic import BaseModel
from typing import List
import json
from app.world_generator import World

app = FastAPI()

# Static files and Jinja2 templates setup
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Redis connection
redis_host = os.getenv("REDIS_HOST", "localhost")
redis = Redis(host=redis_host, port=6379, db=0, decode_responses=True)

# WebSocket connection manager
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

# Root route
@app.get("/")
async def root(request: Request):
    visits = redis.incr("visit_count")
    return templates.TemplateResponse("index.html", {"request": request, "visits": visits})

# WebSocket route for chat
@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client disconnected")

# World generation route
@app.get("/world/{size}")
async def generate_world(size: int):
    world = World(size)
    world.generate_world()
    return {"world": world.get_world_grid()}

# Health check route
@app.get("/health")
async def health_check():
    try:
        redis.ping()
        return {"status": "healthy", "redis": "connected"}
    except:
        return {"status": "unhealthy", "redis": "disconnected"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)