import asyncio
import random
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from redis import Redis
from pydantic import BaseModel
from typing import List, Dict
from app.world_generator import World

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Redis connection
redis = Redis(host="localhost", port=6379, db=0)

# WebSocket connections
active_connections: List[WebSocket] = []

class ChatMessage(BaseModel):
    message: str
    sender: str

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = ChatMessage(message=data, sender=str(websocket.client))
            await broadcast_message(message)
    except WebSocketDisconnect:
        active_connections.remove(websocket)

async def broadcast_message(message: ChatMessage):
    for connection in active_connections:
        await connection.send_text(message.json())

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    visit_count = redis.incr("visit_count")
    return templates.TemplateResponse("index.html", {"request": request, "visit_count": visit_count})

@app.get("/world/{size}")
async def generate_world(size: int):
    if size < 1 or size > 100:
        return {"error": "Size must be between 1 and 100"}
    
    world = World(size, size)
    world.define_tile_types()
    world.generate_world()
    
    return {"message": f"World of size {size}x{size} generated successfully", "world": world.grid}

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