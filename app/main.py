import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import redis
from app.world_generator import World

app = FastAPI()

# Jinja2 Templates setup
templates = Jinja2Templates(directory="templates")

# Static files setup
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

@app.get("/")
async def root(request: Request):
    visits = redis_client.incr("visit_count")
    return templates.TemplateResponse("index.html", {"request": request, "visits": visits})

@app.get("/health")
async def health():
    try:
        redis_client.ping()
        return JSONResponse(content={"status": "healthy", "redis": "connected"})
    except redis.ConnectionError:
        return JSONResponse(content={"status": "unhealthy", "redis": "disconnected"}, status_code=503)

@app.get("/world/{size}")
async def generate_world(size: int):
    world = World(size)
    world.define_tile_types()
    generated_world = world.generate_world()
    return JSONResponse(content={"world": generated_world})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)