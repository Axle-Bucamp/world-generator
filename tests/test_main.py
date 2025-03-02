import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to Asgard World Generator" in response.text

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "redis_connected": True}

@pytest.mark.parametrize("size", [10, 20, 50])
def test_generate_world(size):
    response = client.get(f"/world/{size}")
    assert response.status_code == 200
    assert f"World size: {size}x{size}" in response.text

def test_invalid_world_size():
    response = client.get("/world/101")
    assert response.status_code == 400
    assert "Invalid world size" in response.text

@pytest.mark.asyncio
async def test_websocket_chat():
    with client.websocket_connect("/ws/chat") as websocket:
        data = "Hello, Asgard!"
        await websocket.send_text(data)
        response = await websocket.receive_text()
        assert data in response

# Additional test for world coordinates
def test_world_coordinates():
    response = client.get("/world/10/5")
    assert response.status_code == 200
    assert "World coordinates: x=10, z=5" in response.text