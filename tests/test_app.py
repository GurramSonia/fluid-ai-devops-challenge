from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_liveness():
    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json()["status"] == "alive"