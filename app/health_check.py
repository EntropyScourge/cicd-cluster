from fastapi.testclient import TestClient
from app import app
import pytest

@pytest.fixture(scope="function")
def client():
    return TestClient(app)


def test_returns_healthy_on_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}