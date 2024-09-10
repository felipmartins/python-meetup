from fastapi.testclient import TestClient
from src.app import (
    app,
)

client = TestClient(app)


def test_home_route():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome Python MeetUp 2024!!"}


def test_health_route():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
