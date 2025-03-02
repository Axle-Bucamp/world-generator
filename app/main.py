import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from redis import Redis
from starlette.requests import Request
from starlette.websockets import WebSocketState
from typing import List
from app.world_generator import World

app = FastAPI()

# Setup static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Setup Redis connection
redis_host = os.getenv("REDIS_HOST", "localhost")
redis = Redis(host=redis_host, port=6379, db=0, decode_responses=True)

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
            if connection.application_state == WebSocketState.CONNECTED:
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
        await manager.broadcast("A user has left the chat")

@app.get("/")
async def root(request: Request):
    visits = redis.incr("visit_count")
    return templates.TemplateResponse("index.html", {"request": request, "visits": visits})

@app.get("/health")
async def health():
    try:
        redis.ping()
        return {"status": "healthy", "redis": "connected"}
    except:
        return {"status": "unhealthy", "redis": "disconnected"}

@app.get("/world/{size}")
async def generate_world(size: int):
    if size <= 0 or size > 100:
        raise HTTPException(status_code=400, detail="Size must be between 1 and 100")
    world = World(size)
    world.generate_world()
    return {"world": world.get_world_grid()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)