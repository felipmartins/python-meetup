from fastapi.testclient import TestClient
from src.app import (
    app,
)

client = TestClient(app)



def test_health_route():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
